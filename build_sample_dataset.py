"""Build a small, uploadable teaching sample from the full MIMIC-IV sepsis cohort.
Produces:
  sepsis_timeseries.csv  -- longitudinal (one row per patient per 4h block)  [the 'upload this' file]
  sepsis_patients.csv    -- patient-level engineered feature table (one row per ICU stay)
Design goals: small (<10 MB), preserves time-series structure, retains real data-quality
teaching artifacts (unit errors, outliers, missingness), reproducible (fixed seed).
"""
import numpy as np, pandas as pd

SRC = r"c:/Users/lolka/Claude/Projects/Reinforcement Learning/Course/mimic_dataset.csv"
OUT = r"c:/Users/lolka/Claude/Projects/Reinforcement Learning/Course"
SEED = 42
N_RANDOM_STAYS = 1500
rng = np.random.default_rng(SEED)

COLS = [
    # identifiers / time
    'icustayid','bloc','timestep',
    # demographics / context
    'age','gender','Weight_kg','Height_cm','elixhauser','re_admission',
    # vitals
    'GCS','HR','SysBP','MeanBP','DiaBP','RR','SpO2','Temp_C','Temp_F',
    # labs
    'Potassium','Sodium','Chloride','Glucose','BUN','Creatinine','Calcium','Ionised_Ca',
    'Magnesium','CO2_mEqL','Albumin','Total_bili','Hb','WBC_count','Platelets_count','INR',
    'Arterial_pH','paO2','paCO2','Arterial_lactate','HCO3','SaO2',
    # support / treatment
    'FiO2_1','PEEP','mechvent','input_step','output_step','cumulated_balance','max_dose_vaso',
    # derived severity scores
    'Shock_Index','PaO2_FiO2','SOFA','SIRS',
    # outcomes
    'morta_90','died_in_hosp',
]

print("Loading", len(COLS), "columns from full dataset ...")
df = pd.read_csv(SRC, usecols=COLS)
df = df[COLS]  # enforce order
print("Full:", df.shape, "| stays:", df['icustayid'].nunique())

# ---- identify stays carrying juicy data-quality artifacts (force-include) ----
art_mask = (
    (df['Temp_F'] > 110) | (df['Temp_F'] < 90) |   # temperature unit/entry errors
    (df['Creatinine'] > 15) | (df['WBC_count'] > 100) |
    (df['Platelets_count'] > 1200) | (df['Shock_Index'] > 3) |
    (df['HR'] < 20) | (df['RR'] < 3)
)
artifact_stays = df.loc[art_mask, 'icustayid'].unique()
artifact_stays = rng.permutation(artifact_stays)[:200]
print("Artifact-bearing stays available:", art_mask.sum(), "rows ->", len(artifact_stays), "stays force-included")

# ---- stratified random sample of stays by 90-day mortality ----
pt = df.groupby('icustayid')['morta_90'].max()
pos = pt[pt == 1].index.to_numpy(); neg = pt[pt == 0].index.to_numpy()
n_pos = int(round(N_RANDOM_STAYS * pt.mean()))
n_neg = N_RANDOM_STAYS - n_pos
samp = np.concatenate([rng.choice(pos, n_pos, replace=False),
                       rng.choice(neg, n_neg, replace=False)])
keep = np.union1d(samp, artifact_stays)
print(f"Sampled stays: {len(samp)} (pos={n_pos}, neg={n_neg}) + artifacts -> {len(keep)} unique stays")

ts = df[df['icustayid'].isin(keep)].copy()
ts = ts.sort_values(['icustayid','bloc']).reset_index(drop=True)

# ---- inject a few exact-duplicate rows (documented teaching artifact for drop_duplicates) ----
dup_src = ts.sample(6, random_state=SEED)
ts = pd.concat([ts, dup_src], ignore_index=True)
ts = ts.sort_values(['icustayid','bloc']).reset_index(drop=True)
print("Injected", len(dup_src), "duplicate rows (teaching artifact)")

# round floats to keep file small & readable
floatcols = ts.select_dtypes('float').columns
ts[floatcols] = ts[floatcols].round(2)

ts_path = OUT + "/sepsis_timeseries.csv"
ts.to_csv(ts_path, index=False)
import os
print(f"\nWROTE {ts_path}  shape={ts.shape}  size={os.path.getsize(ts_path)/1e6:.2f} MB")
print("  stays:", ts['icustayid'].nunique(), "| patient mortality:", ts.groupby('icustayid')['morta_90'].max().mean().round(3))
print("  Temp_F errors kept:", ((ts['Temp_F']>110)|(ts['Temp_F']<90)).sum(),
      "| duplicate rows:", ts.duplicated().sum())

