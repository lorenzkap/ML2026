# 👩‍🏫 Instructor guide — the 6-hour version

Everything you need to teach the day confidently, plus the talking points that make it land. The
notebooks are self-explanatory; this guide is the *"what to say and where to pause"* layer.

**Audience.** Pitched at **clinicians *and* medical scientists** — physicians, PhD researchers,
epidemiologists, lab and translational scientists. Where a note says "as a clinician", read it as
"anyone who has worked with real patient data"; the clinical framing is there to make the ML
concrete, not to exclude non-physicians. When a medical term appears (SOFA, ABG, lactate) it is
defined in one plain line — encourage bench scientists to ask, and clinicians to explain, in the room.

**Format.** 6 hours of contact time. Notebooks **00–08** are the taught spine; **09–14** are a flex
pool you draw from when the room moves fast, and hand out as take-home regardless.

---

## ⏱️ The timetable

| Time | Session | Your job |
|------|---------|----------|
| 09:00 – 09:20 | Welcome + **00 START HERE** | get *everyone* past the data upload before you teach anything |
| 09:20 – 10:15 | **01 Pandas** | build the "one row = one patient at one 4-h block" mental model |
| 10:15 – 11:10 | **02 Cleaning** | the Temp_F reveal; per-patient forward-fill |
| 11:10 – 11:25 | ☕ Break | circulate, fix broken laptops |
| 11:25 – 12:00 | **03 EDA** | the diverging trajectory plot — then move on, this one runs short by design |
| 12:00 – 13:10 | ⭐ **04 Feature engineering** | the core hour of the day — protect it |
| 13:10 – 13:40 | 🍽️ Lunch | |
| 13:40 – 14:45 | **05 First models** | pipelines + split by patient |
| 14:45 – 15:30 | **06 Evaluation** | accuracy trap, thresholds, calibration |
| 15:30 – 16:05 | **07 SHAP + 08 Pitfalls** | run as one double act: "why this patient?" then "how you fool yourself" |
| 16:05 | Wrap-up | what to do with their own data · Q&A · point at the flex pool |

**The three timing decisions that make or break the day:**

1. **Do not let 00 + 01 eat into 04.** If half the room is still fighting the upload at 09:30, tell
   them to pair up with a neighbour and carry on. One working laptop per pair is enough.
2. **04 gets its full 70 minutes.** It is the single most transferable skill in the course. If you
   are behind by lunch, take the time out of 03 and 07 — not out of 04.
3. **07 and 08 are a highlights reel, not a full run.** Show the SHAP waterfall for one patient, then
   the random-split-vs-patient-split number in 08. Two plots, twelve minutes each, huge impact.

**If you have to hit a hard 6:00:** cut 03 to 20 minutes (show the trajectory plot, skip the
correlation section) and run 07/08 as a 25-minute demo with no exercises.

**If you are running ahead**, pick from the flex pool by reading the room:

| The room is… | Give them | Why |
|--------------|-----------|-----|
| competitive, hands-on | 🏆 **14 Capstone** | 60 min, everything applied, they'll remember it |
| methodological, academic | ⚖️ **13 Fairness** + **08** in full | the reviewer-proofing content |
| chasing better numbers | **09 Optimization** | and the honest "cleaning doesn't always help AUC" lesson |
| curious about AI's direction | 🧪 **11 Reinforcement learning** | predicting → *choosing* |
| already drowning in real data | 📦 **12 Big data**, **10 tricks** | pure reference value |

---

## Before the day

- **Test the pipeline yourself once.** Open `00_START_HERE` and `05` in Colab (via the badges), run
  top to bottom, upload the CSVs. Do this on a *clean* Google account if you can — it's the only way
  to see what participants see.
- **Decide how the data reaches them** — README "Quick start" has both options. Either hand out the
  two CSVs (USB / internal share) or host them behind a direct-download URL and have everyone set
  `WORKSHOP_DATA_URL` in the setup cell. Remember the **PhysioNet DUA**: only share the data with
  credentialed participants. The *notebooks* can be shared freely — that's what the public repo is for.
