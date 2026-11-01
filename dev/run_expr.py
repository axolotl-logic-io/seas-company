import subprocess, prompts as P, os
from concurrent.futures import ThreadPoolExecutor
jobs=[]
for k,d in P.STAN_EXPR.items():
    if not d: continue
    jobs.append((f"spr/stan_{k}.png", P.EXPR_EDIT.format(desc=d)+" He wears a red beanie, thick black glasses, white tank top, navy anorak, five fingers per hand.", "spr/stan_neutral.png"))
for k,d in P.FORD_EXPR.items():
    jobs.append((f"spr/ford_{k}.png", P.EXPR_EDIT.format(desc=d)+" He keeps his windswept grey hair, cleft chin, thin glasses, maroon turtleneck, navy anorak, and SIX fingers on each hand.", "spr/ford_neutral.png"))
jobs=[j for j in jobs if not os.path.exists(j[0])]
def run(j): return subprocess.run(["python3","gen.py",j[0],j[1],"--ref",j[2],"--size","1024x1536","--transparent","--tries","8"],capture_output=True,text=True)
with ThreadPoolExecutor(6) as ex:
    for r in ex.map(run,jobs): print(r.stdout.strip(), r.stderr.strip()[-200:], flush=True)
