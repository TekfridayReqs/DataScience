# Credit Risk Modelling Assessment

Ten tasks to assess whether a candidate can build a credit (probability-of-default) model end to end. They progress from data understanding to a deployable scorecard and a business decision, mirroring how a real PD model is built.

**Dataset**: `credit_risk_dataset.csv`, available in the notebook environment at `/home/jovyan/data/credit_risk_dataset.csv`. Columns:

| Column | Meaning |
|---|---|
| `person_age` | Applicant age (years) |
| `person_income` | Annual income |
| `person_home_ownership` | RENT / MORTGAGE / OWN / OTHER |
| `person_emp_length` | Employment length (years) |
| `loan_intent` | PERSONAL / EDUCATION / MEDICAL / VENTURE / HOMEIMPROVEMENT / DEBTCONSOLIDATION |
| `loan_grade` | Internal grade A (best) to G (worst) |
| `loan_amnt` | Loan amount |
| `loan_int_rate` | Interest rate (%) |
| `loan_status` | **Target**: 1 = default, 0 = repaid |
| `loan_percent_income` | Loan amount as a fraction of income |
| `cb_person_default_on_file` | Prior default on credit bureau file (Y/N) |
| `cb_person_cred_hist_length` | Credit history length (years) |

Candidates may answer in **Python or R** (both kernels are available). Suggested packages are noted per question but candidates should use whatever they prefer.

---

## Question 1 — Data quality audit and target definition

Load the dataset, confirm `loan_status` as the modelling target, and produce a data quality assessment. Quantify missing values, identify implausible records (for example, ages and employment lengths far outside a believable range), and report the class balance of the target. Decide how you would treat each issue and justify it.

Strong answers separate genuinely missing data from data-entry errors, justify imputation or capping choices rather than deleting rows reflexively, and recognise that the target is imbalanced and that this will shape evaluation later.

## Question 2 — Exploratory risk analysis

Investigate which applicant and loan characteristics relate to default. Compute observed default rates across `loan_grade`, `loan_intent`, `person_home_ownership`, `cb_person_default_on_file`, and sensible bands of income, age, and `loan_percent_income`. Visualise the relationships and state which features look most predictive and why.

Strong answers use bivariate default-rate tables (not just correlations), check whether risk moves monotonically with ordered features such as `loan_grade`, and translate the patterns into a plausible business narrative.

## Question 3 — Preprocessing pipeline without leakage

Build a reproducible preprocessing pipeline: impute missing values, treat outliers, and encode categoricals (handling `loan_grade` as ordered). The pipeline must be fit on training data only and applied to validation/test data, with no leakage.

Strong answers use a structured, re-runnable pipeline (`scikit-learn` `Pipeline`/`ColumnTransformer`, or R `recipes`), fit all learned parameters on the training split alone, and can articulate exactly where leakage would otherwise creep in.

## Question 4 — Sampling design and class imbalance

Create an appropriate train/validation/test split and address the class imbalance. Explain your split strategy, why an out-of-time split would be preferable in a production credit setting, and how you handle imbalance (class weights, resampling, or threshold adjustment) without distorting evaluation.

Strong answers stratify the split, explain why plain accuracy is misleading on imbalanced default data, and apply any resampling inside cross-validation folds rather than before splitting.

## Question 5 — Weight of Evidence binning and Information Value

Engineer features using Weight of Evidence (WoE) and rank their predictive power with Information Value (IV). Bin continuous and categorical variables into monotonic, business-sensible groups, compute IV per feature, and decide which features to keep.

Strong answers produce monotonic or otherwise justifiable bins, compute WoE/IV correctly, handle rare categories and missing bins, and use IV thresholds to drop weak features. (Python: `optbinning`, `scorecardpy`. R: `scorecard`, `smbinning`.)

## Question 6 — Probability-of-default model with logistic regression

Fit a logistic regression PD model (on WoE-transformed or properly encoded features). Interpret the coefficients as odds ratios, confirm the signs make business sense, and check for multicollinearity. Explain why logistic regression remains the default in regulated credit modelling.

Strong answers interpret coefficients in risk terms, check VIF or similar, prefer a parsimonious model, and connect interpretability and monotonicity to regulatory expectations.

## Question 7 — Challenger machine-learning model and trade-offs

Build a challenger model (gradient boosting or random forest) and compare its discrimination against the logistic model. Discuss the interpretability-versus-performance trade-off and how you would explain a machine-learning model's decisions in a lending context.

Strong answers compare models fairly on held-out data, recognise that a higher AUC does not automatically win in regulated lending, and propose explainability approaches (such as SHAP) and adverse-action reasoning.

## Question 8 — Evaluation with credit-specific metrics

Evaluate your models with the metrics used in credit risk: ROC-AUC, Gini, and the Kolmogorov-Smirnov (KS) statistic, plus rank-ordering across score bands (decile lift) and a confusion matrix at a chosen cut-off. Explain why these are preferred over raw accuracy.

Strong answers compute KS and Gini correctly, demonstrate monotonic rank-ordering across score deciles, and distinguish discrimination (ranking) from calibration (probability accuracy).

## Question 9 — Calibration and scorecard creation

Calibrate the predicted probabilities and convert the logistic model into a points-based scorecard. Choose a base score, base odds, and points-to-double-the-odds (PDO), derive the scaling factor and offset, and produce the per-attribute points and a total-score-to-PD mapping.

Strong answers apply correct scorecard scaling (factor and offset from PDO and base odds), produce an interpretable points table, and validate calibration (for example, a reliability curve or Hosmer-Lemeshow test).

## Question 10 — Decisioning, monitoring, and governance

Set an approval cut-off score given a stated risk appetite. Estimate the resulting approval rate and expected bad rate, frame the decision in expected-loss or simple profit terms, and outline how you would monitor the model after deployment and what governance and fairness issues you would watch for.

Strong answers tie the cut-off to a business profit-and-loss view, name population stability (PSI) and score-drift monitoring, and raise fairness, explainability, and reject-inference considerations for production use.

---

### How to score

Each task carries explicit "strong answers" cues above. A practical rubric is to score each question 0–3 (0 absent, 1 attempted, 2 competent, 3 expert) across correctness, sound methodology, and clarity of reasoning. Questions 5, 6, 9, and 10 are the strongest signal of genuine credit-modelling expertise as opposed to generic machine-learning skill.
