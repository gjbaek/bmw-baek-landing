# -*- coding: utf-8 -*-
"""Build a local OFL font subset from all shipped copy; run after content edits."""
from pathlib import Path
from urllib.request import urlopen
from concurrent.futures import ThreadPoolExecutor
from fontTools import subset
from fontTools.ttLib import TTFont
import re

ROOT = Path(__file__).resolve().parents[1]
DIST = ROOT / 'dist'
CACHE = ROOT / 'research/fonts'
OUT = DIST / 'assets/fonts'
WEIGHTS = {400: 'Regular', 500: 'Medium', 600: 'SemiBold', 700: 'Bold', 800: 'ExtraBold'}


def build_fonts():
    CACHE.mkdir(parents=True, exist_ok=True)
    OUT.mkdir(parents=True, exist_ok=True)
    # Include JSON/JS so text revealed by controls and later CMS fields is covered.
    texts = [p.read_text() for folder in [DIST, ROOT / 'data'] for p in folder.rglob('*')
             if p.suffix in {'.html', '.json', '.js'}]
    codepoints = set(range(32, 127)) | {ord(c) for c in ''.join(texts)}

    def fetch(weight_name):
        weight, name = weight_name
        file = CACHE / f'{name}.woff2'
        if not file.exists():
            url = f'https://cdn.jsdelivr.net/gh/projectnoonnu/pretendard@1.0/Pretendard-{name}.woff2'
            with urlopen(url, timeout=40) as response:
                file.write_bytes(response.read())
        return weight, name, file

    original_size = 0
    for weight, name, source in ThreadPoolExecutor(max_workers=5).map(fetch, WEIGHTS.items()):
        font = TTFont(source)
        original_size += source.stat().st_size
        options = subset.Options()
        options.flavor = 'woff2'
        options.name_IDs = ['*']
        options.name_legacy = True
        options.name_languages = ['*']
        subsetter = subset.Subsetter(options=options)
        subsetter.populate(unicodes=codepoints)
        subsetter.subset(font)
        # The original's OFL reserves its font name, so rename the modified font.
        for record in font['name'].names:
            if record.nameID in {1, 3, 4, 6, 16, 17}:
                if record.nameID in {1, 16}:
                    value = 'Hannam Sans'
                elif record.nameID == 17:
                    value = name
                elif record.nameID == 6:
                    value = f'HannamSans-{name}'
                else:
                    value = f'Hannam Sans {name}'
                record.string = value.encode(record.getEncoding())
        font.flavor = 'woff2'
        font.save(OUT / f'hannam-{weight}.woff2')
        font.close()

    license_file = OUT / 'OFL.txt'
    if not license_file.exists():
        with urlopen('https://raw.githubusercontent.com/orioncactus/pretendard/main/LICENSE', timeout=40) as response:
            license_file.write_bytes(response.read())
    (OUT / 'README.txt').write_text('Hannam Sans: site-specific subset of Pretendard.\n'
        'Original: https://github.com/orioncactus/pretendard\n'
        'Modified by subsetting and renaming. Distributed under SIL OFL 1.1; see OFL.txt.\n'
        'Rebuild with scripts/subset-fonts.py after changing site text.\n')
    css_path = DIST / 'styles.css'
    css = re.sub(r'@font-face\{[^}]*\}\s*', '', css_path.read_text())
    css = css.replace('font-family:Pretendard,', 'font-family:"Hannam Sans",')
    faces = ''.join(f'@font-face{{font-family:"Hannam Sans";src:url("/assets/fonts/hannam-{w}.woff2") format("woff2");font-weight:{w};font-display:swap}}\n' for w in WEIGHTS)
    css_path.write_text(faces + css)
    total = sum(p.stat().st_size for p in OUT.glob('*.woff2'))
    print(f'Fonts: {original_size:,} → {total:,} bytes ({100 * (1 - total/original_size):.1f}% smaller); {len(codepoints)} codepoints requested.')


if __name__ == '__main__':
    build_fonts()
