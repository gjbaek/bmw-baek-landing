'use strict';
// Refresh the initial HTML snapshot from the saved list, preserving no-JS playback links.
const fs = require('node:fs');
const path = require('node:path');
const root = path.resolve(__dirname, '..');
const videos = require('../dist/videos.json');
const escape = value => String(value).replace(/[&<>"']/g, c => ({'&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;'}[c]));
const date = new Intl.DateTimeFormat('ko-KR', {timeZone: 'Asia/Seoul', year: 'numeric', month: '2-digit', day: '2-digit'});
const label = video => video.publishedAt ? `${date.format(new Date(video.publishedAt))} 업로드` : video.category;
let html = fs.readFileSync(path.join(root, 'dist/index.html'), 'utf8');
const items = videos.map((video, index) => `<li><button class="playlist-item" type="button" data-video-index="${index}" data-video-id="${escape(video.id)}" aria-pressed="${index === 0}"><span class="playlist-number">${String(index + 1).padStart(2, '0')}</span><span class="playlist-image"><img src="${escape(video.thumbnail)}" width="480" height="270" alt="" loading="lazy">${video.duration ? `<span>${escape(video.duration)}</span>` : ''}</span><span class="playlist-copy"><span>${escape(label(video))}</span><strong>${escape(video.title)}</strong></span></button></li>`).join('');
html = html.replace(/<ol class="playlist-items">[\s\S]*?<\/ol>/, `<ol class="playlist-items">${items}</ol>`)
  .replace(/(id="play-video"[^>]*aria-label=")[^"]+/, (_, before) => `${before}${escape(videos[0].title)} 재생`)
  .replace(/(id="video-poster" src=")[^"]+/, (_, before) => `${before}${escape(videos[0].thumbnail)}`)
  .replace(/(<h3 id="current-video-title">)[\s\S]*?(<\/h3>)/, (_, before, after) => `${before}${escape(videos[0].title)}${after}`)
  .replace(/(<p id="video-category">)[\s\S]*?(<\/p>)/, (_, before, after) => `${before}${escape(label(videos[0]))}${after}`)
  .replace(/(id="watch-youtube" href=")[^"]+/, `$1https://www.youtube.com/watch?v=${videos[0].id}`)
  .replace(/(<span id="video-count">)[^<]+/, `$1${videos.length} VIDEOS`)
  .replace(/(<span id="video-status"[^>]*>)[^<]+/, `$1선택한 영상 1 / ${videos.length}`);
fs.writeFileSync(path.join(root, 'dist/index.html'), html);
console.log(`Rendered ${videos.length} saved videos.`);
