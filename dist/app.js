'use strict';
(() => {
  const phone = '01083089819';
  const smsUrl = (message) => {
    const isiOS = /iPad|iPhone|iPod/.test(navigator.userAgent) || (navigator.platform === 'MacIntel' && navigator.maxTouchPoints > 1);
    return `sms:${phone}${isiOS ? '&' : '?'}body=${encodeURIComponent(message)}`;
  };
  document.querySelectorAll('[data-sms]').forEach(link => { link.href = smsUrl(link.dataset.sms); });
  const familyChoices = [...document.querySelectorAll('[data-family]')];
  const familyPanel = document.getElementById('family-panel');
  const modelOptions = [...document.querySelectorAll('.family-options [data-model]')];
  let activeFamily = null;
  function closeFamily() {
    familyPanel.hidden = true;
    familyChoices.forEach(button => button.setAttribute('aria-expanded', 'false'));
    const previousFamily = activeFamily;
    activeFamily = null;
    return previousFamily;
  }
  familyChoices.forEach(button => button.addEventListener('click', () => {
    const wasOpen = activeFamily === button;
    closeFamily();
    if (wasOpen) return;
    activeFamily = button;
    button.setAttribute('aria-expanded', 'true');
    document.getElementById('family-label').textContent = `${button.dataset.familyLabel} 모델`;
    modelOptions.forEach(model => { model.hidden = model.dataset.category !== button.dataset.family; });
    familyPanel.hidden = false;
  }));
  document.getElementById('close-family').addEventListener('click', () => {
    const previous = closeFamily();
    if (previous) previous.focus({preventScroll: true});
  });
  const dialog = document.getElementById('consult-dialog');
  let trigger = null;
  document.querySelectorAll('[data-model]').forEach(button => button.addEventListener('click', () => {
    trigger = button;
    const model = button.dataset.model;
    document.getElementById('consult-title').textContent = `${model} 상담`;
    document.getElementById('model-sms').href = smsUrl(`안녕하세요, 백경재 대리님. ${model} 구매 상담을 받고 싶습니다.`);
    dialog.showModal();
    document.body.classList.add('dialog-open');
  }));
  document.querySelector('.dialog-close').addEventListener('click', () => dialog.close());
  dialog.addEventListener('click', event => {
    if (event.target !== dialog) return;
    const rect = dialog.getBoundingClientRect();
    if (event.clientX < rect.left || event.clientX > rect.right || event.clientY < rect.top || event.clientY > rect.bottom) dialog.close();
  });
  dialog.addEventListener('close', () => {
    document.body.classList.remove('dialog-open');
    if (trigger) trigger.focus({preventScroll: true});
  });
  const quickBar = document.querySelector('.quick-contact');
  if ('IntersectionObserver' in window) {
    const observer = new IntersectionObserver(entries => {
      quickBar.classList.toggle('visible', !entries[0].isIntersecting);
    }, {threshold: 0});
    observer.observe(document.querySelector('.hero-actions'));
  } else { quickBar.classList.add('visible'); }
  let toastTimer;
  const showToast = text => {
    const toast = document.getElementById('toast');
    clearTimeout(toastTimer);
    toast.textContent = text;
    toast.classList.add('shown');
    toastTimer = setTimeout(() => toast.classList.remove('shown'), 4500);
  };
  document.getElementById('copy-address').addEventListener('click', async () => {
    try {
      await navigator.clipboard.writeText('서울특별시 용산구 이태원로 249, 도이치모터스 BMW 한남 전시장');
      showToast('전시장 주소를 복사했습니다.');
    } catch {
      showToast('복사할 수 없습니다. 화면의 주소를 길게 눌러 복사해 주세요.');
    }
  });
})();
