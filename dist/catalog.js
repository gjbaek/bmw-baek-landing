'use strict';
(() => {
  const one = (selector) => document.querySelector(selector);
  const all = (selector) => [...document.querySelectorAll(selector)];
  const params = new URLSearchParams(location.search);

  // Native links remain usable without JS. Filtering only changes visibility.
  const search = one('#model-search');
  if (search) {
    const cards = all('.catalog-list .car-card');
    const filters = all('[data-filter]');
    let category = filters.some(b => b.dataset.filter === params.get('category')) ? params.get('category') : '전체';
    const normalise = text => text.normalize('NFKC').toLowerCase().replace(/\s+/g, '').replace(/엑티브/g, '액티브');
    function filter() {
      let count = 0;
      cards.forEach(card => {
        card.hidden = !(category === '전체' || category === card.dataset.category) || !normalise(card.dataset.search).includes(normalise(search.value));
        if (!card.hidden) count++;
      });
      filters.forEach(button => button.setAttribute('aria-pressed', String(button.dataset.filter === category)));
      one('#result-count').textContent = `${count}개 모델 · 파생 구성은 상세 페이지에서 확인`;
      one('.catalog-empty').hidden = count !== 0;
    }
    filters.forEach(button => button.addEventListener('click', () => { category = button.dataset.filter; filter(); }));
    search.addEventListener('input', filter);
    one('#reset-catalog').addEventListener('click', () => { category = '전체'; search.value = ''; filter(); search.focus(); });
    filter();
  }

  const consultation = one('[data-consultation-model]');
  let syncConsultationVariant = () => {};
  if (consultation) {
    const variant = one('#consult-variant');
    const exterior = one('#consult-exterior');
    const interior = one('#consult-interior');
    const timing = one('#consult-timing');
    const seats = one('#consult-seats');
    const message = one('#consult-message');
    const status = one('#consult-status');
    const copy = one('#copy-consultation');
    function refresh() {
      const lines = [`안녕하세요. ${consultation.dataset.consultationModel} 상담을 받고 싶습니다.`];
      for (const [label, field] of [['관심 트림', variant], ['좌석 구성', seats], ['희망 외장색', exterior], ['희망 실내색', interior], ['출고 희망 시기', timing]]) {
        const value = field?.value.trim().slice(0, 80);
        if (value) lines.push(`${label}: ${value}`);
      }
      lines.push('현재 가능한 조합과 구매 조건을 확인 부탁드립니다.');
      message.value = lines.join('\n');
      one('#consult-sms').href = smsHref(message.value);
      all('[data-consult-color]').forEach(button => button.setAttribute('aria-pressed', String(button.dataset.consultColor === exterior.value.trim())));
      status.textContent = '';
    }
    function applyEdition() {
      const option = variant.selectedOptions[0];
      if (option?.dataset.edition) exterior.value = option.dataset.exterior;
    }
    const requestedEdition = new URLSearchParams(location.search).get('edition');
    const editionOption = Array.from(variant.options).find(option => requestedEdition && option.dataset.edition === requestedEdition);
    if (editionOption) { variant.value = editionOption.value; applyEdition(); }
    variant.addEventListener('input', () => { applyEdition(); refresh(); });
    [exterior, interior, timing, seats].filter(Boolean).forEach(field => field.addEventListener('input', refresh));
    syncConsultationVariant = name => { variant.value = name; refresh(); };
    all('[data-consult-color]').forEach(button => button.addEventListener('click', () => {
      exterior.value = button.dataset.consultColor;
      refresh();
      status.textContent = `${exterior.value}을 상담 내용에 담았습니다.`;
      exterior.focus({preventScroll: true});
      consultation.scrollIntoView({behavior: matchMedia('(prefers-reduced-motion: reduce)').matches ? 'auto' : 'smooth', block: 'start'});
    }));
    copy.hidden = false;
    copy.addEventListener('click', async () => {
      try {
        await navigator.clipboard.writeText(message.value);
        status.textContent = '문의 내용을 복사했습니다. 카카오톡에 붙여넣어 보내주세요.';
      } catch {
        message.focus();
        message.select();
        status.textContent = '자동 복사를 사용할 수 없어 내용을 선택했습니다. 직접 복사해 주세요.';
      }
    });
    refresh();
  }

  const modelData = one('#model-data');
  if (modelData) {
    const model = JSON.parse(modelData.textContent);
    const select = one('#variant-select');
    const photo = one('#detail-image');
    let angle = 'front';
    function update(changeConsultation = false) {
      const variant = model.variants[Number(select.value)] || model.variants[0];
      photo.src = angle === 'side' ? variant.sideImage : variant.image;
      photo.alt = `${variant.name} ${angle === 'side' ? '측면' : '전면 사선'}`;
      photo.dataset.view = angle;
      one('#variant-fuel').textContent = variant.fuel;
      if (changeConsultation) syncConsultationVariant(variant.name);
      all('[data-angle]').forEach(button => button.setAttribute('aria-pressed', String(button.dataset.angle === angle)));
      all('[data-model-sms]').forEach(link => {
        link.dataset.modelSms = variant.name;
        setSMS(link);
      });
    }
    select.addEventListener('change', () => update(true));
    all('[data-angle]').forEach(button => button.addEventListener('click', () => { angle = button.dataset.angle; update(); }));
    update();
  }

  function smsHref(message) {
    const isiOS = /iPad|iPhone|iPod/.test(navigator.userAgent) || (navigator.platform === 'MacIntel' && navigator.maxTouchPoints > 1);
    return `sms:01083089819${isiOS ? '&' : '?'}body=${encodeURIComponent(message)}`;
  }
  function setSMS(link) {
    link.href = smsHref(`안녕하세요. ${link.dataset.modelSms} 모델과 구매 조건을 상담받고 싶습니다.`);
  }
  all('[data-model-sms]').forEach(setSMS);

  // Date-labelled examples remain historical examples after expiry, never “this month's offer”.
  const parts = Object.fromEntries(new Intl.DateTimeFormat('en-US', {timeZone: 'Asia/Seoul', year: 'numeric', month: '2-digit', day: '2-digit'}).formatToParts(new Date()).map(part => [part.type, part.value]));
  const today = `${parts.year}-${parts.month}-${parts.day}`;
  all('[data-promotion-period]').forEach(label => {
    if (today > label.dataset.through) {
      label.textContent = `적용 기간 종료 · ${label.dataset.period} 참고 예시입니다. 현재 조건은 상담 시 확인하세요.`;
      label.classList.add('expired');
    } else if (today < label.dataset.from) {
      label.textContent = `적용 시작 전 · ${label.dataset.period} 예정 조건입니다. 시행 여부를 확인하세요.`;
    }
  });
})();
