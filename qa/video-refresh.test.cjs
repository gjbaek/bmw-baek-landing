'use strict';
const {test} = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const vm = require('node:vm');
const saved = require('../dist/videos.json');
const source = fs.readFileSync('dist/video-player.js', 'utf8');
const payload = {status: 'live', channelId: 'UCam_yvB4qEmWmAWfT8uy3SQ', videos: [
  {id: 'TvuWH4ZJGFQ', title: 'Old upload', publishedAt: '2020-01-01T00:00:00Z'},
  {id: 'b-wbgk1aP90', title: '<img src=x onerror=alert(1)> & 새 영상', publishedAt: '2020-02-01T00:00:00Z'}
]};
const settle = () => new Promise(resolve => setImmediate(resolve));

function setup(fetchImpl) {
  const elements = new Map();
  class Element {
    constructor(tag = 'div') {this.tag = tag; this.handlers = {}; this.children = []; this.attrs = {}; this.dataset = {}; this.textContent = ''; this.classList = {add(){}, remove(){}};}
    set innerHTML(_) {throw new Error('Remote titles must not become HTML');}
    append(...nodes) {nodes.forEach(node => this.appendChild(node));}
    appendChild(node) {this.children.push(node); if (node.id) elements.set(node.id, node);}
    replaceChildren(...nodes) {this.children = []; this.append(...nodes);}
    addEventListener(name, handler) {(this.handlers[name] ||= []).push(handler);}
    async fire(name) {for (const fn of this.handlers[name] || []) await fn({target: this});}
    setAttribute(name, value) {this.attrs[name] = value;}
    querySelector(selector) {return this.querySelectorAll(selector)[0];}
    querySelectorAll(selector) {
      const matches = element => selector === 'strong' ? element.tag === 'strong' : selector === 'img' ? element.tag === 'img' : selector.startsWith('.') && element.className === selector.slice(1);
      return this.children.flatMap(child => [...(matches(child) ? [child] : []), ...child.querySelectorAll(selector)]);
    }
    remove() {}
  }
  for (const id of ['play-video', 'video-poster', 'player-error', 'video-status', 'previous-video', 'next-video', 'current-video-title', 'video-category', 'watch-youtube', 'youtube-mount', 'retry-video', 'video-feed-status', 'video-count']) elements.set(id, new Element());
  const list = new Element();
  const playlist = new Element();
  const initial = saved.map(video => {
    const item = new Element('button'); item.className = 'playlist-item'; item.dataset.videoId = video.id;
    item.querySelector = selector => ({strong: {textContent: video.title}, '.playlist-copy > span': {textContent: video.category}, img: {src: video.thumbnail}}[selector]);
    list.appendChild(item); return item;
  });
  const document = new Element();
  document.hidden = false;
  document.querySelectorAll = () => initial;
  document.querySelector = selector => selector === '.playlist-items' ? list : playlist;
  document.getElementById = id => elements.get(id);
  document.createElement = tag => new Element(tag);
  document.head = new Element();
  const players = [];
  const window = {setInterval: fn => {window.tick = fn;}, YT: {PlayerState: {ENDED: 0}, Player: function(id, options) {
    this.events = options.events; this.loads = []; this.loadVideoById = id => this.loads.push(id); this.playVideo = () => {}; this.destroy = () => {}; players.push(this);
  }}};
  const context = {document, window, location: {origin: 'http://localhost:4173'}, fetch: fetchImpl, Intl, Date, AbortSignal, URLSearchParams, setTimeout: () => 1, clearTimeout: () => {}};
  vm.runInNewContext(source, context);
  return {elements, list, playlist, initial, window, players, document};
}

test('live list sorts by upload date, inserts titles as text, and preserves playback controls', async () => {
  const app = setup(async () => ({ok: true, json: async () => payload}));
  await settle();
  const buttons = app.list.querySelectorAll('.playlist-item');
  assert.equal(buttons.length, 2);
  assert.equal(buttons[0].dataset.videoId, 'b-wbgk1aP90');
  assert.equal(buttons[0].querySelector('strong').textContent, payload.videos[1].title);
  assert.equal(app.elements.get('video-count').textContent, '2 VIDEOS');
  assert.equal(app.elements.get('previous-video').disabled, true);
  await buttons[0].fire('click');
  await settle();
  app.players[0].events.onReady({target: app.players[0]});
  await app.elements.get('next-video').fire('click');
  assert.equal(app.players[0].loads.at(-1), 'TvuWH4ZJGFQ');
  assert.equal(app.elements.get('next-video').disabled, true);
  await app.window.tick();
  assert.equal(app.list.querySelectorAll('.playlist-item')[0], buttons[0]);
});

test('late response cannot replace a video the visitor has already selected', async () => {
  let finish;
  const app = setup(() => new Promise(resolve => {finish = resolve;}));
  await app.initial[2].fire('click');
  finish({ok: true, json: async () => payload});
  await settle();
  assert.equal(app.list.children.length, saved.length);
  assert.equal(app.elements.get('current-video-title').textContent, saved[2].title);
});

test('failures retain the initial or last successful list, and hidden tabs do not poll', async () => {
  let calls = 0;
  let succeed = false;
  const app = setup(async () => {calls++; return {ok: true, json: async () => succeed ? payload : {status: 'fallback'}};});
  await settle();
  assert.equal(app.list.children.length, saved.length);
  assert.match(app.elements.get('video-feed-status').textContent, /저장된 영상/);
  app.document.hidden = true;
  await app.window.tick();
  assert.equal(calls, 1);
  app.document.hidden = false;
  succeed = true;
  await app.window.tick();
  assert.equal(app.list.children.length, 2);
  succeed = false;
  await app.window.tick();
  assert.equal(app.list.children.length, 2);
  assert.match(app.elements.get('video-feed-status').textContent, /마지막으로/);
});

test('keyboard focus keeps controls stable while an update is in flight', async () => {
  let finish;
  const app = setup(() => new Promise(resolve => {finish = resolve;}));
  await app.playlist.fire('focusin');
  finish({ok: true, json: async () => payload});
  await settle();
  assert.equal(app.list.children[0], app.initial[0]);
});
