"""Exercise the Colab-ONLY branches of the setup cell by injecting a fake `google.colab`.

This is a simulation, not the real Colab. It proves the code paths behave; it cannot prove
Google's UI renders. Covers:
  A. Drive connected  -> upload once, file cached to Drive, second notebook reads it from Drive
  B. Drive declined   -> falls back to a plain per-session upload, still works
  C. Drive connected + file already cached -> no upload prompt at all (the 2nd-notebook case)
"""
import sys, os, io, json, types, shutil, tempfile

sys.stdout.reconfigure(encoding="utf-8")
WS = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))   # the workshop folder
REAL_CSV = os.path.join(WS, "data", "sepsis_timeseries.csv")

nb = json.load(io.open(os.path.join(WS, "01_pandas_for_clinical_data.ipynb"), encoding="utf-8"))
SETUP = next("".join(c["source"]) for c in nb["cells"]
             if c["cell_type"] == "code" and "Workshop setup" in "".join(c["source"]))

fails = []
state = {}


def install_fake_colab(drive_ok, drive_root, upload_src):
    """Put a fake google.colab on sys.modules before the setup cell imports it."""
    for m in [m for m in sys.modules if m.startswith("google")]:
        del sys.modules[m]

    google = types.ModuleType("google"); google.__path__ = []
    colab = types.ModuleType("google.colab"); colab.__path__ = []

    drive_mod = types.ModuleType("google.colab.drive")
    def mount(path, **kw):
        state["mount_called"] = state.get("mount_called", 0) + 1
        if not drive_ok:
            raise RuntimeError("user cancelled Drive authorisation")
        os.makedirs(os.path.join(drive_root, "MyDrive"), exist_ok=True)
    drive_mod.mount = mount

    files_mod = types.ModuleType("google.colab.files")
    def upload():
        state["upload_called"] = state.get("upload_called", 0) + 1
        dest = os.path.basename(upload_src)
        shutil.copy(upload_src, dest)          # Colab drops the file into cwd
        return {dest: b""}
    files_mod.upload = upload

    colab.drive, colab.files = drive_mod, files_mod
    google.colab = colab
    sys.modules.update({"google": google, "google.colab": colab,
                        "google.colab.drive": drive_mod, "google.colab.files": files_mod})


def run_setup():
    ns = {"__name__": "__main__"}
    exec(compile(SETUP, "<setup>", "exec"), ns)
    return ns


def check(label, cond):
    print(f"   {'✅' if cond else '❌'} {label}")
    if not cond:
        fails.append(label)


os.environ["WORKSHOP_DATA_URL"] = ""       # force the upload path, not the download path
tmp_root = tempfile.mkdtemp()
drive_root = os.path.join(tmp_root, "content", "drive")
CACHE = os.path.join(drive_root, "MyDrive", "sepsis_workshop_data")

# ---------------------------------------------------------------- A: Drive connected
print("── A: Colab + Drive connected → upload once, cache to Drive ──")
os.chdir(tempfile.mkdtemp())
state.clear()
install_fake_colab(True, drive_root, REAL_CSV)
ns = run_setup()
# redirect the hard-coded /content/drive path at our sandbox
ns["_drive_cache"].__globals__["os"] = os
src = SETUP.replace('"/content/drive"', f'r"{drive_root}"') \
           .replace('"/content/drive/MyDrive/sepsis_workshop_data"', f'r"{CACHE}"')
ns = {"__name__": "__main__"}; exec(compile(src, "<setup>", "exec"), ns)

check("_in_colab() is True", ns["_in_colab"]() is True)
df = ns["load_csv"]("sepsis_timeseries.csv")
check("upload prompt was used exactly once", state.get("upload_called") == 1)
check("Drive was mounted", state.get("mount_called", 0) >= 1)
check(f"loaded {df.shape[0]:,} rows", df.shape[0] == 37704)
check("file was cached into the Drive folder",
      os.path.exists(os.path.join(CACHE, "sepsis_timeseries.csv")))

# ------------------------------------------- C: a SECOND notebook, same Drive cache
print("\n── C: second notebook, same Drive cache → NO upload prompt ──")
os.chdir(tempfile.mkdtemp())          # fresh session dir, nothing local
state.clear()
install_fake_colab(True, drive_root, REAL_CSV)
ns2 = {"__name__": "__main__"}; exec(compile(src, "<setup>", "exec"), ns2)
df2 = ns2["load_csv"]("sepsis_timeseries.csv")
check("no upload was requested", state.get("upload_called", 0) == 0)
check("data came from the Drive cache", df2.shape[0] == 37704)

# ------------------------------------------------------- B: participant declines Drive
print("\n── B: Colab, Drive declined → plain per-session upload still works ──")
os.chdir(tempfile.mkdtemp())
state.clear()
install_fake_colab(False, drive_root, REAL_CSV)
ns3 = {"__name__": "__main__"}; exec(compile(src, "<setup>", "exec"), ns3)
check("_drive_cache() returns None when declined", ns3["_drive_cache"]() is None)
df3 = ns3["load_csv"]("sepsis_timeseries.csv")
check("upload path used", state.get("upload_called") == 1)
check(f"loaded {df3.shape[0]:,} rows anyway", df3.shape[0] == 37704)

os.chdir(WS)
shutil.rmtree(tmp_root, ignore_errors=True)
print("\n" + "=" * 55)
print("❌ %d FAILURE(S)" % len(fails) if fails else "✅ ALL SIMULATED-COLAB PATHS PASSED")
for f in fails:
    print("   -", f)
sys.exit(1 if fails else 0)