- **Send one link the week before**: the `00_START_HERE` Colab badge from the README, plus "please
  make sure you can sign into a Google account".
- **Room check:** Wi-Fi that survives 20 people on Colab; a projector; encourage laptops (not tablets).
- **Split the room into pairs** — clinicians learn ML faster in pairs (one drives, one reads).

## How to run each session

Project your screen, run a cell, *narrate what you expect before you run it*, then let pairs do the
**✏️ Your turn** exercises (2–5 min each) while you circulate. The `<details>` solutions are there so
nobody gets stuck. Keep energy up: this is a *doing* day, not a lecture.

---

## Per-notebook teaching notes & the moments to slow down for

### 00 — START HERE  *(20 min, and it is not optional)*
- This exists because "everyone gets the data loaded" used to eat 40 minutes of Notebook 01. Do it
  as a group, at the front, with the projector on the upload dialog.
- **Push Google Drive hard.** One click now = zero uploads for the rest of the day, including after
  the inevitable Colab session reset. Participants who decline will re-upload six times and blame the
  workshop.
- Use the environment self-check output as a roll call: "put your hand up if you don't see all ticks."
- The index at the bottom is how they navigate all day. Tell them to keep the tab open.

### 01 — Pandas for clinical data
- The mental model to hammer: **one row = one patient at one 4-hour block.** Draw it on the board.
- Great first "aha": `groupby("icustayid")` collapses a timeline into per-patient facts. Clinicians
  instantly get "max SOFA during the stay".
- The **datetime** bit surprises people: dates are shifted to the future for de-identification, but the
  4-hour spacing is real. Good moment to discuss de-identification.

### 02 — Data cleaning  *(highest "I can use this Monday" value)*
- **The temperature trap** is the showpiece. Put `df["Temp_F"].max()` on screen (≈ 104,109 °F) and let
  the gasp happen. Message: *a single column can hide unit mix-ups and typos; always sanity-check ranges
  and cross-validate against a second column* (`Temp_C`).
- **Per-patient forward-fill vs global mean.** The day's most important cleaning idea, and it's
  time-series specific: carry the last *known* value forward *within a patient*, never borrowing from
  another patient or from the future. Show one patient's creatinine before/after.
- **Clip, don't delete, outliers** — and **never touch the label.** A creatinine of 15 may be a real,
  very sick patient. Deleting sick patients biases the model toward looking healthy.
- The 6 injected duplicate rows are found with `df.duplicated().sum()` — a nice concrete win.

### 03 — EDA  *(deliberately the shortest taught session)*
- The **trajectory plot** (mean SOFA/lactate by 4-hour block, split by survival, with a CI band) is the
  emotional peak: non-survivors visibly diverge over time. Pause here, then keep moving.
- Introduce **class imbalance** (≈18% deaths) gently — it sets up Notebook 06.
- "Missingness as signal": whether a lab was even ordered can correlate with outcome. Clinicians love
  this because it matches how they think — and it comes back as a *feature* in 04 and 14.
- This is your time bank. If the morning ran long, this is what you shorten.

### 04 ⭐ — Time-series feature engineering  *(the core skill; give it the full 70 min)*
- Anchor every transform to **`groupby("icustayid")`** so nothing leaks across patients. Say it every time.
- Sequence to teach: **lag → delta/rate → rolling → cumulative → expanding → trend.** Each is one line of
  pandas; each has an obvious clinical meaning ("a *rising* lactate is worse than a high but falling one").
- **1 block = 4 hours** → a "6-hour window" ≈ 1–2 blocks, "24-hour" ≈ 6 blocks. Connect windows to clinical
  horizons.
