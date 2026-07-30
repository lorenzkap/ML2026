# 🩺 Practical Machine Learning for Medical Research

A 6-hour hands-on course on real ICU data. Nothing to install — everything runs in your browser.

## ▶️ Start here

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/lorenzkap/ML2026/blob/main/00_START_HERE.ipynb)
&nbsp;**← click this**

That opens **`00_START_HERE`** in Google Colab (you just need a free Google account). Run the cells
from the top: it checks your setup, loads the data, and gives you the clickable index of the whole
course. Then work through the notebooks in order, starting with **01**.

Every notebook has its own "Open in Colab" badge at the top, so you can jump into any of them. It
also carries **previous · index · next** links under that badge and a big **➡️ Next** button at the
very bottom, so at the end of a notebook you go straight on to the next one without coming back here.

## 📦 The data

**You don't have to do anything — the notebooks download it automatically** the first time you need
it. The download link is also **posted in the course Teams channel** if you ever need it by hand.

Two files:

| File | What it is |
|------|------------|
| `sepsis_timeseries.csv` | the main file — **one row per patient per 4-hour block**: 37,704 rows spanning 1,696 ICU stays |
| `sepsis_patients.csv` | **one row per ICU stay** (1,696), with the time series already summarised — used from notebook 05 on |

Notebook **04** is where the first file becomes the second, so you never have to take the summary on
trust — you build it.

If the automatic download fails, paste the Teams link into `WORKSHOP_DATA_URL` at the top of the
setup cell. As a last resort the notebook will offer to let you upload the two files by hand.

Running locally instead of Colab? Put both CSVs in a `data/` folder next to the notebooks and they'll
be found with no download at all.

## 📚 The course

**01–08 are the taught core:** pandas → cleaning → exploring → ⭐ time-series features → first models
→ evaluation → SHAP → leakage and pitfalls.

**09–15 are yours to keep:** tuning, 30 pandas tricks, reinforcement learning (a Gym game, then a sepsis
environment built from the data), working beyond pandas,
fairness across subgroups, a 🏆 capstone challenge, and its worked solutions.

Notebook **04** is the heart of it — turning a patient's timeline into features is what separates a
toy model from a useful one.

## 🛠️ Maintaining the course

The prev/next navigation is **generated**, with the index table in `00_START_HERE.ipynb` as the single
source of truth for the order and the titles:

```bash
python tools/update_nav.py           # rewrite the navigation in every notebook
python tools/update_nav.py --check   # exit 1 if any notebook is out of date
```

Add, rename or reorder a row in that table and re-run it — the header links and the ➡️ Next buttons
follow. (Run it *after* `tests/run_all_notebooks.py`, not during: executing a notebook rewrites it.)

## ⚖️ Ground rules

- This is **real, de-identified patient data**, covered by a data use agreement.
  **Do not redistribute the CSVs** and do not try to re-identify anyone. The notebooks you can share.
- **Never paste patient rows into ChatGPT or any other public LLM.** Notebook 10 shows the safe way.
- Anything you build here is **for teaching only** — not validated for clinical use.
