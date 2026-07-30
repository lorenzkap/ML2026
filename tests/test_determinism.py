"""Run every notebook twice in fresh kernels and prove the printed numbers are identical.
This is the check behind the promise 'everyone in the room gets the same results'."""
import sys, os, io, glob, re

sys.stdout.reconfigure(encoding="utf-8")
WS = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))   # the workshop folder
os.chdir(WS)

import nbformat
from nbclient import NotebookClient

# volatile things that legitimately differ between runs and are not results
NOISE = re.compile(
    r"(0x[0-9a-fA-F]{6,}"                       # object addresses
    r"|\d+\.\d+ ?s\b|\d+ ?ms\b|\d+:\d\d<"       # timings / tqdm
    r"|it/s|s/it"
    r"|Wall time.*|CPU times.*"
    r"|at 0x\w+)")


def _strip_timings(t):
    """A results table with a `fit_seconds` column contains wall-clock times, which of course
    vary run to run. Blank the LAST number on each row of such a table; the metrics stay compared."""
    if "fit_seconds" not in t:
        return t
    return "\n".join(re.sub(r"[\d.]+\s*$", "<time>", ln) if re.search(r"\d\s+[\d.]+\s*$", ln) else ln
                     for ln in t.splitlines())


def text_outputs(nb):
    """Return one normalised text blob per cell.

    Consecutive stdout writes are merged: the kernel batches stream messages on a timer, so the
    SAME print statements legitimately arrive as one output object on one run and two on the next.
    Comparing the concatenated text is what actually tests reproducibility."""
    out = []
    for i, c in enumerate(nb.cells):
        if c.cell_type != "code":
            continue
        parts = []
        for o in c.get("outputs", []):
            kind = o.get("output_type")
            if kind == "stream":
                t = o.get("text", "")
            elif "data" in o:
                t = "".join(o["data"].get("text/plain", ""))
            else:
                t = ""
            if t:
                # tag non-stream outputs so a stream and a repr can never silently merge
                parts.append(t if kind == "stream" else "\x00repr\x00" + t)
        if parts:
            blob = "".join(parts)
            out.append((i, _strip_timings(NOISE.sub("<noise>", blob))))
    return out


def run_once(fn):
    nb = nbformat.read(fn, as_version=4)
    NotebookClient(nb, timeout=1800, kernel_name="python3",
                   resources={"metadata": {"path": WS}}).execute()
    return text_outputs(nb)


targets = sys.argv[1:] or sorted(glob.glob("*.ipynb"))
bad = []
for fn in targets:
    a, b = run_once(fn), run_once(fn)
    if len(a) != len(b):
        bad.append((fn, f"different number of outputs: {len(a)} vs {len(b)}"))
        print(f"❌ {fn}: {len(a)} vs {len(b)} outputs", flush=True)
        continue
    diffs = [(ci, x, y) for (ci, x), (_, y) in zip(a, b) if x != y]
    if diffs:
        bad.append((fn, f"{len(diffs)} differing output(s), first in cell {diffs[0][0]}"))
        print(f"❌ {fn}: {len(diffs)} differing output(s)", flush=True)
        ci, x, y = diffs[0]
        print(f"     cell {ci}\n     run1: {x[:220]!r}\n     run2: {y[:220]!r}", flush=True)
    else:
        print(f"✅ {fn}: {len(a)} outputs identical across two fresh kernels", flush=True)

print("\n" + "=" * 60)
print(f"{len(targets)-len(bad)}/{len(targets)} notebooks are bit-identical on re-run")
for fn, why in bad:
    print(f"   ❌ {fn}: {why}")
sys.exit(1 if bad else 0)
