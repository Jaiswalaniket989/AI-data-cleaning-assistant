from src.data_loader import load_dataset
from src.cleaner import clean_dataset


def main():

    df = load_dataset(
        "data/input/sample_sales.csv"
    )

    cleaned_df, audit_log = clean_dataset(df)

    print("\n========== CLEANING REPORT ==========\n")

    print(f"Original rows : {len(df)}")
    print(f"Cleaned rows  : {len(cleaned_df)}")

    print("\nMissing values BEFORE:")
    print(df.isna().sum())

    print("\nMissing values AFTER:")
    print(cleaned_df.isna().sum())

    print("\nAudit Log:")

    for change in audit_log:
        print(change)


if __name__ == "__main__":
    main()