# =====================================================================
# Patient-level feature table  (CANONICAL logic — mirrored in notebook 04)
# =====================================================================
def build_patient_table(ts):
    df = ts.copy()
    # clean temperature: prefer Celsius; repair obvious F-entry errors, drop impossible
    tf = df['Temp_F'].where((df['Temp_F']>=90)&(df['Temp_F']<=110))
    tc = df['Temp_C'].where((df['Temp_C']>=25)&(df['Temp_C']<=45))
    df['Temp_C_clean'] = tc.fillna((tf-32)*5/9)
    # impossible-vitals -> NaN then per-stay ffill/bfill
    for c,lo,hi in [('HR',20,300),('SysBP',40,300),('MeanBP',20,220),('RR',3,80),('SpO2',30,100)]:
        df[c] = df[c].where((df[c]>=lo)&(df[c]<=hi))
    g = df.groupby('icustayid', group_keys=False)
    vitcols = ['HR','SysBP','MeanBP','RR','SpO2','Temp_C_clean']
    df[vitcols] = g[vitcols].apply(lambda x: x.ffill().bfill())
    # winsorise skewed labs (clip 1st-99th pct) so one stray value can't define a min/max
    for c in ['Arterial_lactate','Creatinine','BUN','WBC_count','Platelets_count','INR','Glucose']:
        lo, hi = df[c].quantile(0.01), df[c].quantile(0.99)
        df[c] = df[c].clip(lo, hi)

    tv = ['HR','SysBP','MeanBP','RR','SpO2','Temp_C_clean','GCS','Creatinine','BUN',
          'Arterial_lactate','WBC_count','Platelets_count','Potassium','Sodium',
          'Albumin','INR','Arterial_pH','Shock_Index','SOFA','SIRS','PaO2_FiO2','Hb']
    grp = df.groupby('icustayid')
    feats = {}
    # static
    feats['age'] = grp['age'].first()
    feats['gender'] = grp['gender'].first()
    feats['elixhauser'] = grp['elixhauser'].first()
    feats['re_admission'] = grp['re_admission'].first().astype(int)
    feats['weight_kg'] = grp['Weight_kg'].median()
    feats['n_blocs'] = grp.size()
    feats['los_hours'] = grp['bloc'].max()*4
    # treatment exposure
    feats['mechvent_ever'] = grp['mechvent'].max()
    feats['vaso_max'] = grp['max_dose_vaso'].max()
    feats['fluid_balance_last'] = grp['cumulated_balance'].last()
    feats['urine_total'] = grp['output_step'].sum()
    # time-varying summaries
    for c in tv:
        feats[f'{c}_mean'] = grp[c].mean()
        feats[f'{c}_min']  = grp[c].min()
        feats[f'{c}_max']  = grp[c].max()
        feats[f'{c}_last'] = grp[c].last()
    # simple trend (last minus first) for a few key markers
    for c in ['Creatinine','Arterial_lactate','SOFA','Shock_Index','GCS']:
        feats[f'{c}_delta'] = grp[c].last() - grp[c].first()
    X = pd.DataFrame(feats)
    X['morta_90'] = grp['morta_90'].max()
    X['died_in_hosp'] = grp['died_in_hosp'].max()
    return X.reset_index()

pts = build_patient_table(ts)
pts_floatcols = pts.select_dtypes('float').columns
pts[pts_floatcols] = pts[pts_floatcols].round(4)
pts_path = OUT + "/sepsis_patients.csv"
pts.to_csv(pts_path, index=False)
print(f"\nWROTE {pts_path}  shape={pts.shape}  size={os.path.getsize(pts_path)/1e6:.2f} MB")

# ---- quick sanity: does a baseline model find signal? ----
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import cross_val_score, StratifiedKFold
Xy = pts.drop(columns=['icustayid','morta_90','died_in_hosp']).fillna(pts.median(numeric_only=True))
y = pts['morta_90']
auc = cross_val_score(RandomForestClassifier(n_estimators=200, random_state=0, n_jobs=-1),
                      Xy, y, cv=StratifiedKFold(5, shuffle=True, random_state=0), scoring='roc_auc')
print(f"\nSanity baseline RF ROC-AUC (5-fold): {auc.mean():.3f} +/- {auc.std():.3f}  (target > 0.75)")
print("Class balance:", y.mean().round(3))
