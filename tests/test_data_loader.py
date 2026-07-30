"""Exercise the data-loader paths that only fire outside the happy local case:
   1. WORKSHOP_DATA_URL download   2. friendly failure when nothing is available."""
import sys, os, io, json, glob, shutil, tempfile, threading, functools, http.server, socketserver

sys.stdout.reconfigure(encoding="utf-8")
WS = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))   # the workshop folder

# --- pull the canonical setup cell straight out of a shipped notebook ---------
nb = json.load(io.open(os.path.join(WS, "01_pandas_for_clinical_data.ipynb"), encoding="utf-8"))
setup_src = next("".join(c["source"]) for c in nb["cells"]
                 if c["cell_type"] == "code" and "Workshop setup" in "".join(c["source"]))

# --- serve the real data dir over http, like an instructor's web space --------
handler = functools.partial(http.server.SimpleHTTPRequestHandler,
                            directory=os.path.join(WS, "data"))
socketserver.TCPServer.allow_reuse_address = True
srv = socketserver.TCPServer(("127.0.0.1", 0), handler)
port = srv.server_address[1]
threading.Thread(target=srv.serve_forever, daemon=True).start()
print(f"serving {WS}\\data on http://127.0.0.1:{port}/\n")

workdirs = []

def run_setup(url, fresh=True):
    """Run the setup cell in a FRESH empty cwd so no earlier download is visible."""
    if fresh:
        d = tempfile.mkdtemp(); workdirs.append(d); os.chdir(d)
    ns = {"__name__": "__main__"}
    os.environ["WORKSHOP_DATA_URL"] = url
    exec(compile(setup_src, "<setup>", "exec"), ns)
    return ns

fails = []

# === TEST 1: download path ====================================================
print("── TEST 1: WORKSHOP_DATA_URL download ──")
ns = run_setup(f"http://127.0.0.1:{port}/")
assert ns["WORKSHOP_DATA_URL"] == f"http://127.0.0.1:{port}/", "env var not picked up"
try:
    df = ns["load_csv"]("sepsis_timeseries.csv")
    ok = df.shape[0] > 30000 and "icustayid" in df.columns
    print(f"   {'✅' if ok else '❌'} downloaded {df.shape[0]:,} rows x {df.shape[1]} cols")
    if not ok:
        fails.append("download returned unexpected frame")
except Exception as e:
    fails.append(f"download path raised {e!r}")
    print(f"   ❌ {e!r}")

# === TEST 2: seeding is applied ==============================================
print("\n── TEST 2: seeds set by the setup cell ──")
checks = [("RANDOM_STATE", ns.get("RANDOM_STATE") == 42),
          ("RNG present", "RNG" in ns),
          ("PYTHONHASHSEED", os.environ.get("PYTHONHASHSEED") == "42")]
a = ns["np"].random.rand(3)
ns2 = run_setup(f"http://127.0.0.1:{port}/", fresh=False)
b = ns2["np"].random.rand(3)
checks.append(("np global seeded reproducibly", bool((a == b).all())))
checks.append(("RNG stream reproducible",
               bool((ns["RNG"].random(3) == ns2["RNG"].random(3)).all())))
for name, good in checks:
    print(f"   {'✅' if good else '❌'} {name}")
    if not good:
        fails.append(f"seed check failed: {name}")

# === TEST 3: friendly failure when there is nothing to load ==================
print("\n── TEST 3: no data, no URL, no Colab → friendly error ──")
ns3 = run_setup("")
try:
    ns3["load_csv"]("sepsis_timeseries.csv")
    fails.append("expected FileNotFoundError, got none")
    print("   ❌ no error raised")
except FileNotFoundError as e:
    good = "instructor" in str(e).lower()
    print(f"   {'✅' if good else '❌'} FileNotFoundError: {str(e)[:110]}…")
    if not good:
        fails.append("error message not helpful")
except Exception as e:
    fails.append(f"wrong exception type {type(e).__name__}")
    print(f"   ❌ wrong exception: {e!r}")

# === TEST 4: bad URL falls through instead of crashing =======================
print("\n── TEST 4: unreachable WORKSHOP_DATA_URL falls back gracefully ──")
ns4 = run_setup("http://127.0.0.1:1/")
try:
    ns4["load_csv"]("sepsis_timeseries.csv")
    fails.append("expected FileNotFoundError after bad URL")
    print("   ❌ no error raised")
except FileNotFoundError:
    print("   ✅ fell through to the friendly FileNotFoundError")
except Exception as e:
    fails.append(f"bad URL raised {type(e).__name__} instead of FileNotFoundError")
    print(f"   ❌ {e!r}")

srv.shutdown()
os.chdir(WS)
for d in workdirs:
    shutil.rmtree(d, ignore_errors=True)

print("\n" + "=" * 50)
print(f"{'❌ ' + str(len(fails)) + ' FAILURE(S)' if fails else '✅ ALL LOADER TESTS PASSED'}")
for f in fails:
    print("   -", f)
sys.exit(1 if fails else 0)
