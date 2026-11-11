"""Compose background review frames with unmodified runtime sprites and real UI art.

Run: python3 dev/issue-6/background_review.py
Requires Pillow, as does dev/build_assets.py.
"""
from pathlib import Path
import base64
import html
from PIL import Image, ImageDraw, ImageEnhance, ImageFont, ImageOps

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
GAME = ROOT/'game'
W, H = 1920, 1080
OUT = HERE/'background-review'
SCENES = [
    ('dock', 'Reykjavik harbour', [('stan_neutral', .25, False), ('ford_grin', .75, True)], 'Ford',
     "It's possible that the horn isn't that of a narwhal and may actually be evidence of an entirely unknown species!"),
    ('bunk', 'Boat bunk room', [('stan_neutral', .25, True), ('ford_neutral', .75, False)], 'Beanie Guy',
     "Hey kid, you're finally awake!"),
    ('horn', 'Museum horn exhibit', [('ford_finger', .75, True)], 'Ford',
     "Yes, just as I suspected! This horn is not ivory at all, and moreover, it's a right-handed helical spiral, meaning it isn't a Narwhal horn!"),
    ('sauna', 'Sauna · existing swimwear sprite', [('stan_swim_smile', .5, True)], 'Stan',
     None),
]

FONTS = GAME/'fonts'
TEXT = ImageFont.truetype(str(FONTS/'CrimsonText-Regular.ttf'), 36)
NAME = ImageFont.truetype(str(FONTS/'IMFeENsc28P.ttf'), 40)
QUICK = ImageFont.truetype(str(FONTS/'IMFeENsc28P.ttf'), 24)


def compose(scene, original):
    name, _, sprites, speaker, line = scene
    # Use actual dialogue from the sauna scene rather than introducing new story text.
    if line is None:
        import re
        script=(GAME/'script.rpy').read_text()
        segment=script[script.index('    scene bg sauna'):]
        line=re.search(r'    s(?: \w+)* "([^"]+)"', segment).group(1)
    bg = HERE/'original-backgrounds'/f'{name}.png' if original else ROOT/'dev/bg'/f'{name}.png'
    frame = ImageOps.fit(Image.open(bg).convert('RGB'), (W,H), method=Image.Resampling.LANCZOS).convert('RGBA')
    for name, x, speaking in sprites:
        im=Image.open(GAME/'images/sprites'/f'{name}.png').convert('RGBA')
        if not speaking:
            alpha=im.getchannel('A')
            rgb=ImageEnhance.Color(im.convert('RGB')).enhance(.7).point(lambda v:max(0,v-33))
            im=rgb.convert('RGBA');im.putalpha(alpha)
        frame.alpha_composite(im,(int(W*x-im.width/2),H-im.height))
    textbox=Image.open(GAME/'gui/textbox.png').convert('RGBA');top=H-46-textbox.height
    frame.alpha_composite(textbox,(0,top))
    d=ImageDraw.Draw(frame)
    source=Image.open(GAME/'gui/namebox.png').convert('RGBA')
    width=int(d.textlength(speaker,font=NAME))+80
    tag=Image.new('RGBA',(width,source.height))
    tag.paste(source.crop((0,0,40,source.height)),(0,0))
    tag.paste(source.crop((40,0,source.width-40,source.height)).resize((width-80,source.height)),(40,0))
    tag.paste(source.crop((source.width-40,0,source.width,source.height)),(width-40,0))
    frame.alpha_composite(tag,(175,top-30))
    d=ImageDraw.Draw(frame);d.text((215,top-30+source.height//2),speaker,font=NAME,fill='#f3dfae',anchor='lm',stroke_width=2,stroke_fill='#3a120f')
    lines=[];current=''
    for word in line.split():
        trial=f'{current} {word}'.strip()
        if d.textlength(trial,font=TEXT)>1470:
            lines.append(current);current=word
        else:current=trial
    lines.append(current)
    for i,line in enumerate(lines):d.text((215,top+82+i*46),line,font=TEXT,fill='#2b1d12',anchor='lt')
    d.rectangle((0,H-46,W,H),fill='#2b1410');d.line((0,H-46,W,H-46),fill='#8c6022')
    d.text((W//2,H-23),'Back   Journal   History   Skip   Auto   Save   Q.Save   Q.Load   Prefs',font=QUICK,fill='#f3dfae',anchor='mm')
    path=OUT/f'{scene[0]}-{"before" if original else "after"}.jpg'
    frame.convert('RGB').resize((1280,720),Image.Resampling.LANCZOS).save(path,quality=88,optimize=True)
    return path


def main():
    OUT.mkdir(exist_ok=True)
    pairs=[(scene,compose(scene,True),compose(scene,False)) for scene in SCENES]
    for inline in [True,False]:
        def src(p):
            return str(p) if inline else 'data:image/jpeg;base64,'+base64.b64encode(p.read_bytes()).decode()
        doc='''<!doctype html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><style>*{box-sizing:border-box}body{margin:0;font-family:var(--font-sans,system-ui);color:var(--foreground,#ddd)}section{background:var(--card,#222);border-radius:var(--radius,10px);padding:12px;margin-bottom:12px}header{display:flex;gap:10px;align-items:center;justify-content:space-between;margin-bottom:9px}h3{font-size:14px;margin:0}button{font:12px var(--font-sans,system-ui);padding:6px 10px;border:1px solid var(--border,#555);border-radius:5px;background:var(--secondary,#333);color:var(--foreground,#ddd);cursor:pointer}img{width:100%;height:auto;display:block;border-radius:4px}img[hidden]{display:none}p{font-size:13px;line-height:1.5;margin:0 0 12px;color:var(--muted-foreground,#999)}</style></head><body><p>Fresh backgrounds from dialogue and narration · No image inputs were used in generation. Existing sprites and UI are unchanged. Toggle each frame to compare the original pre-issue artwork.</p>'''
        for scene,before,after in pairs:
            doc+=f'<section><header><h3>{html.escape(scene[1])}</h3><button aria-pressed="false">Show original background</button></header><img class="after" src="{src(after)}" alt="Simplified {scene[0]} background with existing sprites"><img class="before" src="{src(before)}" alt="Original background" hidden></section>'
        doc+='''<script>document.querySelectorAll('button').forEach(b=>b.onclick=()=>{const s=b.closest('section'),original=b.getAttribute('aria-pressed')!=='true';b.setAttribute('aria-pressed',String(original));s.querySelector('.before').hidden=!original;s.querySelector('.after').hidden=original;b.textContent=original?'Show updated background':'Show original background';});</script></body></html>'''
        if not inline:doc=doc.replace('</style>','body{background:#121212;color:#eee;max-width:1100px;margin:24px auto;padding:0 16px}</style>')
        (HERE/('background-inline.html' if inline else 'selected-review.html')).write_text(doc)
    print(HERE/'selected-review.html')


if __name__=='__main__':main()
