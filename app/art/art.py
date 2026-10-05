"""Draws the game's icon as vector art and renders every size the stores and the Android project need.
Run:  python3 app/art/art.py   (needs Playwright's Chromium). Output: app/art/out and the Android mipmaps."""
import os, asyncio
HERE = os.path.dirname(os.path.abspath(__file__)); OUT = os.path.join(HERE, 'out'); os.makedirs(OUT, exist_ok=True)
RES = os.path.join(HERE, '..', 'android', 'app', 'src', 'main', 'res')
K = '#1b1436'
DEFS = '''<defs><linearGradient id="sky" x1="0" y1="0" x2="0" y2="1">
<stop offset="0" stop-color="#3c2f7a"/><stop offset=".34" stop-color="#76476b"/><stop offset=".67" stop-color="#b25e5c"/><stop offset="1" stop-color="#e3774e"/></linearGradient></defs>'''
def scene(hand=True):
    """the icon's drawing in its own 512 x 512 space, without the sky and the ground"""
    s = f'''<g stroke="{K}" stroke-width="12" stroke-linejoin="round" stroke-linecap="round">
<rect x="135" y="250" width="190" height="140" fill="#c9c4dc"/>
<path d="M110 250 L230 150 L350 250 Z" fill="#d9534f"/>
<rect x="165" y="285" width="50" height="50" rx="4" fill="{K}"/>
<rect x="250" y="300" width="45" height="90" fill="#6b5a8c"/>
<path d="M380 390 V320 L394 298 L408 320 V390 Z M422 390 V320 L436 298 L450 320 V390 Z M464 390 V320 L478 298 L492 320 V390 Z" fill="#f2c14e"/>
</g>
<g fill="#ffd94a"><rect x="171" y="291" width="13" height="13"/><rect x="196" y="291" width="13" height="13"/><rect x="171" y="316" width="13" height="13"/><rect x="196" y="316" width="13" height="13"/></g>'''
    if hand:
        s += f'''<path d="M40 560 V426 Q40 412 54 412 H58 V388 Q58 376 68 376 Q78 376 78 388 V406 H88 Q98 406 98 418 V440 H104 Q116 440 116 452 V560 Z"
 fill="#8fd14f" stroke="{K}" stroke-width="12" stroke-linejoin="round"/>'''
    return s
def icon(size, scale=1.0, cx=256, cy=256):
    """full-bleed square icon. scale < 1 shrinks the drawing around the house so a launcher mask cannot cut it"""
    hy = 256 + (380 - cy) * scale       # where the horizon lands
    t = f'translate({256 - cx * scale} {256 - cy * scale}) scale({scale})'
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{size}" height="{size}" viewBox="0 0 512 512">{DEFS}
<rect width="512" height="{hy + 1}" fill="url(#sky)"/>
<g transform="{t}"><circle cx="380" cy="330" r="90" fill="#ffe08a"/></g>
<rect y="{hy}" width="512" height="{512 - hy}" fill="#2f4a2a"/>
<g transform="{t}">{scene()}</g></svg>'''
def feature():
    """Google Play feature graphic, 1024 x 500: the scene on the left third, the name on the right"""
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="1024" height="500" viewBox="0 0 1024 500">{DEFS}
<style>@font-face{{font-family:T;src:local("M PLUS Rounded 1c ExtraBold"),local("DejaVu Sans Bold")}}text{{font-family:T,"DejaVu Sans",sans-serif;font-weight:900}}</style>
<rect width="1024" height="381" fill="url(#sky)"/>
<circle cx="360" cy="330" r="110" fill="#ffe08a"/>
<rect y="380" width="1024" height="120" fill="#2f4a2a"/>
<g transform="translate(-20 -10)">{scene()}</g>
<g text-anchor="middle" stroke="{K}" stroke-width="14" stroke-linejoin="round" paint-order="stroke" fill="#fff">
<text x="790" y="170" font-size="92">BOB'S</text><text x="790" y="262" font-size="76" fill="#ffd94a">HOUSE</text><text x="790" y="346" font-size="64">DEFENSE</text></g></svg>'''
JOBS = [('play-icon-512.png', icon(512), 512, 512), ('icon-1024.png', icon(1024), 1024, 1024), ('feature-1024x500.png', feature(), 1024, 500)]
# Android: the legacy square/round icons, and the adaptive foreground (108 dp, only the middle 66 dp is always visible)
for d, px in dict(mdpi=48, hdpi=72, xhdpi=96, xxhdpi=144, xxxhdpi=192).items():
    m = os.path.join(RES, 'mipmap-' + d)
    JOBS += [(os.path.join(m, 'ic_launcher.png'), icon(px), px, px),
             (os.path.join(m, 'ic_launcher_round.png'), icon(px, .86, 246, 272).replace('<svg ', '<svg style="border-radius:50%" '), px, px),
             (os.path.join(m, 'ic_launcher_foreground.png'), icon(px * 108 // 48, .70, 292, 282), px * 108 // 48, px * 108 // 48)]
async def main():
    from playwright.async_api import async_playwright
    async with async_playwright() as p:
        b = await p.chromium.launch(); pg = await b.new_page()
        for name, svg, w, h in JOBS:
            await pg.set_viewport_size({'width': w, 'height': h})
            await pg.set_content('<body style="margin:0;background:transparent">' + svg)
            await pg.screenshot(path=name if os.path.isabs(name) else os.path.join(OUT, name), omit_background=True)
        await b.close()
asyncio.run(main())
