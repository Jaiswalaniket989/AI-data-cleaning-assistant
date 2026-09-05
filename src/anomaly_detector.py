import pandas as pd
import numpy as np


def detect_missing_values(df):
    """
    Detect missing values in each column.
    """

    issues = []

    for column in df.columns:
        missing_count = int(df[column].isna().sum())

        if missing_count > 0:
            percentage = round(
                (missing_count / len(df)) * 100, 2
            )

            issues.append({
                "type": "missing_values",
                "column": column,
                "count": missing_count,
                "percentage": percentage,
                "severity": (
                    "high" if percentage >= 30
                    else "medium" if percentage >= 10
                    else "low"
                )
            })

    return issues


def detect_duplicates(df):
    """
    Detect duplicate rows.
    """

    duplicate_count = int(df.duplicated().sum())

    if duplicate_count == 0:
        return []

    return [{
        "type": "duplicate_rows",
        "count": duplicate_count,
        "severity": "medium"
    }]


def detect_outliers(df):
    """
    Detect numerical outliers using the IQR method.
    """

    issues = []

    numeric_columns = df.select_dtypes(
        include=np.number
    ).columns

    for column in numeric_columns:

        series = df[column].dropna()

        if len(series) < 4:
            continue

        q1 = series.quantile(0.25)
        q3 = series.quantile(0.75)

        iqr = q3 - q1

        if iqr == 0:
            continue

        lower_bound = q1 - 1.5 * iqr
        upper_bound = q3 + 1.5 * iqr

        outliers = df[
            (df[column] < lower_bound) |
            (df[column] > upper_bound)
        ]

        if len(outliers) > 0:

            issues.append({
                "type": "outliers",
                "column": column,
                "count": int(len(outliers)),
                "lower_bound": float(lower_bound),
                "upper_bound": float(upper_bound),
                "severity": "medium"
            })

    return issues


def detect_category_inconsistencies(df):
    """
    Detect possible inconsistencies in categorical/text columns.
    """

    issues = []

    categorical_columns = df.select_dtypes(
        include=["object", "string"]
    ).columns

    for column in categorical_columns:

        values = (
            df[column]
            .dropna()
            .astype(str)
            .str.strip()
        )

        normalized = values.str.lower()

        groups = {}

        for original, normal in zip(values, normalized):
            groups.setdefault(normal, set()).add(original)

        for normalized_value, variants in groups.items():

            if len(variants) > 1:

                issues.append({
                    "type": "category_inconsistency",
                    "column": column,
                    "variants": list(variants),
                    "suggested_value": normalized_value.title(),
                    "severity": "low"
                })

    return issues


def detect_all_anomalies(df):
    """
    Run all anomaly detectors.
    """

    issues = []

    issues.extend(
        detect_missing_values(df)
    )

    issues.extend(
        detect_duplicates(df)
    )

    issues.extend(
        detect_outliers(df)
    )

    issues.extend(
        detect_category_inconsistencies(df)
    )

    return issues