- Spend real time on the **leakage** section: whole-stay `max()` is fine for *end-of-stay* mortality, but
  for an *early-warning* model you may only use data up to time *t*. This distinction is the difference
  between a paper that replicates and one that doesn't.
- Ends by **building `sepsis_patients.csv`** — the table the modelling notebooks consume. If a participant
  skips 04, notebooks 05–08, 13 and 14 rebuild it automatically.

### 05 — First models
- **Pipelines prevent leakage**: the scaler/imputer is fit on the *training fold only*. Show the 3-line
  `Pipeline` and explain that this is not cosmetic — it's correctness.
- **Split by patient.** On the patient table each row is already one patient, so a stratified split is fine;
  but show the `GroupShuffleSplit` pattern for the raw time series and promise the full demo in 08.
- `class_weight="balanced"` / `scale_pos_weight` — one sentence on why imbalance needs it.
- Expected honest ROC-AUC ≈ **0.76–0.80**. If someone reports 0.99, they've leaked — celebrate it as a
  teaching moment and jump to 08.

### 06 — Evaluation
- Open with the **accuracy trap**: "predict everyone survives" scores ~82% accuracy and is useless.
- **Calibration** is the clinician's metric and is under-taught elsewhere: a predicted 20% must *mean* 20%.
  Contrast a higher-AUC but poorly-calibrated model with a slightly lower-AUC well-calibrated one and ask
  "which would you deploy?".
- **Threshold = a clinical decision.** Frame it as alarms-per-caught-death; there is no universal 0.5.

