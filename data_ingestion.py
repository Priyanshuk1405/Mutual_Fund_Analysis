"""
data_ingestion.py
Bluestock Fintech — Mutual Fund Analytics Capstone | Day 1
Loads all 10 provided CSV datasets, prints shape/dtypes/head,
and flags any obvious anomalies.
"""

import pandas as pd
from pathlib import Path
from tabulate import tabulate


pd.set_option("display.max_columns", None)
pd.set_option("display.width", 200)
pd.set_option("display.max_colwidth", 50)


RAW_DIR = Path("/Users/priyanshukansara/Downloads/Bluestock_MF_Datasets/data/raw")


DATASETS = {
    "01_fund_master":          "01_fund_master.csv",
    "02_nav_history":          "02_nav_history.csv",
    "03_aum_by_fund_house":    "03_aum_by_fund_house.csv",
    "04_monthly_sip_inflows":  "04_monthly_sip_inflows.csv",
    "05_category_inflows":     "05_category_inflows.csv",
    "06_industry_folio_count": "06_industry_folio_count.csv",
    "07_scheme_performance":   "07_scheme_performance.csv",
    "08_investor_transactions":"08_investor_transactions.csv",
    "09_portfolio_holdings":   "09_portfolio_holdings.csv",
    "10_benchmark_indices":    "10_benchmark_indices.csv",
}


def load_and_inspect(name: str, filename: str) -> pd.DataFrame | None:
    """Load a single CSV and print a diagnostic summary."""
    filepath = Path(RAW_DIR) / filename

    print(f"\n{'-' * 50}")
    print(f"  {name}  →  {filename}")
    print(f"{'-' * 50}")

    if not filepath.exists():
        print(f" [WARNING] File not found: {filepath}")
        print(f" Place the CSV in:  data/raw/{filename}")
        return None

    df = pd.read_csv(filepath)

    print(f"\nShape : {df.shape[0]:,} rows  ×  {df.shape[1]} columns")
    print(f"\nColumn types:")
    for col, dtype in df.dtypes.items():
        print(f"  {col:<35} {str(dtype):<12}")


    print(f"\nFirst 3 rows:")
    print(df.head(5))


    '''
    check for anomalies : find irregularity in the data 
    for example null values, duplicate rows, negative or zero values in numeric columns 
    where it doesn't make sense (like NAV or amount_inr).
    '''
    anomalies = []

    total_nulls = df.isna().sum().sum()
    if total_nulls:
        anomalies.append(f"Total null cells : {total_nulls}")

    dup_count = df.duplicated().sum()
    if dup_count:
        anomalies.append(f"Duplicate rows : {dup_count}")

    if "nav" in df.columns:
        bad_nav = (df["nav"] <= 0).sum()
        if bad_nav:
            anomalies.append(f"NAV ≤ 0 rows   : {bad_nav}")

    if "amount_inr" in df.columns:
        bad_amt = (df["amount_inr"] <= 0).sum()
        if bad_amt:
            anomalies.append(f"amount_inr ≤ 0   : {bad_amt}")

    if anomalies:
        print(f"\n[ANOMALIES DETECTED]")
        for a in anomalies:
            print(f"  ⚠  {a}")
    else:
        print(f"\n  ✓  No anomalies detected")

    return df


def main():
    print(f"\n{'*' * 65}")
    print(f" Bluestock Fintech — Data Ingestion (Day 1)")
    print(f" Loading from: {RAW_DIR}")
    print(f"{'*' * 65}")

    dataframes: dict[str, pd.DataFrame] = {}
    missing = []

    for name, filename in DATASETS.items():
        df = load_and_inspect(name, filename)
        if df is not None:
            dataframes[name] = df
        else:
            missing.append(filename)

    print(f"\n\n{'*' * 65}")
    print(f"SUMMARY")
    print(f"{'*' * 65}")
    print(f" Loaded successfully : {len(dataframes)} / {len(DATASETS)} datasets")
    if missing:
        print(f"\n Missing files (place in data/raw/):")
        for f in missing:
            print(f"    - {f}")
    else:
        print(f" All datasets present ✓")

    total_rows = sum(df.shape[0] for df in dataframes.values())
    print(f"\n Total rows across all datasets : {total_rows:,}")


if __name__ == "__main__":
    main()