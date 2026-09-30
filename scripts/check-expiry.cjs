// Exercise the real browser script with dates around the Korea-time deadline.
const fs = require('node:fs');
const vm = require('node:vm');
const assert = require('node:assert/strict');
const path = require('node:path');
const source = fs.readFileSync(path.join(__dirname, '../dist/catalog.js'), 'utf8');
for (const [instant, expected] of [
  ['2026-08-31T14:59:59Z', '적용 시작 전'],
  ['2026-08-31T15:00:00Z', '현재 조건'],
  ['2026-09-30T14:59:59Z', '현재 조건'],
  ['2026-09-30T15:00:00Z', '적용 기간 종료'],
]) {
  const label = {dataset: {from:'2026-09-01', through:'2026-09-30', period:'2026년 9월'}, textContent:'현재 조건', classList:{add(){}}};
  class FixedDate extends Date { constructor(...args) { super(...(args.length ? args : [instant])); } }
  vm.runInNewContext(source, {
    Date: FixedDate, Intl, URLSearchParams, location: {search:''},
    document: {querySelector:()=>null, querySelectorAll:selector=>selector === '[data-promotion-period]' ? [label] : []}
  });
  assert.ok(label.textContent.startsWith(expected), `${instant}: ${label.textContent}`);
}
console.log('PASS: promotion start/expiry at midnight Asia/Seoul, including month boundary.');
