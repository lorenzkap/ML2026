# 🧪 Workshop self-tests

Run these before a workshop (or after editing any notebook) to be sure the day will actually work.
They need the two CSVs present in `../data/` and a Python env with the workshop packages plus
`nbclient`/`nbformat`:

```bash
pip install -r ../requirements.txt nbclient nbformat
```

| Script | What it proves | Runtime |
|--------|----------------|--------:|
| `run_all_notebooks.py` | every notebook executes top-to-bottom in a **fresh kernel** with no errors | ≈2 min |
| `test_data_loader.py` | the `WORKSHOP_DATA_URL` download path works, an unreachable URL falls back gracefully, and "no data anywhere" gives a *helpful* error rather than a traceback | ≈10 s |
| `test_colab_paths.py` | the **Colab-only** branches behave: Drive connected → upload once and cache; second notebook → no upload prompt; Drive declined → plain upload still works | ≈10 s |
| `test_determinism.py` | each notebook run **twice in fresh kernels** produces identical printed output — i.e. every participant really does get the same numbers | ≈5 min |

```bash
python tests/run_all_notebooks.py                 # all notebooks
python tests/run_all_notebooks.py 05_first_ml_models.ipynb   # just one

SAVE_EXECUTED=1 python tests/run_all_notebooks.py  # also write the outputs back into the .ipynb
```

`SAVE_EXECUTED=1` is how the committed notebooks get their stored outputs — the repo deliberately
ships executed notebooks so they read correctly on GitHub and in Colab.

## What these do *not* cover

`test_colab_paths.py` **simulates** Google Colab by injecting a fake `google.colab` module. It proves
the code paths are correct; it cannot prove Google's UI renders the notebook. Before a workshop,
still click the `00_START_HERE` badge in the README once yourself and run it end to end — ideally on
a clean Google account, so you see exactly what a participant sees.
