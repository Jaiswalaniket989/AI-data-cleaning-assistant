from src.data_loader import load_dataset
from src.cleaner import clean_dataset


def test_clean_dataset():

    df = load_dataset(
        "data/input/sample_sales.csv"
    )

    cleaned_df, audit_log = clean_dataset(df)

    # Duplicate should be removed
    assert len(cleaned_df) < len(df)

    # Missing values should be reduced
    assert cleaned_df["age"].isna().sum() == 0
    assert cleaned_df["salary"].isna().sum() == 0

    # Cleaning actions should be recorded
    assert len(audit_log) > 0