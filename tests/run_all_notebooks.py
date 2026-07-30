"""Execute workshop notebooks in fresh kernels and report pass/fail."""
import sys, os, glob, time, io, json, traceback

sys.stdout.reconfigure(encoding="utf-8")
WS = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))   # the workshop folder
os.chdir(WS)

import nbformat
from nbclient import NotebookClient
from nbclient.exceptions import CellExecutionError

targets = sys.argv[1:] or sorted(glob.glob("*.ipynb"))
save = os.environ.get("SAVE_EXECUTED", "") == "1"

results = []
for fn in targets:
    t0 = time.time()
    try:
        nb = nbformat.read(fn, as_version=4)
        client = NotebookClient(nb, timeout=1800, kernel_name="python3",
                                allow_errors=False, resources={"metadata": {"path": WS}})
        client.execute()
        if save:
            nbformat.write(nb, fn)
        results.append((fn, "PASS", time.time() - t0, ""))
        print(f"✅ PASS  {fn}   ({time.time()-t0:.0f}s)", flush=True)
    except CellExecutionError as e:
        msg = str(e).strip().splitlines()
        tail = " | ".join(m for m in msg[-6:] if m.strip())[:600]
        results.append((fn, "FAIL", time.time() - t0, tail))
        print(f"❌ FAIL  {fn}   ({time.time()-t0:.0f}s)\n     {tail}\n", flush=True)
    except Exception as e:
        results.append((fn, "ERROR", time.time() - t0, repr(e)[:400]))
        print(f"💥 ERROR {fn}: {e!r}", flush=True)

print("\n================ SUMMARY ================")
for fn, st, dt, msg in results:
    print(f"{st:6} {dt:7.0f}s  {fn}")
bad = [r for r in results if r[1] != "PASS"]
print(f"\n{len(results)-len(bad)}/{len(results)} passed")
sys.exit(1 if bad else 0)
