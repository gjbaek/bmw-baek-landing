'use strict';

const {CHANNEL_ID, REFRESH_SECONDS, getLatestVideos} = require('../lib/youtube-feed.cjs');
const savedVideos = require('../dist/videos.json');

module.exports = async function handler(request, response) {
  response.setHeader('Content-Type', 'application/json; charset=utf-8');
  response.setHeader('X-Content-Type-Options', 'nosniff');
  if (!['GET', 'HEAD'].includes(request.method)) {
    response.setHeader('Allow', 'GET, HEAD');
    response.setHeader('Cache-Control', 'no-store');
    response.statusCode = 405;
    response.end(JSON.stringify({error: 'Method not allowed'}));
    return;
  }
  let result;
  try {
    result = await getLatestVideos();
    response.setHeader('Cache-Control', `public, max-age=0, s-maxage=${REFRESH_SECONDS}, stale-while-revalidate=60`);
  } catch {
    // A failed fetch must not replace good browser data or be cached as a fresh result.
    response.setHeader('Cache-Control', 'no-store');
    result = {status: 'fallback', source: 'saved', channelId: CHANNEL_ID, checkedAt: null, videos: savedVideos};
  }
  response.statusCode = 200;
  response.end(request.method === 'HEAD' ? undefined : JSON.stringify(result));
};
