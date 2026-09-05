import pandas as pd


def profile_dataset(df):
    """
    Generate a basic data quality profile.
    """

    profile = {
        "rows": len(df),
        "columns": len(df.columns),
        "column_names": list(df.columns),
        "missing_values": df.isnull().sum().to_dict(),
        "duplicate_rows": int(df.duplicated().sum()),
        "data_types": df.dtypes.astype(str).to_dict(),
        "unique_values": df.nunique().to_dict(),
    }

    numeric_columns = df.select_dtypes(
        include="number"
    ).columns

    profile["numeric_statistics"] = (
        df[numeric_columns]
        .describe()
        .to_dict()
    )

    return profile