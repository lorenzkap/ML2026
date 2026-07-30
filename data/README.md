# 📁 Put the workshop data here

**This folder is intentionally almost empty.** The two workshop CSVs are *not* in this repository.

## Why not?

They are derived from **MIMIC-IV**, a credentialed ICU database hosted on
[PhysioNet](https://physionet.org/content/mimiciv/) and governed by a **Data Use Agreement that
forbids open redistribution**. The notebooks are free to share; the patient data is not.

## What goes here

Get these two files from your workshop instructor (USB stick, internal share, or a private link):

| File | Size | What it is |
|------|-----:|------------|
| `sepsis_timeseries.csv` | ≈9.5 MB | the main file — one row per patient per 4-hour block, 53 columns, 1,696 ICU stays |
| `sepsis_patients.csv` | ≈0.9 MB | one row per patient, 107 columns — used by notebooks 05–08, 13, 14 |

Drop them in **this folder**:

```
ML2026/
├── 00_START_HERE.ipynb
├── 01_pandas_for_clinical_data.ipynb
├── …
└── data/
    ├── sepsis_timeseries.csv   ← here
    ├── sepsis_patients.csv     ← here
    ├── data_dictionary.md
    └── README.md               (this file)
```

…and the notebooks will find them automatically with no upload prompt.

> `sepsis_patients.csv` is optional — every notebook that needs it will **rebuild it from the
> time-series file** if it's missing (that's what Notebook 04 teaches you to do).

## If you're on Google Colab

You don't need this folder at all. Run the first cell of
[`00_START_HERE.ipynb`](../00_START_HERE.ipynb), upload the two CSVs when prompted, and say **yes**
to connecting Google Drive — they get cached to `MyDrive/sepsis_workshop_data/` and you never upload
them again.

## If you're the instructor

You can skip uploads entirely: host the two CSVs behind a direct-download URL your participants can
reach, then have everyone set one variable at the top of the setup cell:

```python
WORKSHOP_DATA_URL = "https://your-institution.example/sepsis_workshop/"
```

Only do this where the DUA permits — i.e. an access-controlled location, not a public bucket.

## Rebuilding the data yourself

If you are PhysioNet-credentialed and have the full AI-Clinician MIMIC-IV sepsis cohort,
[`../build_sample_dataset.py`](../build_sample_dataset.py) regenerates this teaching subset
reproducibly (fixed seed, stratified by outcome, preserving the intentional teaching artifacts).

---

**Column reference:** [`data_dictionary.md`](data_dictionary.md) — every column, its units, and the
deliberate data-quality quirks the workshop uses for teaching.
