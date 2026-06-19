"""Replace the synthetic dataset with the real Kaggle credit-risk data.

Requires Kaggle API credentials. Set them as environment variables before
running, or place a kaggle.json in ~/.kaggle/:

    export KAGGLE_USERNAME=your_username
    export KAGGLE_KEY=your_api_key

Then run inside the single-user container (or bake into the image at build time):

    python /home/jovyan/scripts/load_kaggle_data.py

This loads "absuag/credit-risk-modelling" and writes it to the same path the
synthetic generator uses, so notebooks and questions are unaffected.
"""
import os
import kagglehub
from kagglehub import KaggleDatasetAdapter

OUT = "/home/jovyan/data/credit_risk_dataset.csv"

# file_path = "" loads the dataset's single/primary file. If the dataset has
# multiple files, set file_path to the specific CSV you want.
df = kagglehub.load_dataset(
    KaggleDatasetAdapter.PANDAS,
    "absuag/credit-risk-modelling",
    "",
)

os.makedirs(os.path.dirname(OUT), exist_ok=True)
df.to_csv(OUT, index=False)
print(f"Wrote {len(df)} rows from Kaggle to {OUT}")
print("Columns:", list(df.columns))
