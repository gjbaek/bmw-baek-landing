'use strict';
const {test} = require('node:test');
const assert = require('node:assert/strict');
const {CHANNEL_ID, parseFeed, parseApi, getLatestVideos} = require('../lib/youtube-feed.cjs');
const entry = (id, date, title = 'BMW &amp; 이야기', channel = CHANNEL_ID) => `<entry><yt:videoId>${id}</yt:videoId><yt:channelId>${channel}</yt:channelId><title>${title}</title><published>${date}</published><updated>2099-01-01T00:00:00Z</updated></entry>`;
const feed = entries => `<feed xmlns="http://www.w3.org/2005/Atom">${entries}</feed>`;
const goodFeed = feed(entry('b-wbgk1aP90', '2020-01-02T00:00:00Z'));

test('Atom feed uses upload dates, decodes titles, sorts, deduplicates and excludes foreign/invalid/future entries', () => {
  const result = parseFeed(feed([
    entry('TvuWH4ZJGFQ', '2020-01-01T00:00:00Z'),
    entry('wWzw-OQ9CvM', '2020-01-03T00:00:00Z', '<![CDATA[X3 <시승> & 출고]]>'),
    entry('b-wbgk1aP90', '2020-01-02T00:00:00Z', 'i4 &#x26; &#49464;&#45800;'),
    entry('b-wbgk1aP90', '2020-01-02T00:00:00Z'),
    entry('khu4S-4ot1Y', '2020-01-04T00:00:00Z', 'Other channel', 'UCnotours'),
    entry('KvEjml1YNdw', '2099-01-01T00:00:00Z'),
    entry('In3Z7pXPFv4', 'not a date'),
    entry('"onerror=x', '2020-01-01T00:00:00Z')
  ].join('')));
  assert.deepEqual(result.map(v => v.id), ['wWzw-OQ9CvM', 'b-wbgk1aP90', 'TvuWH4ZJGFQ']);
  assert.equal(result[0].title, 'X3 <시승> & 출고');
  assert.equal(result[1].title, 'i4 & 세단');
  assert.equal(result[2].title, 'BMW & 이야기');
  assert.equal(result[0].thumbnail, 'https://i.ytimg.com/vi/wWzw-OQ9CvM/hqdefault.jpg');
  assert.throws(() => parseFeed('<html>Sign in</html>'));
  assert.throws(() => parseFeed('<!DOCTYPE feed>' + goodFeed));
  assert.throws(() => parseFeed(goodFeed.replace('</feed>', '')));
});

test('API excludes private/foreign entries and uses videoPublishedAt', () => {
  const item = {snippet: {title: 'i4', videoOwnerChannelId: CHANNEL_ID, publishedAt: '2021-01-01T00:00:00Z'}, contentDetails: {videoId: 'b-wbgk1aP90', videoPublishedAt: '2020-01-02T00:00:00Z'}, status: {privacyStatus: 'public'}};
  const result = parseApi({items: [item, {...item, status: {privacyStatus: 'private'}}, {...item, snippet: {...item.snippet, videoOwnerChannelId: 'UCother'}}]});
  assert.equal(result.length, 1);
  assert.equal(result[0].publishedAt, '2020-01-02T00:00:00.000Z');
});

test('only the latest 12 public entries are returned', () => {
  const entries = Array.from({length: 15}, (_, i) => entry(`video${String(i).padStart(6, '0')}`, `2020-01-${String(i + 1).padStart(2, '0')}T00:00:00Z`));
  const videos = parseFeed(feed(entries.join('')));
  assert.equal(videos.length, 12);
  assert.equal(videos[0].id, 'video000014');
  assert.equal(videos.at(-1).id, 'video000003');
});

test('channel feed failure falls back to uploads feed, with a bounded request', async () => {
  const calls = [];
  const result = await getLatestVideos({apiKey: '', fetchImpl: async (url, options) => {
    calls.push(url);
    assert.equal(options.redirect, 'error');
    assert.ok(options.signal instanceof AbortSignal);
    return calls.length === 1 ? new Response('', {status: 404}) : new Response(goodFeed);
  }});
  assert.equal(calls.length, 2);
  assert.match(calls[1], /playlist_id=UUam/);
  assert.equal(result.status, 'live');
  assert.equal(result.videos[0].id, 'b-wbgk1aP90');
});

test('configured API key is used only as an upstream header; not in URLs or public data', async () => {
  const key = 'test-key-never-public';
  const data = {items: [{snippet: {title: 'i4', videoOwnerChannelId: CHANNEL_ID}, contentDetails: {videoId: 'b-wbgk1aP90', videoPublishedAt: '2020-01-02T00:00:00Z'}, status: {privacyStatus: 'public'}}]};
  const result = await getLatestVideos({apiKey: key, fetchImpl: async (url, options) => {
    assert.equal(options.headers['X-Goog-Api-Key'], key);
    assert.ok(!url.includes(key));
    return Response.json(data);
  }});
  assert.equal(result.source, 'youtube-api');
  assert.ok(!JSON.stringify(result).includes(key));
});

test('unavailable, empty and oversized sources cannot replace a valid list', async () => {
  for (const response of [() => new Response(''), () => new Response(feed('')), () => new Response('x'.repeat(256 * 1024 + 1))]) {
    await assert.rejects(getLatestVideos({apiKey: '', fetchImpl: async () => response()}), /unavailable/);
  }
});

test('HTTP handler caches live responses, does not cache fallback, handles HEAD and rejects writes', async () => {
  const handler = require('../api/videos.js');
  const originalFetch = global.fetch;
  const originalKey = process.env.YOUTUBE_API_KEY;
  delete process.env.YOUTUBE_API_KEY;
  async function request(method) {
    const result = {headers: {}, setHeader(k, v) {this.headers[k] = v;}, end(body) {this.body = body;}};
    await handler({method}, result);
    return result;
  }
  try {
    global.fetch = async () => new Response(goodFeed);
    const live = await request('GET');
    assert.equal(JSON.parse(live.body).status, 'live');
    assert.match(live.headers['Cache-Control'], /s-maxage=600/);
    assert.equal((await request('HEAD')).body, undefined);
    const blocked = await request('POST');
    assert.equal(blocked.statusCode, 405);
    global.fetch = async () => {throw new Error('network unavailable');};
    const fallback = await request('GET');
    assert.equal(fallback.headers['Cache-Control'], 'no-store');
    assert.equal(JSON.parse(fallback.body).checkedAt, null);
    for (const id of ['TvuWH4ZJGFQ', 'wWzw-OQ9CvM', 'b-wbgk1aP90']) assert.ok(JSON.parse(fallback.body).videos.some(v => v.id === id));
  } finally {
    global.fetch = originalFetch;
    if (originalKey === undefined) delete process.env.YOUTUBE_API_KEY; else process.env.YOUTUBE_API_KEY = originalKey;
  }
});
