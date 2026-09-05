import pandas as pd
import numpy as np


def remove_duplicates(df):
    """
    Remove duplicate rows and record the number removed.
    """

    before = len(df)

    cleaned_df = df.drop_duplicates().copy()

    removed = before - len(cleaned_df)

    return cleaned_df, removed


def fill_numeric_missing_values(df, columns=None):
    """
    Fill missing numeric values using the median.
    """

    cleaned_df = df.copy()
    changes = []

    if columns is None:
        columns = cleaned_df.select_dtypes(
            include=np.number
        ).columns

    for column in columns:

        if column not in cleaned_df.columns:
            continue

        missing_before = int(
            cleaned_df[column].isna().sum()
        )

        if missing_before == 0:
            continue

        median_value = cleaned_df[column].median()

        if pd.isna(median_value):
            continue

        cleaned_df[column] = (
            cleaned_df[column]
            .fillna(median_value)
        )

        changes.append({
            "action": "median_imputation",
            "column": column,
            "rows_affected": missing_before,
            "value_used": float(median_value),
            "status": "completed"
        })

    return cleaned_df, changes


def fill_categorical_missing_values(df, columns=None):
    """
    Fill missing categorical values using the mode.
    """

    cleaned_df = df.copy()
    changes = []

    if columns is None:
        columns = cleaned_df.select_dtypes(
            include=[
                "object",
                "string",
                "category"
            ]
        ).columns

    for column in columns:

        if column not in cleaned_df.columns:
            continue

        missing_before = int(
            cleaned_df[column].isna().sum()
        )

        if missing_before == 0:
            continue

        mode_values = (
            cleaned_df[column]
            .mode()
        )

        if mode_values.empty:
            continue

        mode_value = mode_values.iloc[0]

        cleaned_df[column] = (
            cleaned_df[column]
            .fillna(mode_value)
        )

        changes.append({
            "action": "mode_imputation",
            "column": column,
            "rows_affected": missing_before,
            "value_used": str(mode_value),
            "status": "completed"
        })

    return cleaned_df, changes


def standardize_categories(df):
    """
    Standardize categorical text values.

    Example:
        MUMBAI -> Mumbai
        mumbai -> Mumbai
        Mumbai -> Mumbai
    """

    cleaned_df = df.copy()
    changes = []

    categorical_columns = (
        cleaned_df
        .select_dtypes(
            include=[
                "object",
                "string"
            ]
        )
        .columns
    )

    for column in categorical_columns:

        original_values = (
            cleaned_df[column]
            .copy()
        )

        cleaned_df[column] = (
            cleaned_df[column]
            .astype("string")
            .str.strip()
        )

        non_null_values = (
            cleaned_df[column]
            .dropna()
            .unique()
        )

        mapping = {}

        for value in non_null_values:

            normalized = str(value).lower()

            mapping[value] = (
                normalized.title()
            )

        cleaned_df[column] = (
            cleaned_df[column]
            .map(mapping)
            .fillna(cleaned_df[column])
        )

        changed_rows = int(
            (
                original_values.astype("string")
                != cleaned_df[column].astype("string")
            ).sum()
        )

        if changed_rows > 0:

            changes.append({
                "action": "standardize_categories",
                "column": column,
                "rows_affected": changed_rows,
                "status": "completed"
            })

    return cleaned_df, changes


def convert_numeric_columns(df, columns):
    """
    Convert selected columns to numeric.
    """

    cleaned_df = df.copy()
    changes = []

    for column in columns:

        if column not in cleaned_df.columns:
            continue

        original_dtype = str(
            cleaned_df[column].dtype
        )

        cleaned_df[column] = (
            pd.to_numeric(
                cleaned_df[column],
                errors="coerce"
            )
        )

        new_dtype = str(
            cleaned_df[column].dtype
        )

        if original_dtype != new_dtype:

            changes.append({
                "action": "convert_to_numeric",
                "column": column,
                "old_dtype": original_dtype,
                "new_dtype": new_dtype,
                "status": "completed"
            })

    return cleaned_df, changes


def cap_outliers_iqr(df, columns=None):
    """
    Cap numerical outliers using the IQR method.
    """

    cleaned_df = df.copy()
    changes = []

    if columns is None:

        columns = (
            cleaned_df
            .select_dtypes(
                include=np.number
            )
            .columns
        )

    for column in columns:

        if column not in cleaned_df.columns:
            continue

        series = (
            cleaned_df[column]
            .dropna()
        )

        if len(series) < 4:
            continue

        q1 = series.quantile(0.25)
        q3 = series.quantile(0.75)

        iqr = q3 - q1

        if iqr == 0:
            continue

        lower_bound = (
            q1 - 1.5 * iqr
        )

        upper_bound = (
            q3 + 1.5 * iqr
        )

        outlier_mask = (
            (cleaned_df[column] < lower_bound)
            |
            (cleaned_df[column] > upper_bound)
        )

        outlier_count = int(
            outlier_mask.sum()
        )

        if outlier_count == 0:
            continue

        cleaned_df[column] = (
            cleaned_df[column]
            .clip(
                lower=lower_bound,
                upper=upper_bound
            )
        )

        changes.append({
            "action": "iqr_outlier_capping",
            "column": column,
            "rows_affected": outlier_count,
            "lower_bound": float(
                lower_bound
            ),
            "upper_bound": float(
                upper_bound
            ),
            "status": "completed"
        })

    return cleaned_df, changes


def clean_dataset(df):
    """
    Run the complete data-cleaning pipeline
    and generate a detailed audit log.
    """

    cleaned_df = df.copy()

    audit_log = []

    # ========================================================
    # 1. REMOVE DUPLICATES
    # ========================================================

    rows_before = len(cleaned_df)

    cleaned_df, removed = (
        remove_duplicates(
            cleaned_df
        )
    )

    if removed > 0:

        audit_log.append({
            "action": "remove_duplicates",
            "column": "ALL",
            "rows_affected": removed,
            "details": (
                f"{removed} duplicate row(s) removed"
            ),
            "status": "completed"
        })


    # ========================================================
    # 2. NUMERIC MISSING VALUES
    # ========================================================

    cleaned_df, changes = (
        fill_numeric_missing_values(
            cleaned_df
        )
    )

    audit_log.extend(changes)


    # ========================================================
    # 3. CATEGORICAL MISSING VALUES
    # ========================================================

    cleaned_df, changes = (
        fill_categorical_missing_values(
            cleaned_df
        )
    )

    audit_log.extend(changes)


    # ========================================================
    # 4. STANDARDIZE CATEGORIES
    # ========================================================

    cleaned_df, changes = (
        standardize_categories(
            cleaned_df
        )
    )

    audit_log.extend(changes)


    # ========================================================
    # 5. HANDLE OUTLIERS
    # ========================================================

    cleaned_df, changes = (
        cap_outliers_iqr(
            cleaned_df
        )
    )

    audit_log.extend(changes)


    # ========================================================
    # ADD FINAL SUMMARY
    # ========================================================

    rows_after = len(cleaned_df)

    total_changes = len(audit_log)

    summary = {
        "action": "cleaning_summary",
        "column": "ALL",
        "rows_before": rows_before,
        "rows_after": rows_after,
        "rows_removed": (
            rows_before - rows_after
        ),
        "total_actions": total_changes,
        "status": "completed"
    }

    audit_log.append(summary)


    return cleaned_df, audit_log