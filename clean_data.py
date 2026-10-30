"""
SWYNEX Task 1: Data Cleaning & Preparation
Dataset: Public Titanic passenger dataset (DataScienceDojo GitHub mirror)

Run:
    pip install -r requirements.txt
    python src/clean_data.py

The script downloads the full public dataset and creates:
    data/titanic_cleaned.csv
    data/cleaning_report.txt
"""
from pathlib import Path
import pandas as pd

PROJECT_DIR = Path(__file__).resolve().parents[1]
DATA_DIR = PROJECT_DIR / "data"
DATA_DIR.mkdir(exist_ok=True)

DATASET_URL = "https://raw.githubusercontent.com/datasciencedojo/datasets/master/titanic.csv"
RAW_FILE = DATA_DIR / "titanic_raw.csv"
CLEAN_FILE = DATA_DIR / "titanic_cleaned.csv"
REPORT_FILE = DATA_DIR / "cleaning_report.txt"

def main():
    print("Downloading the public Titanic dataset...")
    df = pd.read_csv(DATASET_URL)
    rows_before = len(df)
    missing_before = df.isna().sum().to_dict()

    # 1. Remove fully duplicated rows.
    duplicate_count = int(df.duplicated().sum())
    df = df.drop_duplicates().copy()

    # 2. Clean text columns to avoid inconsistent spaces/capitalization.
    for col in df.select_dtypes(include=["object"]).columns:
        df[col] = df[col].astype("string").str.strip()

    if "Sex" in df.columns:
        df["Sex"] = df["Sex"].str.lower()
    if "Embarked" in df.columns:
        df["Embarked"] = df["Embarked"].str.upper()

    # 3. Convert columns to suitable data types.
    for col in ["Age", "Fare", "SibSp", "Parch", "Pclass", "Survived", "PassengerId"]:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")

    # 4. Handle missing values using sensible, documented choices.
    if "Age" in df.columns:
        df["Age"] = df["Age"].fillna(df["Age"].median())
    if "Fare" in df.columns:
        df["Fare"] = df["Fare"].fillna(df["Fare"].median())
    if "Embarked" in df.columns and df["Embarked"].notna().any():
        df["Embarked"] = df["Embarked"].fillna(df["Embarked"].mode().iloc[0])

    # 5. Cabin has many missing values; drop it for this introductory task.
    # This is a documented project choice, not the only possible approach.
    dropped_columns = []
    if "Cabin" in df.columns:
        df = df.drop(columns=["Cabin"])
        dropped_columns.append("Cabin (many missing values)")

    # 6. Check for missing values left in the output.
    # Remaining missing values are filled only where a reasonable rule exists.
    # Keep the report transparent if any other columns still contain nulls.
    df.to_csv(CLEAN_FILE, index=False)

    missing_after = df.isna().sum().to_dict()
    report = [
        "SWYNEX - Data Cleaning & Preparation Report",
        "=" * 46,
        f"Dataset source: {DATASET_URL}",
        f"Rows before cleaning: {rows_before}",
        f"Rows after duplicate removal: {len(df)}",
        f"Duplicate rows removed: {duplicate_count}",
        "",
        "Missing values before cleaning:",
    ]
    report += [f"  {k}: {v}" for k, v in missing_before.items()]
    report += ["", "Missing values after cleaning:"]
    report += [f"  {k}: {v}" for k, v in missing_after.items()]
    report += ["", "Actions performed:",
               "- Removed fully duplicated rows.",
               "- Trimmed extra spaces from text columns.",
               "- Standardized Sex to lowercase and Embarked to uppercase.",
               "- Converted numeric fields to numeric data types.",
               "- Filled missing Age and Fare with their medians.",
               "- Filled missing Embarked with its mode.",
               "- Dropped Cabin because it has many missing values."]
    if dropped_columns:
        report += ["", "Dropped columns: " + ", ".join(dropped_columns)]
    report += ["", f"Cleaned file: {CLEAN_FILE.name}",
               "Note: median/mode imputation is a simple beginner-friendly choice; explain it in your submission."]
    REPORT_FILE.write_text("\n".join(report), encoding="utf-8")

    print(f"Rows before cleaning: {rows_before}")
    print(f"Rows after cleaning:  {len(df)}")
    print(f"Duplicate rows removed: {duplicate_count}")
    print(f"Saved cleaned dataset to: {CLEAN_FILE}")
    print(f"Saved cleaning report to: {REPORT_FILE}")

if __name__ == "__main__":
    main()