### 07 — SHAP  *(35 min, highlights)*
- Global beeswarm first (what the model uses *overall*), then the **single-patient waterfall** ("why THIS
  patient?"). The per-patient explanation is what wins clinicians over — if you only have ten minutes,
  show this one plot.
- Caveat clearly: SHAP explains **the model, not the biology**; correlation ≠ causation; features can be
  proxies. This humility matters for clinical audiences.

### 08 — Pitfalls  *(the credibility notebook; 40 min, highlights)*
- **Patient overlap** is the centrepiece: split the time series randomly by row → inflated AUC; split by
  `icustayid` → honest AUC. Same data, very different number. This single demo prevents a lot of bad papers.
- **Target leakage**: adding `died_in_hosp` as a feature → AUC ≈ 1.0. Then discuss subtle real-world leaks
  (discharge disposition, "comfort care" orders, a lab only ordered when death is expected).
- End on **external validation**: models drop when moved to a new hospital; that's expected, not failure.
- This is the note to finish the taught day on. It's the one that makes them trustworthy researchers.

---

## The flex pool

### 09 — Optimizing your model *(cleaner data & smarter search)*
- **Lead with the honest clean-data test.** It builds the features twice (raw vs cleaned) and compares with
  5-fold CV. The lesson lands *because* it refuses to overclaim: the outlier-sensitive model (Naive Bayes)
  gains clearly, the robust tree model barely moves. Ask the room *"so should we skip cleaning for XGBoost?"*
  then deliver the three reasons to clean anyway (corrupted Table-1 stats, artefact-driven individual
  predictions, reduced variance). This is the antidote to the "cleaning always boosts AUC" myth.
- **Search:** `GridSearchCV` → `RandomizedSearchCV` (budgeted) → a note on `HalvingRandomSearchCV`.
  Emphasise the gain is *small but real*, always CV-scored, and to tune **last**.
- Order-of-impact mantra: **more & cleaner data → better features → right model family → hyperparameters.**

### 10 — Bonus tricks (+ LLM copilot)
- Pure dopamine — let pairs race to apply a trick to the sepsis data. Great end-of-day or filler material.
- The **LLM copilot** section is where you give the prompt recipes and the hard rule —
  **never paste PHI into a public LLM** — and the *verify-always* habit. Aggregate `describe()` tables and
  schema are usually safe; individual rows are not.

### 11 — Reinforcement learning (Q-learning) *(advanced)*
- The "where does this all lead?" finale, mapping onto real sepsis-RL research (Komorowski's *AI Clinician*).
  Frame it as a **shift from *predicting* to *choosing***: NB05 asked "will this patient die?"; NB11 asks
  "what treatment should we give?".
- Spend time on the **offline-RL caveat up front**: we can never experiment on real patients, so we learn
  from logged data — and evaluating such a policy is genuinely hard. Do **not** let anyone leave thinking the
  learned policy is deployable; the honesty section (off-policy evaluation, distribution shift, ethics) is the
  point, not an afterthought. Cite Komorowski 2018 **and** the Gottesman 2019 critique.
- Great discussion prompt: *"the AI suggests more vasopressors than the clinicians did — is that a discovery
  or an artefact of the data?"* (Answer: you can't tell from this alone — that's why off-policy evaluation and
  prospective trials exist.)
- Requires more comfort than the rest of the day; best for a motivated subgroup or as take-home. Prereqs 05–06.

### 12 — When your data is too big for pandas *(reference)*
- A short, information-only sheet for the inevitable question *"but our real dataset is 200 GB — now what?"*.
  It runs three genuine demos on the sample (dtype downcasting halves memory; Parquet is ≈4× smaller than
  CSV; `chunksize` streaming processes the file without loading it) and then tables the escalation path:
  **Parquet + downcast + chunking → Polars / DuckDB (out-of-core) → Dask (parallel) → Spark (cluster)**.
- The message to leave them with: *most laptop "big data" pain is solved without a cluster.* Also lists large
  medical dataset **sources** (MIMIC-IV, eICU, UK Biobank, All of Us, …). Pure take-home.

### 13 ⚖️ — Fairness & subgroup performance *(35 min; the reviewer-proofing notebook)*
- The one-line framing: **"an average is a promise you make to a population, not to a patient."**
- Show the base-rate table *before* any model output. Half of what looks like unfairness later is the model
  correctly reporting that one group is sicker — participants need to see the base rates first to tell the
  difference.
- The **bootstrap CI plot is the point of the notebook.** On ~400 test patients, a 0.05 AUC gap between
  subgroups is usually noise. Reporting "0.81 in men vs 0.75 in women" without intervals is one of the most
  common ways fairness analyses mislead — in *both* directions. Make them look at the overlap.
- Land the **impossibility result** (Chouldechova 2017; Kleinberg 2016): when base rates differ you cannot
  equalise sensitivity, PPV and calibration at once. The equalise-sensitivity cell shows the cost concretely
  — PPV collapses, alert rate doubles. "We optimised fairness" is not a sentence anyone should write.
- The "fairness through unawareness" exercise (drop `age`, gaps persist, performance drops) is the best
  90 seconds in the notebook. Ask them to predict the result before running it.
- Discussion prompt: *"who gets a lactate drawn in your hospital?"* — the model learns ordering behaviour,
  not just biology.

### 14 🏆 — The capstone challenge *(60 min; the best way to end a day)*
- **Logistics:** locked patient-level split, fixed seed 2026 — everyone in the room scores on the identical
  held-out stays, so the leaderboard is real. Pairs work well; four teams is better than twelve.
- Run the three benchmarks live at the front (null model → worst SOFA alone → XGBoost starter), then set
  them loose. **The "worst SOFA alone" benchmark is the important one** — it's the bar a clinical reviewer
  will actually hold them to, and it's closer than people expect.
- **Police the CV habit, not the score.** The rule that matters: cross-validate on training stays, submit
  two or three times all session. Say out loud that a team who submits thirty times has tuned on the test set
  and their number is fiction — that *is* the lesson of Notebook 08, applied under time pressure.
- Anyone reporting **> 0.93 has leaked.** Make finding the leak the prize; it's a better outcome than winning.
- **Leave 10 minutes for the debrief.** The five debrief questions (external validity, what action the score
  triggers, what the winning feature actually encodes, is it fair, is it calibrated) are the real payload.
  Close on: *"getting from 0.78 to 0.83 took an hour. Getting to something that helps a patient takes
  prospective validation, a workflow, and a team."*
- If you want a second round: re-sort the leaderboard by **Brier** instead of AUC and ask whether the winner
  changed. It usually does, and the argument that follows is worth 15 minutes.

---

## 🎁 The "wow" moments to make sure you hit

1. `Temp_F.max()` ≈ 104,109 °F (02) — data quality is real.
2. The diverging survival **trajectory** plot (03/04).
3. One line of pandas turns a timeline into a **rolling feature** (04).
4. **"Why did the model flag this patient?"** SHAP waterfall (07).
5. Random split **0.9+** vs patient split **0.78** — the **leakage** reveal (08).
6. The honest "cleaning helps the *sensitive* model, not the robust one" (09).
7. Subgroup AUCs with **overlapping** confidence intervals (13) — the gap you were about to publish isn't there.
8. The AI **treatment policy** map — escalating pressors as lactate rises (11) — and why we *can't* yet trust it.
9. A team beating the XGBoost starter with **better features, not a better model** (14).

## ❓ Common participant questions

- *"Why not just use accuracy?"* → 06, the imbalance trap.
- *"Can I use my own Excel/CSV?"* → yes: same recipes; match your ID column to `icustayid`, your time
  column to `bloc`/`timestep`, your outcome to `morta_90`. Point them at 01→02→04→05.
- *"Deep learning / LSTMs?"* → out of scope for a one-day intro; the feature-engineering + gradient-boosting
  recipe here is a strong, honest baseline that often matches deep models on tabular ICU data. Mention it.
- *"Is this good enough to use on patients?"* → no — teaching only; needs prospective + external validation.
- *"Do I have to check every subgroup?"* → 13. You check the ones a reviewer will ask about, you report the
  ones you couldn't evaluate, and you never report a gap without a confidence interval.

## 🛠️ Troubleshooting

- **`FileNotFoundError` / "Upload …"** → the CSV isn't in the session; re-run the setup cell and
  upload from `data/`. Locally, keep notebooks next to the `data/` folder.
- **Upload once, reuse everywhere** → on first upload the setup cell offers to connect **Google Drive**
  and caches the file to `MyDrive/sepsis_workshop_data/`; later notebooks (and later sessions) load it
  from there with no re-upload. If a participant declines Drive, they upload per session as before.
  If Drive was connected but a file still isn't found, check they uploaded into that same Drive folder.
- **Nobody should upload at all** → host the CSVs somewhere reachable and have everyone set
  `WORKSHOP_DATA_URL = "https://…/"` at the top of the setup cell. Test the URL yourself first; it must
  serve the files by their exact names.
- **Colab session reset** → re-run the setup cell; with Drive connected the data reloads automatically.
- **`shap`/`xgboost` "installing…"** on first run → normal on Colab (≈20 s), only when missing.
- **A plot looks different** → fine; small dataset + random seeds. Numbers should be in the same ballpark.
- **Someone gets AUC ≈ 1.0** → almost always leakage; use it to teach 08.
- **The "Open in Colab" badge 404s** → check the repo is public and the branch in the badge URL matches
  (`main`). The badges point at `github.com/lorenzkap/ML2026`.

## Adapting to their own research

The fastest path for a participant with their own longitudinal data: (1) rename their columns to match
this schema (patient id, time index, features, outcome); (2) run Notebook 02's cleaning; (3) run
Notebook 04's `build_patient_table` pattern; (4) run Notebook 05; (5) before they believe anything, run
Notebook 08's split check and Notebook 13's subgroup report. Encourage them to keep the
**split-by-patient** and **pipeline** habits — those two alone prevent most beginner mistakes.

## Answer keys

Every exercise ships with a collapsible `<details>💡 Show solution</details>` block in the notebook, so
there is no separate answer key to manage.
