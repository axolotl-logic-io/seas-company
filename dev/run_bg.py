import subprocess, bg_prompts as B, os, sys
from concurrent.futures import ThreadPoolExecutor
EXTRA=" Keep shapes simplified and stylized like a TV cartoon background, not photorealistic."
jobs=[]
for k,p in B.BGS.items():
    out=f"bg/{k}.png"
    if os.path.exists(out): continue
    prompt=B.BGSTYLE+p+EXTRA
    jobs.append((out,prompt))
def run(j):
    cmd=["python3","gen.py",j[0],j[1],"--size","1920x1088","--tries","4"]
    return subprocess.run(cmd,capture_output=True,text=True)
with ThreadPoolExecutor(4) as ex:
    for r in ex.map(run,jobs): print(r.stdout.strip(), r.stderr.strip()[-200:], flush=True)
