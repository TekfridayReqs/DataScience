"""Generate a synthetic credit_risk_dataset.csv that matches the schema and
quirks of the Kaggle credit-risk dataset, so the platform runs out of the box.

Replace this with the real Kaggle data using load_kaggle_data.py once you have
Kaggle API credentials. The columns and their behaviour are designed to mirror
the real file (including some missing values and implausible outliers) so the
assessment questions about data quality remain meaningful.
"""
import os
import numpy as np
import pandas as pd

N = 30000
OUT = "/home/jovyan/data/credit_risk_dataset.csv"

rng = np.random.default_rng(42)

home = rng.choice(["RENT", "MORTGAGE", "OWN", "OTHER"], N, p=[0.50, 0.41, 0.08, 0.01])
intent = rng.choice(
    ["EDUCATION", "MEDICAL", "PERSONAL", "VENTURE", "HOMEIMPROVEMENT", "DEBTCONSOLIDATION"],
    N, p=[0.20, 0.19, 0.18, 0.17, 0.13, 0.13],
)
grade = rng.choice(list("ABCDEFG"), N, p=[0.33, 0.32, 0.20, 0.10, 0.03, 0.015, 0.005])

age = rng.normal(28, 6, N).clip(20, 70).round().astype(int)
income = (rng.lognormal(11.0, 0.5, N)).round().astype(int).clip(4000, 6_000_000)
emp_length = rng.gamma(2.0, 2.0, N).clip(0, 40).round(1)
amount = (rng.lognormal(9.0, 0.5, N)).round(-2).astype(int).clip(500, 35000)

grade_rate = {"A": 7.0, "B": 10.5, "C": 13.0, "D": 15.5, "E": 17.5, "F": 19.0, "G": 21.0}
int_rate = np.array([grade_rate[g] for g in grade]) + rng.normal(0, 1.2, N)
int_rate = int_rate.round(2).clip(5.0, 24.0)

pct_income = (amount / income).round(2).clip(0, 0.85)
prior_default = rng.choice(["Y", "N"], N, p=[0.18, 0.82])
cred_hist = rng.gamma(3.0, 2.0, N).clip(1, 30).round().astype(int)

# Default probability driven by sensible risk factors, then sample the target.
grade_risk = {"A": -1.6, "B": -0.9, "C": -0.2, "D": 0.5, "E": 1.1, "F": 1.6, "G": 2.1}
logit = (
    -1.8
    + np.array([grade_risk[g] for g in grade])
    + 0.05 * (int_rate - 11)
    + 2.2 * (pct_income - 0.15)
    + np.where(prior_default == "Y", 0.8, 0.0)
    + np.where(home == "RENT", 0.25, 0.0)
    - 0.000002 * (income - 60000)
)
prob = 1 / (1 + np.exp(-logit))
status = (rng.random(N) < prob).astype(int)

df = pd.DataFrame({
    "person_age": age,
    "person_income": income,
    "person_home_ownership": home,
    "person_emp_length": emp_length,
    "loan_intent": intent,
    "loan_grade": grade,
    "loan_amnt": amount,
    "loan_int_rate": int_rate,
    "loan_status": status,
    "loan_percent_income": pct_income,
    "cb_person_default_on_file": prior_default,
    "cb_person_cred_hist_length": cred_hist,
})

# Inject the real dataset's known quirks so the data-quality task has substance.
miss_rate = rng.choice(df.index, int(0.095 * N), replace=False)
df.loc[miss_rate, "loan_int_rate"] = np.nan          # ~9.5% missing interest rate
miss_emp = rng.choice(df.index, int(0.027 * N), replace=False)
df.loc[miss_emp, "person_emp_length"] = np.nan        # ~2.7% missing emp length
outlier_age = rng.choice(df.index, 5, replace=False)
df.loc[outlier_age, "person_age"] = rng.integers(123, 145, 5)   # implausible ages
outlier_emp = rng.choice(df.index, 2, replace=False)
df.loc[outlier_emp, "person_emp_length"] = rng.integers(100, 124, 2)  # implausible tenure

os.makedirs(os.path.dirname(OUT), exist_ok=True)
df.to_csv(OUT, index=False)
print(f"Wrote {len(df)} rows to {OUT}")
print(f"Default rate: {df['loan_status'].mean():.3f}")
