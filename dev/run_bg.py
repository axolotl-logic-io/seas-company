import subprocess, bg_prompts as B, os, sys
from concurrent.futures import ThreadPoolExecutor
EXTRA=" Keep shapes simplified and stylized like a TV cartoon background, not photorealistic."
REF={"pier_night":"bg/dock.png","menu":"bg/dock.png"}
jobs=[]
for k,p in B.BGS.items():
    out=f"bg/{k}.png"
    if os.path.exists(out): continue
    prompt=B.BGSTYLE+p+EXTRA
    if k in REF: prompt="Use the fishing boat in the reference image as the design reference for the boat (same hull colors and shape). "+prompt
    jobs.append((out,prompt,REF.get(k)))
def run(j):
    cmd=["python3","gen.py",j[0],j[1],"--size","1920x1088","--tries","4"]
    if j[2]: cmd+=["--ref",j[2]]
    return subprocess.run(cmd,capture_output=True,text=True)
with ThreadPoolExecutor(4) as ex:
    for r in ex.map(run,jobs): print(r.stdout.strip(), r.stderr.strip()[-200:], flush=True)
