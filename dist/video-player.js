'use strict';
(() => {
  let items = [...document.querySelectorAll('.playlist-item')];
  if (!items.length) return;
  let videos = items.map(item => ({
    id: item.dataset.videoId,
    title: item.querySelector('strong').textContent,
    category: item.querySelector('.playlist-copy > span').textContent,
    thumbnail: item.querySelector('img').src
  }));
  const cover = document.getElementById('play-video');
  const poster = document.getElementById('video-poster');
  const errorPanel = document.getElementById('player-error');
  const status = document.getElementById('video-status');
  const previous = document.getElementById('previous-video');
  const next = document.getElementById('next-video');
  let index = 0;
  let player;
  let ready = false;
  let starting = false;
  let apiPromise;
  let generation = 0;
  let readyTimer;
  let interacted = false;
  let refreshing = false;
  let updated = false;
  const feedStatus = document.getElementById('video-feed-status');
  const dateFormatter = new Intl.DateTimeFormat('ko-KR', {timeZone: 'Asia/Seoul', year: 'numeric', month: '2-digit', day: '2-digit'});

  async function refreshVideos() {
    if (!feedStatus || refreshing || interacted || document.hidden) return;
    refreshing = true;
    try {
      const response = await fetch('/api/videos', {signal: AbortSignal.timeout(15000)});
      if (!response.ok) throw new Error('Feed unavailable');
      const data = await response.json();
      if (data.status !== 'live' || data.channelId !== 'UCam_yvB4qEmWmAWfT8uy3SQ' || !Array.isArray(data.videos)) throw new Error('Feed unavailable');
      const seen = new Set();
      const latest = data.videos.filter(video => {
        if (!/^[\w-]{11}$/.test(video.id || '') || typeof video.title !== 'string' || !video.title.trim() || seen.has(video.id)) return false;
        if (!video.publishedAt || !Number.isFinite(Date.parse(video.publishedAt)) || Date.parse(video.publishedAt) > Date.now()) return false;
        seen.add(video.id);
        return true;
      }).sort((a, b) => Date.parse(b.publishedAt) - Date.parse(a.publishedAt)).slice(0, 12).map(video => ({
        id: video.id, title: video.title.trim().slice(0, 300),
        category: `${dateFormatter.format(new Date(video.publishedAt))} 업로드`,
        thumbnail: `https://i.ytimg.com/vi/${video.id}/hqdefault.jpg`
      }));
      if (!latest.length) throw new Error('Empty feed');
      // A response arriving after a click must never interrupt playback or move keyboard focus.
      if (interacted) return;
      const list = document.querySelector('.playlist-items');
      const nodes = latest.map((video, position) => {
        const li = document.createElement('li');
        const button = document.createElement('button');
        button.className = 'playlist-item';
        button.type = 'button';
        button.dataset.videoId = video.id;
        button.dataset.videoIndex = position;
        const number = document.createElement('span');
        number.className = 'playlist-number';
        number.textContent = String(position + 1).padStart(2, '0');
        const image = document.createElement('span');
        image.className = 'playlist-image';
        const thumbnail = document.createElement('img');
        thumbnail.src = video.thumbnail;
        thumbnail.width = 480;
        thumbnail.height = 270;
        thumbnail.alt = '';
        thumbnail.loading = 'lazy';
        image.appendChild(thumbnail);
        const copy = document.createElement('span');
        copy.className = 'playlist-copy';
        const date = document.createElement('span');
        date.textContent = video.category;
        const title = document.createElement('strong');
        title.textContent = video.title;
        copy.append(date, title);
        button.append(number, image, copy);
        button.addEventListener('click', () => choose(position));
        li.appendChild(button);
        return li;
      });
      videos = latest;
      list.replaceChildren(...nodes);
      items = [...list.querySelectorAll('.playlist-item')];
      document.getElementById('video-count').textContent = `${videos.length} VIDEOS`;
      selectVideo(0);
      updated = true;
      feedStatus.textContent = '최근 업로드 순 · 채널과 자동으로 연결됩니다.';
    } catch {
      if (!interacted) feedStatus.textContent = updated
        ? '마지막으로 불러온 목록입니다. 최신 영상은 채널에서도 확인할 수 있습니다.'
        : '저장된 영상 목록입니다. 최신 영상은 채널에서 확인해 주세요.';
    } finally { refreshing = false; }
  }

  function setStatus(message) {
    status.textContent = `${message} · ${index + 1} / ${videos.length}`;
  }

  function selectVideo(selected) {
    if (selected < 0 || selected >= videos.length) return;
    index = selected;
    const video = videos[index];
    items.forEach((item, position) => item.setAttribute('aria-pressed', String(position === index)));
    poster.src = video.thumbnail;
    cover.setAttribute('aria-label', `${video.title} 재생`);
    document.getElementById('current-video-title').textContent = video.title;
    document.getElementById('video-category').textContent = video.category;
    document.getElementById('watch-youtube').href = `https://www.youtube.com/watch?v=${video.id}`;
    previous.disabled = index === 0;
    next.disabled = index === videos.length - 1;
    setStatus('선택한 영상');
  }

  function showError() {
    clearTimeout(readyTimer);
    starting = false;
    cover.hidden = true;
    cover.disabled = false;
    cover.classList.remove('is-loading');
    errorPanel.hidden = false;
    setStatus('재생을 확인해 주세요');
  }

  function loadAPI() {
    if (window.YT && window.YT.Player) return Promise.resolve();
    if (apiPromise) return apiPromise;
    apiPromise = new Promise((resolve, reject) => {
      const oldCallback = window.onYouTubeIframeAPIReady;
      const timer = setTimeout(() => reject(new Error('Player API timed out')), 15000);
      window.onYouTubeIframeAPIReady = () => {
        clearTimeout(timer);
        if (typeof oldCallback === 'function') oldCallback();
        resolve();
      };
      const oldScript = document.getElementById('youtube-api');
      if (oldScript) oldScript.remove();
      const script = document.createElement('script');
      script.id = 'youtube-api';
      script.src = 'https://www.youtube.com/iframe_api';
      script.referrerPolicy = 'strict-origin-when-cross-origin';
      script.onerror = () => { clearTimeout(timer); reject(new Error('Player API unavailable')); };
      document.head.appendChild(script);
    }).catch(error => { apiPromise = undefined; throw error; });
    return apiPromise;
  }

  async function play() {
    interacted = true;
    errorPanel.hidden = true;
    if (ready && player) {
      cover.hidden = true;
      setStatus('불러오는 중');
      player.loadVideoById(videos[index].id);
      return;
    }
    if (starting) return;
    if (player && typeof player.destroy === 'function') player.destroy();
    player = undefined;
    starting = true;
    const attempt = ++generation;
    cover.hidden = false;
    cover.disabled = true;
    cover.classList.add('is-loading');
    setStatus('플레이어를 불러오는 중');
    try {
      await loadAPI();
      if (attempt !== generation) return;
      const mount = document.getElementById('youtube-mount');
      mount.replaceChildren();
      const frame = document.createElement('iframe');
      frame.id = 'bmw-youtube-player';
      frame.title = 'BMW는 끼쟁이 YouTube 영상 플레이어';
      frame.allow = 'autoplay; encrypted-media; picture-in-picture; fullscreen';
      frame.allowFullscreen = true;
      frame.referrerPolicy = 'strict-origin-when-cross-origin';
      const params = new URLSearchParams({enablejsapi: '1', autoplay: '1', playsinline: '1', rel: '0', hl: 'ko', origin: location.origin});
      frame.src = `https://www.youtube-nocookie.com/embed/${videos[index].id}?${params}`;
      const initialVideo = videos[index].id;
      mount.appendChild(frame);
      readyTimer = setTimeout(() => { if (attempt === generation && !ready) showError(); }, 15000);
      player = new window.YT.Player(frame.id, {
        events: {
          onReady(event) {
            if (attempt !== generation) return;
            clearTimeout(readyTimer);
            ready = true;
            starting = false;
            cover.hidden = true;
            cover.disabled = false;
            cover.classList.remove('is-loading');
            if (initialVideo !== videos[index].id) event.target.loadVideoById(videos[index].id);
            else event.target.playVideo();
            setStatus('재생 준비 완료');
          },
          onStateChange(event) {
            if (attempt !== generation) return;
            if (event.data === window.YT.PlayerState.PLAYING) {
              errorPanel.hidden = true;
              setStatus('재생 중');
            } else if (event.data === window.YT.PlayerState.PAUSED) setStatus('일시 정지');
            else if (event.data === window.YT.PlayerState.BUFFERING) setStatus('불러오는 중');
            else if (event.data === window.YT.PlayerState.ENDED) {
              if (index < videos.length - 1) { selectVideo(index + 1); play(); }
              else setStatus('재생목록을 모두 보셨습니다');
            }
          },
          onError() { if (attempt === generation) showError(); }
        }
      });
    } catch { if (attempt === generation) showError(); }
  }

  function choose(selected) { selectVideo(selected); play(); }
  items.forEach((item, position) => item.addEventListener('click', () => choose(position)));
  cover.addEventListener('click', play);
  previous.addEventListener('click', () => choose(index - 1));
  next.addEventListener('click', () => choose(index + 1));
  document.getElementById('retry-video').addEventListener('click', () => {
    generation += 1;
    clearTimeout(readyTimer);
    if (player && typeof player.destroy === 'function') player.destroy();
    player = undefined;
    ready = false;
    starting = false;
    play();
  });
  if (feedStatus) {
    // Keep focused controls stable when navigating the playlist with a keyboard.
    document.querySelector('.playlist').addEventListener('focusin', () => { interacted = true; });
    refreshVideos();
    window.setInterval(refreshVideos, 10 * 60 * 1000);
    document.addEventListener('visibilitychange', () => { if (!document.hidden) refreshVideos(); });
  }
})();
