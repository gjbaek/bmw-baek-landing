// Offline unit checks: a fake DOM/YouTube API; no network requests.
const fs = require('node:fs');
const vm = require('node:vm');
const assert = require('node:assert/strict');
const videos = JSON.parse(fs.readFileSync('dist/videos.json', 'utf8'));
const elements = new Map();
class Element {
  constructor() { this.handlers = {}; this.children = []; this.attrs = {}; this.dataset = {}; this.hidden = false; this.disabled = false; this.textContent = ''; this.classList = {add(){},remove(){}}; }
  addEventListener(name, fn) { (this.handlers[name] ||= []).push(fn); }
  fire(name) { return Promise.all((this.handlers[name] || []).map(fn => fn({target:this}))); }
  setAttribute(name,value) { this.attrs[name] = value; }
  querySelector(name) { return this.selectors[name]; }
  appendChild(child) { this.children.push(child); if(child.id) elements.set(child.id,child); }
  replaceChildren() { this.children = []; }
  showModal() { this.open = true; }
  close() { this.open = false; this.fire('close'); }
  focus() { this.focused = true; }
  remove() {}
}
for (const id of ['play-video','video-poster','player-error','video-status','previous-video','next-video','current-video-title','video-category','watch-youtube','youtube-mount','retry-video']) elements.set(id,new Element());
const items=videos.map((v,i)=>{
 const e=new Element();e.dataset.videoId=v.id;e.selectors={'strong':{textContent:v.title},'.playlist-copy > span':{textContent:v.category},'img':{src:v.thumbnail}};return e;
});
const document={querySelectorAll:()=>items,getElementById:id=>elements.get(id),createElement:()=>new Element(),head:new Element(),body:new Element(),activeElement:items[0]};
const players=[];
const YT={PlayerState:{PLAYING:1,PAUSED:2,BUFFERING:3,ENDED:0},Player:function(id,config){
 this.events=config.events;this.loads=[];this.loadVideoById=x=>this.loads.push(x);this.playVideo=()=>{};this.destroy=()=>{this.destroyed=true;};players.push(this);
}};
const context={document,window:{YT},location:{origin:'http://localhost:4173'},URLSearchParams,setTimeout:()=>1,clearTimeout:()=>{}};
vm.runInNewContext(fs.readFileSync('dist/video-player.js','utf8'),context);
(async()=>{
 await items[3].fire('click');
 await Promise.resolve();
 assert.equal(elements.get('current-video-title').textContent,videos[3].title);
 assert.equal(players.length,1);
 assert.match(elements.get('bmw-youtube-player').src,new RegExp(videos[3].id));
 players[0].events.onReady({target:players[0]});
 assert.equal(elements.get('play-video').hidden,true);
 await elements.get('previous-video').fire('click');
 assert.equal(players[0].loads.at(-1),videos[2].id);
 await elements.get('next-video').fire('click');
 assert.equal(players[0].loads.at(-1),videos[3].id);
 await elements.get('next-video').fire('click');
 assert.equal(players[0].loads.at(-1),videos[4].id);
 assert.equal(elements.get('current-video-title').textContent,videos[4].title);
 players[0].events.onStateChange({data:0});
 assert.equal(players[0].loads.at(-1),videos[5].id,'Ended advances to the next video');
 assert.equal(elements.get('next-video').disabled,true);
 const loads=players[0].loads.length;
 players[0].events.onStateChange({data:0});
 assert.equal(players[0].loads.length,loads,'Last video does not loop');
 players[0].events.onError({data:150});
 assert.equal(elements.get('player-error').hidden,false);
 await elements.get('retry-video').fire('click');
 await Promise.resolve();
 assert.equal(players[0].destroyed,true);
 assert.equal(players.length,2);
 assert.match(elements.get('bmw-youtube-player').src,new RegExp(videos[5].id));
 console.log('PASS: one-click playback, selected video, player initialization, previous/next, auto advance, final boundary, error and retry');
})().catch(e=>{console.error(e);process.exitCode=1;});
