"""Build the issue #6 review with real image layers and the game's dialogue art.

python3 dev/issue-6/build_review.py
Produces a standalone review.html and a local-image inline.html for T3 rendering.
"""
from pathlib import Path
import base64
import html
import json
from PIL import Image

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]


def build(inline=False):
    thumbnails = HERE/'review-assets'
    thumbnails.mkdir(exist_ok=True)

    def asset(path):
        path = Path(path)
        if path.suffix == '.png':
            thumb = thumbnails/'-'.join(path.relative_to(ROOT).parts)
            if not thumb.exists() or thumb.stat().st_mtime < path.stat().st_mtime:
                with Image.open(path) as im:
                    im.thumbnail((900, 900), Image.Resampling.LANCZOS)
                    im.save(thumb, optimize=True)
            path = thumb
        if inline:
            return str(path)
        mime = 'font/ttf' if path.suffix == '.ttf' else 'image/png'
        return f'data:{mime};base64,' + base64.b64encode(path.read_bytes()).decode()

    manifest = json.loads((HERE/'prompts.json').read_text())
    images = {'current': [ROOT/'dev/bg/dock.png', ROOT/'dev/spr/stan_neutral.png', ROOT/'dev/spr/ford_grin.png']}
    for key in manifest['directions']:
        images[key] = [HERE/key/'bg_dock.png', ROOT/'dev/spr/stan_neutral.png',
                       ROOT/'dev/spr/ford_grin.png' if key == 'a-cel' else HERE/key/'ford_grin.png']
    textbox = asset(ROOT/'game/gui/textbox.png')
    namebox = asset(ROOT/'game/gui/namebox.png')

    def scene(key):
        bg, stan, ford = map(asset, images[key])
        return f'''<div class="scene"><img class="bg" src="{bg}" alt="Reykjavik harbour"><img class="sprite stan" src="{stan}" alt="Existing Stan sprite"><img class="sprite ford" src="{ford}" alt="Ford sprite"><img class="textbox" src="{textbox}" alt=""><div class="speaker" style="background-image:url('{namebox}')">Ford</div><div class="dialogue">It's possible that the horn isn't that of a narwhal and may actually be evidence of an entirely unknown species!</div><div class="quick">Back　 Journal　 History　 Skip　 Auto　 Save　 Q.Save　 Q.Load　 Prefs</div><div class="guides" hidden><span class="safe left">STAN · 25%</span><span class="safe right">FORD · 75%</span><span class="dialogue-guide">Dialogue area</span></div></div>'''

    labels = {'current':'Current artwork', 'a-cel':'A · Quiet gouache', 'b-painted':'B · Soft painted', 'c-graphic':'C · Graphic adventure'}
    descriptions = {
        'a-cel': 'New simplified harbour with the existing Stan and Ford sprites. The proposed cel-shaded sprite generations were rejected.',
        'b-painted': 'New wash-painted harbour and softly modeled Ford, with the existing Stan sprite.',
        'c-graphic': 'New graphic harbour and Ford with stronger shadow shapes, with the existing Stan sprite.',
    }
    cards = ''
    for key in manifest['directions']:
        note = '<p class="note">Ford anatomy draft: the open hand needs six digits before use in the game.</p>' if key != 'a-cel' else ''
        cards += f'<section class="card" data-key="{key}"><h3>{labels[key]}</h3><p>{descriptions[key]}</p>{scene(key)}{note}</section>'
    options = ''.join(f'<option value="{k}">{html.escape(v)}</option>' for k,v in labels.items())
    fonts = '' if inline else f"@font-face{{font-family:Crimson;src:url({asset(ROOT/'game/fonts/CrimsonText-Regular.ttf')})}}@font-face{{font-family:Seas;src:url({asset(ROOT/'game/fonts/IMFeENsc28P.ttf')})}}"
    css = '''
*{box-sizing:border-box}body{margin:0;font-family:var(--font-sans,system-ui);color:var(--foreground,#ddd)}
p{font-size:13px;line-height:1.5;color:var(--muted-foreground,#999);margin:5px 0 12px}h3{font-size:15px;margin:0 0 5px;font-weight:600}
.card{padding:16px;border-radius:var(--radius,10px);background:var(--card,#222);margin:0 0 14px}
.scene{position:relative;aspect-ratio:16/9;overflow:hidden;container-type:inline-size;background:#b7bcc5;border-radius:4px}
.bg{width:100%;height:100%;object-fit:cover;display:block}.sprite{position:absolute;height:99.5%;width:auto;bottom:0;transform:translateX(-50%)}.stan{left:25%;filter:brightness(.87) saturate(.7)}.ford{left:75%}
.textbox{position:absolute;left:0;width:100%;bottom:4.259%}.speaker{position:absolute;left:9.11%;bottom:28.9%;font-family:Seas,Georgia,serif;font-size:2.08cqw;padding:.15em 1em;color:#f3dfae;border-radius:.3em;background-color:#6b1f1f;background-size:100% 100%;line-height:1.7}
.dialogue{position:absolute;left:11.2%;top:77.3%;width:76.56%;font-family:Crimson,Georgia,serif;font-size:1.875cqw;line-height:1.28;color:#2b1d12}
.quick{position:absolute;bottom:0;left:0;width:100%;height:4.259%;display:flex;align-items:center;justify-content:center;background:#2b1410;border-top:1px solid #8c6022;font-family:Seas,Georgia,serif;color:#f3dfae;font-size:1.25cqw;white-space:pre}
.controls{display:flex;gap:12px;flex-wrap:wrap;align-items:end;margin-bottom:12px}label{font-size:12px;display:grid;gap:5px;flex:1;min-width:140px}select{color:var(--foreground,#ddd);background:var(--secondary,#333);border:1px solid var(--border,#555);border-radius:6px;padding:8px;font:inherit}.check{display:flex;align-items:center;gap:5px;min-width:auto;flex:0 0 auto;white-space:nowrap}summary{cursor:pointer;font-size:13px;padding:4px 0 12px}details{margin-bottom:14px}.note{font-size:12px;margin:8px 0 0;color:var(--warning,#d7a953)}
.safe{position:absolute;top:4%;bottom:31%;width:34%;border:1px dashed #f3dfae;color:#fff;font:10px system-ui;padding:6px;text-shadow:0 1px 3px #000}.left{left:8%}.right{right:8%}.dialogue-guide{position:absolute;left:9%;right:9%;top:72%;bottom:6%;border:1px dashed #f3dfae;font:10px system-ui;color:#2b1d12;padding:4px}.guides{position:absolute;inset:0;pointer-events:none}
'''
    if not inline:
        css += 'body{background:#121212;color:#eee;max-width:1100px;margin:24px auto;padding:0 16px}'
    doc = '<!doctype html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><style>'+fonts+css+'</style></head><body>'
    doc += '<p>Issue #6 · Real generated images in a 1920 × 1080 composition. Same day outfits, dialogue, scale and speaker focus in every version. Stan remains the existing sprite because generation was rejected. Game assets are unchanged.</p>'+cards
    doc += '<details><summary>Current artwork and mix-and-match comparison</summary><section class="card"><div class="controls"><label>Background<select id="background">'+options+'</select></label><label>Sprites<select id="characters">'+options+'</select></label><label class="check"><input id="guide" type="checkbox"> Layout guides</label></div><div id="mixer" data-key="current">'+scene('current')+'</div><p>Change one layer at a time to assess visual hierarchy. Composition approximates the game; the standalone file embeds the game fonts.</p></section></details>'
    doc += '''<script>const originals={};document.querySelectorAll('[data-key]').forEach(card=>{originals[card.dataset.key]=Object.fromEntries(['bg','stan','ford'].map(role=>[role,card.querySelector('.'+role).getAttribute('src')]));});const mixer=document.querySelector('#mixer');function mix(){let bg=document.querySelector('#background').value,chars=document.querySelector('#characters').value;mixer.querySelector('.bg').src=originals[bg].bg;for(let role of ['stan','ford'])mixer.querySelector('.'+role).src=originals[chars][role];}document.querySelectorAll('select').forEach(s=>s.addEventListener('change',mix));document.querySelector('#guide').addEventListener('change',e=>mixer.querySelector('.guides').hidden=!e.target.checked);mix();</script></body></html>'''
    path = HERE/('inline.html' if inline else 'review.html')
    path.write_text(doc)
    print(path)


if __name__ == '__main__':
    build()
    build(inline=True)
