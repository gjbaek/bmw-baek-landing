'use strict';

const CHANNEL_ID = 'UCam_yvB4qEmWmAWfT8uy3SQ';
const UPLOADS_ID = 'UUam_yvB4qEmWmAWfT8uy3SQ';
const LIMIT = 12;
const REFRESH_SECONDS = 600;

function normalizeVideos(videos) {
  const seen = new Set();
  return videos.filter(video => {
    if (!/^[\w-]{11}$/.test(video.id || '') || typeof video.title !== 'string' || !video.title.trim()) return false;
    if (!video.publishedAt || !Number.isFinite(Date.parse(video.publishedAt))) return false;
    if (Date.parse(video.publishedAt) > Date.now() || seen.has(video.id)) return false;
    seen.add(video.id);
    return true;
  }).sort((a, b) => Date.parse(b.publishedAt) - Date.parse(a.publishedAt)).slice(0, LIMIT).map(video => ({
    id: video.id,
    title: video.title.trim().slice(0, 300),
    publishedAt: new Date(video.publishedAt).toISOString(),
    category: '채널 영상',
    thumbnail: `https://i.ytimg.com/vi/${video.id}/hqdefault.jpg`
  }));
}

function xmlText(value) {
  if (value.startsWith('<![CDATA[') && value.endsWith(']]>')) return value.slice(9, -3);
  const entities = {amp: '&', lt: '<', gt: '>', quot: '"', apos: "'"};
  return value.replace(/&(amp|lt|gt|quot|apos|#\d+|#x[\da-f]+);/gi, (match, entity) => {
    if (entities[entity]) return entities[entity];
    const number = entity[1].toLowerCase() === 'x' ? parseInt(entity.slice(2), 16) : parseInt(entity.slice(1), 10);
    return number > 0 && number <= 0x10ffff ? String.fromCodePoint(number) : '';
  });
}

function parseFeed(xml) {
  // Read only YouTube's small, fixed Atom field set. Never evaluate XML/HTML or resolve entities.
  if (!/<feed\s/.test(xml) || !/<\/feed>\s*$/.test(xml) || /<!DOCTYPE|<!ENTITY/i.test(xml)) throw new Error('Invalid feed');
  const field = (entry, tag) => xmlText(entry.match(new RegExp(`<${tag}>([\\s\\S]*?)</${tag}>`))?.[1]?.trim() || '');
  const videos = [...xml.matchAll(/<entry>([\s\S]*?)<\/entry>/g)].map(([, entry]) => ({
    id: field(entry, 'yt:videoId'),
    channelId: field(entry, 'yt:channelId'),
    title: field(entry, 'title'),
    publishedAt: field(entry, 'published')
  })).filter(video => video.channelId === CHANNEL_ID);
  return normalizeVideos(videos);
}

function parseApi(data) {
  return normalizeVideos((data.items || []).filter(item =>
    item.snippet?.videoOwnerChannelId === CHANNEL_ID && item.status?.privacyStatus === 'public'
  ).map(item => ({
    id: item.contentDetails?.videoId,
    title: item.snippet?.title,
    // The upload date, not the date the item was added to a playlist.
    publishedAt: item.contentDetails?.videoPublishedAt
  })));
}

async function readResponse(url, fetchImpl, headers = {}) {
  const response = await fetchImpl(url, {
    headers: {'User-Agent': 'BMWgjbaek/1.0 (+https://www.bmwgjbaek.com)', ...headers},
    signal: AbortSignal.timeout(4000),
    redirect: 'error'
  });
  if (!response.ok) throw new Error('Upstream unavailable');
  const reader = response.body.getReader();
  const chunks = [];
  let size = 0;
  while (true) {
    const {value, done} = await reader.read();
    if (done) break;
    size += value.byteLength;
    if (size > 256 * 1024) { await reader.cancel(); throw new Error('Response too large'); }
    chunks.push(value);
  }
  return Buffer.concat(chunks).toString('utf8');
}

async function getLatestVideos({fetchImpl = fetch, apiKey = process.env.YOUTUBE_API_KEY} = {}) {
  const sources = [];
  if (apiKey) {
    const params = new URLSearchParams({part: 'snippet,contentDetails,status', playlistId: UPLOADS_ID, maxResults: '15'});
    sources.push({url: `https://www.googleapis.com/youtube/v3/playlistItems?${params}`, headers: {'X-Goog-Api-Key': apiKey}, parse: text => parseApi(JSON.parse(text)), name: 'youtube-api'});
  }
  sources.push(
    {url: `https://www.youtube.com/feeds/videos.xml?channel_id=${CHANNEL_ID}`, parse: parseFeed, name: 'youtube-feed'},
    {url: `https://www.youtube.com/feeds/videos.xml?playlist_id=${UPLOADS_ID}`, parse: parseFeed, name: 'youtube-feed'}
  );
  for (const source of sources) {
    try {
      const videos = source.parse(await readResponse(source.url, fetchImpl, source.headers));
      if (videos.length) return {status: 'live', source: source.name, channelId: CHANNEL_ID, checkedAt: new Date().toISOString(), videos};
    } catch { /* Try the next official source; do not log API credentials or upstream bodies. */ }
  }
  throw new Error('YouTube sources unavailable');
}

module.exports = {CHANNEL_ID, REFRESH_SECONDS, parseFeed, parseApi, getLatestVideos};
