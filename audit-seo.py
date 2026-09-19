"""Reproducible local implementation checklist; NOT Lighthouse or a ranking score."""
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlparse
from urllib.request import urlopen
import json, re, sys, xml.etree.ElementTree as ET
ROOT=Path(__file__).parent
class Node:
 def __init__(self,tag='',attrs=None):self.tag=tag;self.a=dict(attrs or []);self.children=[]
 def text(self):return ''.join(c if isinstance(c,str) else c.text() for c in self.children)
 def all(self,tag=None):
  out=[]
  for c in self.children:
   if isinstance(c,Node):
    if tag is None or c.tag==tag:out.append(c)
    out+=c.all(tag)
  return out
class Parser(HTMLParser):
 def __init__(self):super().__init__();self.root=Node();self.stack=[self.root]
 def handle_starttag(self,t,a):
  n=Node(t,a);self.stack[-1].children.append(n)
  if t not in ['area','base','br','col','embed','hr','img','input','link','meta','param','source','track','wbr']:self.stack.append(n)
 def handle_endtag(self,t):
  for i in range(len(self.stack)-1,0,-1):
   if self.stack[i].tag==t:self.stack=self.stack[:i];break
 def handle_data(self,d):self.stack[-1].children.append(d)
def norm(s):return re.sub(r'\s+',' ',s).strip()
def run(path,browser):
 raw=path.read_text();p=Parser();p.feed(raw);d=p.root;nodes=d.all();metas=d.all('meta');results=[]
 def add(label,passed,evidence):results.append({'check':label,'passed':bool(passed),'evidence':evidence})
 def meta(k):return [x.a.get('content','') for x in metas if x.a.get('name',x.a.get('property'))==k]
 def cls(k):return [n for n in nodes if k in n.a.get('class','').split()]
 titles=d.all('title');h1=d.all('h1');h1text=norm(h1[0].text()) if h1 else ''
 ids=[n.a['id'] for n in nodes if 'id' in n.a];links=d.all('a');imgs=d.all('img')
 canonical=[n.a.get('href','') for n in d.all('link') if n.a.get('rel')=='canonical'];url=canonical[0] if canonical else ''
 scripts=d.all('script');schema=json.loads(next(n.text() for n in scripts if n.a.get('type')=='application/ld+json'));graph=schema['@graph']
 person=next(n for n in graph if n['@type']=='Person');dealer=next(n for n in graph if n['@type']=='AutoDealer');faq=next(n for n in graph if n['@type']=='FAQPage')
 main=d.all('main')[0];body=d.all('body')[0];visible=norm(main.text())
 add('HTML5·한국어·UTF-8',raw.lower().startswith('<!doctype html>') and d.all('html')[0].a.get('lang')=='ko' and any(n.a.get('charset')=='utf-8' for n in metas),'문서 기본 언어/인코딩')
 add('고유한 페이지 제목',len(titles)==1 and all(x in titles[0].text() for x in ['BMW','백경재','한남']),titles[0].text())
 add('설명 메타데이터',len(meta('description'))==1 and 30<=len(meta('description')[0])<=180,meta('description'))
 add('상담 목적이 드러나는 단일 H1',len(h1)==1 and all(x in h1text for x in ['BMW','상담']),h1text)
 heads=[int(n.tag[1]) for n in main.all() if re.fullmatch('h[1-6]',n.tag)]
 add('제목 계층',all(b<=a+1 for a,b in zip(heads,heads[1:])),heads)
 add('모바일 viewport',len(meta('viewport'))==1 and 'width=device-width' in meta('viewport')[0] and 'initial-scale=1' in meta('viewport')[0],meta('viewport'))
 add('페이지 수집 허용 지시',not any('noindex' in m for m in meta('robots')),meta('robots'))
 add('단일 절대 canonical',len(canonical)==1 and urlparse(url).scheme=='https' and bool(urlparse(url).netloc),url+' (실제 공개 응답 검증은 별도)')
 sitemap=ET.parse(ROOT/'dist/sitemap.xml').getroot();locs=[n.text for n in sitemap.iter() if n.tag.endswith('loc')]
 add('사이트맵과 canonical 일치',url in locs,locs)
 robots=(ROOT/'dist/robots.txt').read_text()
 add('robots.txt 수집 및 사이트맵',bool(re.search(r'^Allow: /$',robots,re.M)) and 'Disallow: /' not in robots and url.rstrip('/')+'/sitemap.xml' in robots,robots.strip())
 local=[n.a[k].split('#')[0] for n in nodes for k in ['href','src'] if n.a.get(k,'').startswith('/')]
 add('로컬 리소스 존재',all((ROOT/'dist'/u.lstrip('/')).exists() for u in local),{'references':len(set(local))})
 with urlopen('http://127.0.0.1:4173/',timeout=10) as r:status=r.status
 add('로컬 HTTP 정상 응답',status==200,status)
 add('이미지 대체 텍스트 속성',all('alt' in n.a for n in imgs),{'images':len(imgs),'decorative_empty_alt_allowed':True})
 add('이미지 크기 명시',all(n.a.get('width') and n.a.get('height') for n in imgs),len(imgs))
 add('핵심 본문을 HTML로 제공',len(visible)>1000 and all(x in visible for x in ['백경재','이태원로 249','010-8308-9819']),{'text_length':len(visible)})
 anchors=[n.a.get('href','')[1:] for n in links if n.a.get('href','').startswith('#')]
 add('고유 ID·내부 앵커 연결',len(ids)==len(set(ids)) and all(a in ids for a in anchors),{'ids':len(ids),'anchors':len(anchors)})
 add('설명 있는 실제 링크',all(n.a.get('href') and (norm(n.text()) or n.a.get('aria-label') or any(c.a.get('alt') for c in n.all('img'))) for n in links),len(links))
 add('페이지·인물·전시장 구조화 데이터',all(t in [n['@type'] for n in graph] for t in ['WebSite','WebPage','Person','AutoDealer','FAQPage']),[n['@type'] for n in graph])
 add('연락처·위치·담당자 일치',person['name']=='백경재' and person['telephone']=='+82-10-8308-9819' and dealer['address']['streetAddress']=='이태원로 249' and '010-8308-9819' in visible and '이태원로 249' in visible,{'name':person['name'],'phone':person['telephone'],'address':dealer['address']})
 faqs=cls('faq-list')[0].all('details');visiblefaq=[(norm(n.all('summary')[0].text()),norm(next(x for x in n.all('div') if x.a.get('class')=='faq-answer').text())) for n in faqs]
 schemafaq=[(norm(n['name']),norm(n['acceptedAnswer']['text'])) for n in faq['mainEntity']]
 add('보이는 FAQ와 구조화 데이터 일치',visiblefaq==schemafaq and len(faqs)==5,{'visible':len(faqs),'schema':len(schemafaq)})
 add('실제 SNS 계정 연결',set(person['sameAs'])=={'https://blog.naver.com/back03278','https://www.youtube.com/@bmw_gjbaek','https://www.instagram.com/bmw_gjbaek/'},person['sameAs'])
 og=['og:title','og:description','og:url','og:image','og:image:alt']
 add('Open Graph 공유 정보',all(len(meta(k))==1 and meta(k)[0] for k in og),{k:meta(k) for k in og})
 tw=['twitter:card','twitter:title','twitter:description','twitter:image','twitter:image:alt']
 add('공유 카드 정보',all(len(meta(k))==1 and meta(k)[0] for k in tw),{k:meta(k) for k in tw})
 add('기본 로딩 최적화',all('defer' in n.a for n in scripts if n.a.get('src')) and any(n.a.get('fetchpriority')=='high' for n in imgs) and any(n.a.get('loading')=='lazy' for n in imgs) and not d.all('iframe'),'지연 JS·대표 이미지 우선·하단 이미지 lazy·초기 iframe 없음; Core Web Vitals 실측은 별도')
 add('브라우저 글자 가독성·가로 넘침',browser['minimum_supporting_font_px']>=12 and browser['body_font_px']>=16 and browser['scroll_width']==browser['viewport_width'],browser)
 assert len(results)==25
 return {'label':'자체 로컬 SEO·공유·기본 UX 구현 체크리스트','not_lighthouse':True,'scope':'출판/공개 URL·색인·검색순위·실사용 성능·콘텐츠 전문성은 점수에서 제외; 별도 필수 점검','passed':sum(x['passed'] for x in results),'total':25,'score':sum(x['passed'] for x in results)*4,'checks':results}
if __name__=='__main__':
 before=run(ROOT/'qa/before-v3/index.html',json.loads((ROOT/'qa/browser-before.json').read_text()))
 after=run(ROOT/'dist/index.html',json.loads((ROOT/'qa/browser-after.json').read_text()))
 (ROOT/'qa/seo-audit.json').write_text(json.dumps({'before':before,'after':after},ensure_ascii=False,indent=2))
 for label,result in [('Before',before),('After',after)]:
  print(label,result['score'],f"({result['passed']}/25)")
  for check in result['checks']:
   if not check['passed']:print('FAIL:',check['check'])
