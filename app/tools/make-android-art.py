# Makes every Android and Google Play graphic from the 1024-pixel app icon (the one make-icon.py draws).
# Usage: python3 app/tools/make-android-art.py   (needs Pillow)
import os
from PIL import Image, ImageDraw, ImageFont
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.join(HERE, '..', '..')
SRC = os.path.join(ROOT, 'app', 'ios', 'App', 'App', 'Assets.xcassets', 'AppIcon.appiconset', 'AppIcon-512@2x.png')
RES = os.path.join(ROOT, 'app', 'android', 'app', 'src', 'main', 'res'); STORE = os.path.join(ROOT, 'docs', 'play-store-assets')
icon = Image.open(SRC).convert('RGB'); S = icon.width

def stage(w, h, scale, cx, cy):
    """the icon at `scale`, centred on (cx, cy) of a w x h canvas, with its sky and ground carried on to the edges"""
    n = round(S * scale); small = icon.resize((n, n), Image.LANCZOS)
    x0, y0 = round(cx - n / 2), round(cy - n / 2)
    edge = small.crop((1, 0, 2, n))                       # one column of sky, horizon and ground
    out = Image.new('RGB', (w, h))
    for y in range(h): out.paste(edge.getpixel((0, min(max(y - y0, 0), n - 1))), (0, y, w, y + 1))
    out.paste(small, (x0, y0)); return out

# launcher icons: the plain square, a round one, and the adaptive foreground (108 dp, of which only the middle 66 dp is always visible)
for d, px in dict(mdpi=48, hdpi=72, xhdpi=96, xxhdpi=144, xxxhdpi=192).items():
    m = os.path.join(RES, 'mipmap-' + d); f = px * 108 // 48
    icon.resize((px, px), Image.LANCZOS).save(os.path.join(m, 'ic_launcher.png'))
    big = stage(px * 4, px * 4, px * 4 * .84 / S, px * 2, px * 2); mask = Image.new('L', big.size, 0); ImageDraw.Draw(mask).ellipse((0, 0, big.width - 1, big.height - 1), fill=255)
    big.putalpha(mask); big.resize((px, px), Image.LANCZOS).save(os.path.join(m, 'ic_launcher_round.png'))
    stage(f, f, f * .64 / S, f / 2, f / 2).save(os.path.join(m, 'ic_launcher_foreground.png'))

# Google Play: 512 icon (32-bit PNG), 1024 icon, and the 1024 x 500 feature graphic (24-bit, no alpha)
os.makedirs(STORE, exist_ok=True)
icon.resize((512, 512), Image.LANCZOS).convert('RGBA').save(os.path.join(STORE, 'icon-512.png'))
icon.save(os.path.join(STORE, 'icon-1024.png'))
fg = stage(1024, 500, 500 / S, 262, 250); d = ImageDraw.Draw(fg)
def font(sz):
    for p in ('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', '/System/Library/Fonts/Supplemental/Arial Bold.ttf'):
        if os.path.exists(p): return ImageFont.truetype(p, sz)
    return ImageFont.load_default()
for text, y, sz, col in (("BOB'S", 120, 96, '#ffffff'), ('HOUSE', 222, 80, '#ffd94a'), ('DEFENSE', 312, 66, '#ffffff')):
    d.text((775, y), text, font=font(sz), fill=col, anchor='mm', stroke_width=9, stroke_fill='#1b1436')
fg.save(os.path.join(STORE, 'feature-graphic-1024x500.png'))
print('done')
