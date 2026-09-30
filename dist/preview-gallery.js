(() => {
  const cards = Array.from(document.querySelectorAll('[data-photo-group]'));
  const filters = Array.from(document.querySelectorAll('[data-photo-filter]'));
  const dialog = document.querySelector('#photo-dialog');
  if (!cards.length || !dialog || typeof dialog.showModal !== 'function') return;
  let visible = cards.slice();
  let active = 0;
  let opener = null;
  const result = document.querySelector('#photo-result');
  document.querySelector('.preview-filters').hidden = false;
  filters.forEach(button => button.addEventListener('click', () => {
    const group = button.dataset.photoFilter;
    cards.forEach(card => { card.hidden = group !== 'all' && card.dataset.photoGroup !== group; });
    visible = cards.filter(card => !card.hidden);
    filters.forEach(item => item.setAttribute('aria-pressed', String(item === button)));
    result.textContent = `사진 ${visible.length}장 · 사진을 누르면 크게 볼 수 있습니다.`;
  }));
  function render() {
    const card = visible[active];
    const img = document.querySelector('#photo-dialog-image');
    img.src = card.querySelector('a').href;
    img.alt = card.querySelector('img').alt;
    document.querySelector('#photo-dialog-title').textContent = card.querySelector('strong').textContent;
    document.querySelector('#photo-dialog-caption').textContent = card.querySelector('figcaption p').textContent;
    document.querySelector('#photo-dialog-counter').textContent = `${active + 1} / ${visible.length} · 글로벌 공개 이미지`;
    document.querySelector('#photo-dialog-prev').disabled = active === 0;
    document.querySelector('#photo-dialog-next').disabled = active === visible.length - 1;
  }
  cards.forEach(card => card.querySelector('a').addEventListener('click', event => {
    if (event.metaKey || event.ctrlKey || event.shiftKey || event.altKey) return;
    event.preventDefault();
    opener = event.currentTarget;
    active = visible.indexOf(card);
    render();
    dialog.showModal();
    document.documentElement.classList.add('photo-viewer-open');
    document.querySelector('#photo-dialog-close').focus();
  }));
  function move(step) { active = Math.max(0, Math.min(visible.length - 1, active + step)); render(); }
  document.querySelector('#photo-dialog-prev').addEventListener('click', () => move(-1));
  document.querySelector('#photo-dialog-next').addEventListener('click', () => move(1));
  document.querySelector('#photo-dialog-close').addEventListener('click', () => dialog.close());
  dialog.addEventListener('keydown', event => {
    if (event.key === 'ArrowLeft' || event.key === 'ArrowRight') { event.preventDefault(); move(event.key === 'ArrowLeft' ? -1 : 1); }
  });
  dialog.addEventListener('close', () => { document.documentElement.classList.remove('photo-viewer-open'); opener?.focus({preventScroll:true}); });
})();
