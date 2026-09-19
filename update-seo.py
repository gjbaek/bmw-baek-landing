# -*- coding: utf-8 -*-
"""Refresh search files from the visible page. Run after changing FAQ copy or origin."""
from pathlib import Path
from html.parser import HTMLParser
import json
import re

ROOT = Path(__file__).parent
ORIGIN = 'https://bmw-baek-gyeongjae.glassy-candy-6334.chatgpt.site'

class FAQParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.items = []
        self.current = None
        self.part = None
        self.div_depth = 0
        self.faq_depth = None
    def handle_starttag(self, tag, attrs):
        if tag == 'div':
            self.div_depth += 1
            if 'faq-list' in dict(attrs).get('class', '').split(): self.faq_depth = self.div_depth
        if tag == 'details' and self.faq_depth is not None: self.current = {'question': '', 'answer': ''}
        if self.current is not None:
            if tag == 'summary': self.part = 'question'
            if tag == 'div' and dict(attrs).get('class') == 'faq-answer': self.part = 'answer'
    def handle_data(self, data):
        if self.current is not None and self.part: self.current[self.part] += data
    def handle_endtag(self, tag):
        if tag == 'div':
            if self.div_depth == self.faq_depth: self.faq_depth = None
            self.div_depth -= 1
        if tag == 'summary': self.part = None
        if tag == 'details' and self.current:
            self.items.append({key: value.strip() for key,value in self.current.items()})
            self.current = None
            self.part = None

html_path = ROOT / 'dist/index.html'
html = html_path.read_text()
parser = FAQParser()
parser.feed(html)
address = {'@type':'PostalAddress', 'streetAddress':'이태원로 249', 'addressLocality':'용산구', 'addressRegion':'서울특별시', 'addressCountry':'KR'}
schema = {
    '@context':'https://schema.org',
    '@graph':[
        {'@type':'WebSite','@id':ORIGIN+'/#website','url':ORIGIN+'/','name':'BMW 백경재 · 도이치모터스 한남 전시장','inLanguage':'ko-KR','publisher':{'@id':ORIGIN+'/#advisor'}},
        {'@type':'WebPage','@id':ORIGIN+'/#webpage','url':ORIGIN+'/','name':'BMW 백경재 대리 | 도이치모터스 한남 전시장 · 신차·시승 상담','inLanguage':'ko-KR','isPartOf':{'@id':ORIGIN+'/#website'},'mainEntity':{'@id':ORIGIN+'/#advisor'},'about':[{'@id':ORIGIN+'/#advisor'},{'@id':ORIGIN+'/#showroom'}]},
        {'@type':'Person','@id':ORIGIN+'/#advisor','name':'백경재','jobTitle':'대리 · Sales Expert','description':'BMW Korea 인증 영업직원. BMW 도이치모터스 한남 전시장에서 신차 구매와 시승 상담을 안내합니다.','telephone':'+82-10-8308-9819','email':'gyungjae.baek@deutschmotors.com','image':ORIGIN+'/assets/baek-gyeongjae.webp','url':ORIGIN+'/#advisor','worksFor':{'@type':'Organization','name':'도이치모터스','alternateName':'Deutsch Motors','url':'https://www.deutschmotors.com/'},'workLocation':{'@id':ORIGIN+'/#showroom'},'sameAs':['https://blog.naver.com/back03278','https://www.youtube.com/@bmw_gjbaek','https://www.instagram.com/bmw_gjbaek/']},
        {'@type':'AutoDealer','@id':ORIGIN+'/#showroom','name':'도이치모터스 BMW 한남 전시장','telephone':'+82-2-749-7301','address':address,'parentOrganization':{'@type':'Organization','name':'도이치모터스','url':'https://www.deutschmotors.com/'},'brand':{'@type':'Brand','name':'BMW'},'hasMap':'https://map.naver.com/p/search/도이치모터스%20BMW%20한남%20전시장'},
        {'@type':'FAQPage','@id':ORIGIN+'/#faq','inLanguage':'ko-KR','mainEntity':[{'@type':'Question','name':item['question'],'acceptedAnswer':{'@type':'Answer','text':item['answer']}} for item in parser.items]}
    ]
}
block='<script type="application/ld+json" id="structured-data">\n'+json.dumps(schema,ensure_ascii=False,separators=(',',':')).replace('</','<\\/')+'\n</script>'
html=re.sub(r'<script type="application/ld\+json" id="structured-data">[\s\S]*?</script>\n?', '', html)
html=html.replace('</head>',block+'\n</head>')
html=re.sub(r'(<link rel="canonical" href=")[^"]+',r'\g<1>'+ORIGIN+'/',html)
html=re.sub(r'(<meta property="og:url" content=")[^"]+',r'\g<1>'+ORIGIN+'/',html)
html=re.sub(r'(<meta (?:property="og:image"|name="twitter:image") content=")[^"]+',r'\g<1>'+ORIGIN+'/assets/baek-gyeongjae.webp',html)
html_path.write_text(html)
privacy_path = ROOT / 'dist/privacy.html'
if privacy_path.exists():
    privacy = re.sub(r'(<link rel="canonical" href=")[^"]+',r'\g<1>'+ORIGIN+'/privacy.html',privacy_path.read_text())
    privacy_path.write_text(privacy)
(ROOT/'dist/robots.txt').write_text('User-agent: *\nAllow: /\n\nSitemap: '+ORIGIN+'/sitemap.xml\n')
(ROOT/'dist/sitemap.xml').write_text('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"><url><loc>'+ORIGIN+'/</loc></url></urlset>\n')
(ROOT/'dist/llms.txt').write_text('# BMW 백경재 — 도이치모터스 한남 전시장\n\n> 백경재 대리의 BMW 신차 구매 및 시승 상담 안내 페이지. BMW Korea와 도이치모터스 기업 공식 사이트와 별도로 운영됩니다.\n\n## 상담 담당자\n- 이름: 백경재\n- 직책: 대리, Sales Expert\n- 소속: 도이치모터스 BMW 한남 전시장\n- 자격: BMW Korea 인증 영업직원 (제공된 명함 기준)\n- 휴대전화: 010-8308-9819\n- 이메일: gyungjae.baek@deutschmotors.com\n\n## 전시장\n- 주소: 서울특별시 용산구 이태원로 249\n- 전시장 전화: 02-749-7301\n\n## 페이지\n- [상담 안내]('+ORIGIN+'/): 모델 상담, 담당자, 전시장 안내 및 자주 묻는 질문\n- [카카오톡 상담](https://open.kakao.com/o/stXSvxki): 백경재의 오픈채팅 상담\n- [네이버 블로그](https://blog.naver.com/back03278): 백경재의 블로그\n- [인스타그램](https://www.instagram.com/bmw_gjbaek/): 백경재의 인스타그램\n- [BMW는 끼쟁이](https://www.youtube.com/@bmw_gjbaek): 백경재의 유튜브 채널\n- [BMW Korea](https://www.bmw.co.kr/ko/index.html): 공식 모델 정보\n- [도이치모터스](https://www.deutschmotors.com/): 공식 딜러사 정보\n\n## 정보 범위\nBMW 5시리즈, X3, i5를 포함한 모델 상담. 가격, 프로모션, 재고, 시승 가능 여부, 출고 일정은 고정된 정보가 아니며 상담 시점에 확인이 필요합니다.\n\n## 자주 묻는 질문\n'+''.join('\n### '+i['question']+'\n'+i['answer']+'\n' for i in parser.items))
print(f'Updated schema, canonical, robots, sitemap and llms.txt. FAQ entries: {len(parser.items)}')
