import subprocess
from concurrent.futures import ThreadPoolExecutor
jobs=[
("ui/parchment.png","Seamless flat texture of aged parchment paper, warm cream and light tan color, subtle fibers, faint mottled stains and slight vignette, even lighting, no text, no objects, fills the whole image edge to edge.","1536x1024",False),
("ui/leather.png","Seamless flat texture of worn dark maroon-red leather book cover, subtle grain and scuffs, even lighting, no text, no objects, fills the whole image edge to edge.","1536x1024",False),
("ui/hand.png","A single emblem icon: a golden six-fingered hand (palm facing viewer, six fingers spread), like the embossed gold emblem on an old mysterious journal cover, flat 2D cartoon style with clean outlines and simple gold shading, centered, isolated on a fully transparent background, no text.","1024x1024",True),
("ui/icon.png","App icon: an old blue-and-white fishing trawler on a dark sea under a starry sky, inside a circular badge with a golden rope border, flat 2D cartoon style like the TV show Gravity Falls, bold outlines, isolated on a fully transparent background, no text.","1024x1024",True),
]
def run(j):
    cmd=["python3","gen.py",j[0],j[1],"--size",j[2],"--tries","4"]+(["--transparent"] if j[3] else [])
    return subprocess.run(cmd,capture_output=True,text=True)
with ThreadPoolExecutor(2) as ex:
    for r in ex.map(run,jobs): print(r.stdout.strip(), r.stderr.strip()[-200:], flush=True)
