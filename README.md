# 🩺 Practical Machine Learning for Medical Research

**A 6-hour hands-on workshop on real ICU data — nothing to install, everything runs in your browser.**

[![Open the workshop in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/lorenzkap/ML2026/blob/main/00_START_HERE.ipynb)
&nbsp;⬅ **participants: click this, it's the only link you need**

> Learn to clean, explore, model and interpret **real ICU time-series data** with Python, pandas and
> scikit-learn — and leave with notebooks you can point at *your own* clinical CSV tomorrow.

Built for **clinicians and medical scientists** — physicians, researchers, epidemiologists, lab and
translational scientists — who are comfortable with medicine or biomedical research but new (or
newish) to machine learning. **No prior Python required.** Every topic ends in a runnable Google
Colab notebook you can modify. The running example is **sepsis in the ICU**: predicting 90-day
mortality from vitals, labs and treatments recorded every 4 hours, with a heavy emphasis on
**time-series clinical data** (lags, deltas, rolling windows, cumulative sums, per-patient aggregation).

---

## 🚀 Quick start (2 minutes)

### If you are a **participant**

1. **Click** the badge above (or [this link](https://colab.research.google.com/github/lorenzkap/ML2026/blob/main/00_START_HERE.ipynb)) — it opens `00_START_HERE` in Google Colab. You need a free Google account.
2. **Get the two data files from your instructor** — `sepsis_timeseries.csv` and
   `sepsis_patients.csv`. They are *not* in this repository (see [Where's the data?](#-wheres-the-data) below).
   Download them to your laptop, somewhere you can find them again.
3. **Run the cells top to bottom.** When Colab asks you to upload, pick those two CSVs. Say **yes**
   to connecting Google Drive — the files get cached to `MyDrive/sepsis_workshop_data/` and you
   will **never upload them again**, not even in a new session or a different notebook.
4. Green ticks? You're done. Open **Notebook 01** from the index in `00_START_HERE`.

That's it. Every other notebook has its own "Open in Colab" badge at the top and finds the data by
itself.

### If you are the **instructor**

Read **[`INSTRUCTOR_GUIDE.md`](INSTRUCTOR_GUIDE.md)** — timings, talking points, and the "wow"
moments. The short version:

1. **A week before:** open `00_START_HERE` and `05` in Colab yourself and run them end to end.
2. **Decide how to hand out the data** (see the two options below).
3. **On the day:** project `00_START_HERE`, walk the room through the upload once, and go.

**Handing out the data — option A (simple):** put `data/sepsis_timeseries.csv` and
`data/sepsis_patients.csv` on a USB stick / internal share; participants upload them in step 3 above.

**Handing out the data — option B (zero uploads):** host the two CSVs behind a direct-download URL
your participants can reach (institutional web space, an authenticated share, a private bucket).
Then tell everyone to set **one variable** at the top of the setup cell:

```python
WORKSHOP_DATA_URL = "https://your-institution.example/sepsis_workshop/"
```

The loader will fetch `sepsis_timeseries.csv` and `sepsis_patients.csv` from there automatically and
nobody ever sees an upload prompt. (Only do this where the PhysioNet DUA allows — see
[licence](#️-data-provenance-licence--ethics--please-read).)

### Running locally instead of Colab

```bash
git clone https://github.com/lorenzkap/ML2026.git
cd ML2026
pip install -r requirements.txt
# put the two CSVs in ./data/  -->  the loader finds them, no upload needed
jupyter lab
```

---

## 📁 Where's the data?

**The CSVs are deliberately not in this repository.** They are derived from **MIMIC-IV**, which is
credentialed on PhysioNet and governed by a Data Use Agreement that forbids open redistribution.
The *notebooks* are free to share; the *data* is not.

| File | Size | What it is | Where it goes |
|------|-----:|------------|---------------|
| `sepsis_timeseries.csv` | ≈9.5 MB | the main file — one row per patient per 4-hour block, 53 columns | `data/` (local) **or** upload it in Colab |
| `sepsis_patients.csv` | ≈0.9 MB | one row per patient, 107 columns — used by notebooks 05–08, 13, 14 | same; notebooks **rebuild it automatically** if it's missing |

So the folder layout the notebooks expect is simply:

```
ML2026/
├── 00_START_HERE.ipynb
├── 01_pandas_for_clinical_data.ipynb
├── …
└── data/
    ├── sepsis_timeseries.csv     ← from your instructor
    ├── sepsis_patients.csv       ← from your instructor
    └── data_dictionary.md        ← in the repo: every column explained
```

The loader searches, in order: the current folder → `data/` → `../data/` → your Google Drive cache →
`WORKSHOP_DATA_URL` → and only then asks you to upload. **Ask your instructor for the files** — or,
if you are PhysioNet-credentialed and want to rebuild them from scratch, see
[Reproducing the sample](#-reproducing--resizing-the-sample).

Every column is documented in **[`data/data_dictionary.md`](data/data_dictionary.md)**, including the
*intentional* data-quality quirks we use for teaching.

---

## 🎯 What you'll be able to do by the end

1. Load, filter, group and reshape a longitudinal ICU dataset with **pandas**.
2. **Clean** messy clinical data — impossible values, unit errors, outliers, missingness — *without*
   destroying real signal, using **time-series-aware** imputation.
3. Turn a patient's **timeline into features**: lags, rate-of-change, rolling windows, cumulative
   sums, trends — the core skill of clinical ML.
4. Train and compare **Logistic Regression, Random Forest and XGBoost**.
5. Evaluate models the way a clinician should: **ROC-AUC, precision/recall, calibration, thresholds**
   — not just accuracy.
6. Explain predictions with **SHAP** — including *"why did the model flag **this** patient?"*.
7. Recognise and avoid the classic traps: **data leakage, patient overlap, improper validation,
   class imbalance**.
8. Check whether your model works **for every subgroup**, and report it the way TRIPOD+AI expects.

---

## 📚 The notebooks

Every badge opens that notebook directly in Colab.

| # | Notebook | You'll learn | ~min |
|---|----------|--------------|-----:|
| 00 | [**🚦 START HERE**](https://colab.research.google.com/github/lorenzkap/ML2026/blob/main/00_START_HERE.ipynb) | environment check, one-time data setup, the course index | 20 |
| 01 | [**Pandas for clinical data**](https://colab.research.google.com/github/lorenzkap/ML2026/blob/main/01_pandas_for_clinical_data.ipynb) | load, filter, groupby, datetime, pivot, merge | 55 |
| 02 | [**Cleaning messy clinical data**](https://colab.research.google.com/github/lorenzkap/ML2026/blob/main/02_data_cleaning.ipynb) | missingness, impossible values, unit errors, outliers, duplicates | 55 |
| 03 | [**Exploratory data analysis**](https://colab.research.google.com/github/lorenzkap/ML2026/blob/main/03_exploratory_data_analysis.ipynb) | distributions, correlations, trajectories over time | 35 |
| 04 | [⭐ **Turning a timeline into features**](https://colab.research.google.com/github/lorenzkap/ML2026/blob/main/04_time_series_feature_engineering.ipynb) | lags, deltas, rolling/expanding windows, leakage-safe aggregation | 70 |
| 05 | [**Your first predictive models**](https://colab.research.google.com/github/lorenzkap/ML2026/blob/main/05_first_ml_models.ipynb) | pipelines, train/test split *by patient*, LogReg → RF → XGBoost | 65 |
| 06 | [**Evaluating models like a clinician**](https://colab.research.google.com/github/lorenzkap/ML2026/blob/main/06_model_evaluation.ipynb) | ROC, PR, confusion matrix, thresholds, **calibration** | 45 |
| 07 | [**Opening the black box with SHAP**](https://colab.research.google.com/github/lorenzkap/ML2026/blob/main/07_explainable_ai.ipynb) | global & per-patient explanations | 35 |
| 08 | [**How to fool yourself**](https://colab.research.google.com/github/lorenzkap/ML2026/blob/main/08_pitfalls_and_leakage.ipynb) | data leakage, patient overlap, tuning on test, temporal validation | 40 |

### 🎒 The flex pool — take-home, or live if the room is fast

| # | Notebook | You'll learn | ~min |
|---|----------|--------------|-----:|
| 09 | [**Optimizing your model**](https://colab.research.google.com/github/lorenzkap/ML2026/blob/main/09_model_optimization.ipynb) | does cleaning help? (measured) · hyperparameter **search** · leaderboard | 55 |
| 10 | [**30 pandas tricks** *(+ LLM copilot)*](https://colab.research.google.com/github/lorenzkap/ML2026/blob/main/10_bonus_pandas_tricks.ipynb) | a punchy reference you'll reuse for years · using LLMs safely | 45 |
| 11 | [🧪 **Reinforcement learning (Q-learning)**](https://colab.research.google.com/github/lorenzkap/ML2026/blob/main/11_reinforcement_learning_qlearning.ipynb) | learn a sepsis *treatment policy*, AI-Clinician style — offline RL, honestly | 70 |
| 12 | [📦 **When your data is too big for pandas**](https://colab.research.google.com/github/lorenzkap/ML2026/blob/main/12_big_data_beyond_pandas.ipynb) | Parquet, chunking, **Polars / DuckDB / Dask / Spark**; big-data sources | 15 |
| 13 | [⚖️ **Fairness & subgroup performance**](https://colab.research.google.com/github/lorenzkap/ML2026/blob/main/13_fairness_and_subgroups.ipynb) | per-subgroup AUC & calibration, bootstrap CIs, the impossibility theorem | 35 |
| 14 | [🏆 **The capstone challenge**](https://colab.research.google.com/github/lorenzkap/ML2026/blob/main/14_capstone_challenge.ipynb) | beat the baseline on a locked held-out set · live leaderboard | 60 |

Notebook **04** is the heart of the course — clinical data is *temporal*, and knowing how to engineer
time-series features is what separates a toy model from a useful one. Notebook **14** is the most fun
way to end a day if the group has energy left; **11** is the "where does this lead?" finale for the
RL-curious.

---

## ⏱️ The 6-hour schedule

Six hours of contact time, breaks included. Times are shown from a 09:00 start — shift as needed.

| Time | Elapsed | Session |
|------|---------|---------|
| 09:00 – 09:20 | 0:20 | Welcome · why ML in medicine · the dataset · **00 START HERE** (everyone gets the data loaded) |
| 09:20 – 10:15 | 1:15 | **01 Pandas for clinical data** |
| 10:15 – 11:10 | 2:10 | **02 Data cleaning** |
| 11:10 – 11:25 | 2:25 | ☕ **Break** |
| 11:25 – 12:00 | 3:00 | **03 Exploratory data analysis** |
| 12:00 – 13:10 | 4:10 | ⭐ **04 Time-series feature engineering** — the core skill, don't rush it |
| 13:10 – 13:40 | 4:40 | 🍽️ **Lunch** |
| 13:40 – 14:45 | 5:45 | **05 Your first predictive models** |
| 14:45 – 15:30 | 6:30 | **06 Evaluating models like a clinician** |
| 15:30 – 16:05 | 7:05 | **07 SHAP** + **08 Pitfalls & leakage** — highlights, run as a double act |
| 16:05 | | Wrap-up · what to do with your own data · Q&A |

*(7:05 elapsed − 45 min of breaks = **6:20 of teaching**. If you need a hard 6:00, cut Notebook 03 to
20 minutes and run 07/08 as a 25-minute demo.)*

**Running ahead? Pull from the flex pool** — in this order, depending on the room:

| The room is… | Give them |
|--------------|-----------|
| competitive / hands-on | 🏆 **14 Capstone challenge** (the best 60 min you can add) |
| methodological / academic | ⚖️ **13 Fairness** then **08** in full |
| wants better numbers | **09 Optimization** |
| curious where AI in medicine is going | 🧪 **11 Reinforcement learning** |
| already drowning in real data | 📦 **12 Big data** · **10 pandas tricks** |

**Running short?** The irreducible core is **01 → 02 → 04 → 05 → 06**. Everything else is
self-containable as take-home material — the notebooks are written to be read alone.

---

## 🗂️ The dataset in one paragraph

A **real, de-identified ICU cohort** of sepsis patients from **MIMIC-IV** (Beth Israel Deaconess
Medical Center) — the same data used in the *AI Clinician* studies — down-sampled to **1,696 ICU
stays** so it fits comfortably in Colab. One row per patient per **4-hour block**; ~50 columns of
vitals, labs, ventilation, fluids, vasopressors and severity scores; the target is **90-day
mortality** (≈18% of patients). Full column reference and the (intentional!) data-quality quirks are
in **[`data/data_dictionary.md`](data/data_dictionary.md)**.

### ⚖️ Data provenance, licence & ethics — please read

- The teaching subset is **derived from MIMIC-IV**, credentialed on
  [PhysioNet](https://physionet.org/content/mimiciv/) and governed by a Data Use Agreement.
- **This is why the CSVs are not in this repo.** Do not commit them, do not put them on a public
  URL, and do not share them with anyone who has not completed PhysioNet credentialing and the
  required human-subjects training. Share the *notebooks* freely; share the *data* responsibly.
- The data is **de-identified** (dates shifted; ages capped). Do not attempt to re-identify patients.
- Models built here are **for teaching only** — not validated for clinical use.
- **Never paste patient rows into a public LLM.** Notebook 10 has the safe recipes; aggregate
  `describe()` output and schema are usually fine, individual records are not.

---

## 🧭 Reproducing / resizing the sample

The subset was built by **[`build_sample_dataset.py`](build_sample_dataset.py)** from the full
AI-Clinician MIMIC-IV sepsis cohort: fixed random seed (reproducible), stratified by outcome,
force-including the patients that carry the teaching artifacts, and injecting 6 duplicate rows for
the cleaning exercise. Change `N_RANDOM_STAYS` to make it bigger or smaller. You need your own
credentialed copy of the source cohort to run it.

## 🔧 Repo layout

```
00_START_HERE.ipynb …… 14_capstone_challenge.ipynb   the course
README.md                    this file
INSTRUCTOR_GUIDE.md          timings, talking points, "wow" moments, troubleshooting
requirements.txt             minimal local environment
build_sample_dataset.py      how the teaching subset was made
data/data_dictionary.md      every column explained
data/*.csv                   ← NOT in git (see licence above); get them from the instructor
```

---

## 🙏 Inspiration & further reading

- **AI Clinician** — Komorowski et al., *A reinforcement learning approach to sepsis treatment*,
  *Nature Medicine* 2018 (the cohort design this dataset follows).
- **The critique** — Gottesman et al., *Guidelines for reinforcement learning in healthcare*,
  *Nature Medicine* 2019.
- **MIMIC-IV** — Johnson et al., *Scientific Data* 2023 · [physionet.org](https://physionet.org/content/mimiciv/).
- **TRIPOD+AI** — Collins et al., *BMJ* 2024 — how to report a clinical prediction model.
- Improved inpatient deterioration detection using time-series vital signs —
  [*Scientific Reports* 2022](https://www.nature.com/articles/s41598-022-16195-2).
- scikit-learn, SHAP and XGBoost documentation.

Have fun — and at the end of the day, open one of *your* CSVs and try the same recipes. 🚀
