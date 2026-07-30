# Data dictionary — Sepsis ICU teaching dataset

Two files, both derived from the **MIMIC-IV** critical-care database (a real, de-identified
ICU database from Beth Israel Deaconess Medical Center). This is the same cohort used by the
*AI Clinician* sepsis studies. It has been **down-sampled to a small teaching subset** so it
uploads to Google Colab in seconds.

- **`sepsis_timeseries.csv`** — longitudinal / time-series file. **One row per patient per 4-hour block.** This is the main file you upload. *1,696 ICU stays · 37,704 rows · 53 columns.*
- **`sepsis_patients.csv`** — patient-level table. **One row per ICU stay**, with time-series features already aggregated (mean/min/max/last/delta per variable). Convenience file for the modelling notebooks. *1,696 rows · 107 columns.*

Each ICU stay (`icustayid`) is a **sepsis patient**. Time advances in **4-hour blocks** (`bloc` = 1, 2, 3 …). The prediction target is **90-day mortality** (`morta_90`).

---

## Key columns in `sepsis_timeseries.csv`

### Identifiers & time
| column | meaning |
|---|---|
| `icustayid` | ICU stay ID — **the patient key**. Group / split by this. |
| `bloc` | Time-block index within the stay (1 = first 4 h, 2 = next 4 h …). |
| `timestep` | De-identified UNIX timestamp (seconds). Absolute dates are shifted to protect privacy, **but intervals are real** (consecutive blocks are 4 h = 14,400 s apart). |

### Demographics / context (constant within a stay)
| column | meaning | notes |
|---|---|---|
| `age` | Age in years | capped/clipped in MIMIC |
| `gender` | 0 / 1 (de-identified coding) | |
| `Weight_kg` | Body weight (kg) | ~8 % missing |
| `Height_cm` | Height (cm) | ~40 % missing — good "when to drop / impute?" example |
| `elixhauser` | Elixhauser comorbidity index | higher = sicker |
| `re_admission` | ICU re-admission flag (True/False) | |

### Vital signs (change over time)
`GCS` (Glasgow Coma Scale, 3–15), `HR` (heart rate), `SysBP`/`MeanBP`/`DiaBP` (blood pressure),
`RR` (respiratory rate), `SpO2` (oxygen saturation %), `Temp_C` (°C), `Temp_F` (°F).

### Laboratory values (change over time)
`Potassium`, `Sodium`, `Chloride`, `Glucose`, `BUN` (urea nitrogen), `Creatinine` (kidney),
`Calcium`, `Ionised_Ca`, `Magnesium`, `CO2_mEqL`, `Albumin`, `Total_bili` (bilirubin/liver),
`Hb` (haemoglobin), `WBC_count` (white cells — infection), `Platelets_count`, `INR` (clotting),
`Arterial_pH`, `paO2`, `paCO2`, `Arterial_lactate` (tissue hypoxia — key sepsis marker),
`HCO3`, `SaO2` (~95 % missing — good "mostly-empty column" example).

### Support & treatment
| column | meaning |
|---|---|
| `FiO2_1` | Fraction of inspired oxygen (0.21–1.0) |
| `PEEP` | Ventilator positive end-expiratory pressure |
| `mechvent` | On mechanical ventilation this block? (0/1) |
| `input_step` | Fluids given **during this block** (mL) |
| `output_step` | Urine / fluid out **during this block** (mL) |
| `cumulated_balance` | Running cumulative fluid balance (mL) — a cumulative sum |
| `max_dose_vaso` | Max vasopressor dose this block (0 = none) |

### Derived severity scores
| column | meaning |
|---|---|
| `Shock_Index` | HR / SysBP (>0.9 suggests shock) |
| `PaO2_FiO2` | Oxygenation ratio (lower = worse lungs / ARDS) |
| `SOFA` | Sequential Organ Failure Assessment (0–24, higher = worse) |
| `SIRS` | Systemic Inflammatory Response Syndrome criteria (0–4) |

### Outcomes (labels — constant within a stay)
| column | meaning |
|---|---|
| `morta_90` | **Died within 90 days? (1 = died). PRIMARY TARGET.** |
| `died_in_hosp` | Died during this hospital admission (1 = died). |

---

## ⚠️ Known data-quality issues (intentionally kept for the cleaning exercises)

This subset deliberately **retains real messiness** so you can practise cleaning. Look for:

1. **Temperature unit / entry errors** — `Temp_F` contains impossible values (e.g. 597 °F, 19 °F, 0)
   caused by unit mix-ups and typos. `Temp_C` is mostly clean. *(≈130 bad `Temp_F` values.)*
2. **Impossible physiological values** — a few `HR`/`RR` values of 0 or below survivable limits
   (sensor artifacts / missing-data sentinels), and extreme lab outliers
   (`Creatinine` > 15, `WBC_count` > 100, `Platelets_count` > 1200, `Shock_Index` > 3).
3. **Missing data** — `Height_cm` (~40 %), `Weight_kg` (~8 %), `SaO2` (~95 %), plus scattered lab gaps.
4. **Duplicate rows** — **6 exact-duplicate patient-block rows** were inserted for the
   `drop_duplicates()` exercise. Find them with `df.duplicated().sum()`.

> These issues are typical of raw hospital data. Part of the workshop is learning to **find and
> fix them without silently destroying real signal.**

---

## Patient-level file `sepsis_patients.csv`

Built by `build_sample_dataset.py` (and rebuilt in **Notebook 04**). One row per `icustayid`.
For each time-varying variable it contains `_mean`, `_min`, `_max`, `_last`; for a few key
markers also `_delta` (last − first). Plus static features (`age`, `elixhauser`, `weight_kg`…),
stay descriptors (`n_blocs`, `los_hours`), treatment exposure (`mechvent_ever`, `vaso_max`,
`fluid_balance_last`, `urine_total`) and the labels (`morta_90`, `died_in_hosp`).

**Always split by patient** — every row is already one unique patient here, but when you model the
time-series file directly, never let the same `icustayid` appear in both train and test.
