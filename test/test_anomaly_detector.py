from src.data_loader import load_dataset
from src.anomaly_detector import detect_all_anomalies


def test_anomaly_detection():

    df = load_dataset(
        "data/input/sample_sales.csv"
    )

    issues = detect_all_anomalies(df)

    assert len(issues) > 0

    issue_types = {
        issue["type"]
        for issue in issues
    }

    assert "missing_values" in issue_types
    assert "duplicate_rows" in issue_types
    assert "outliers" in issue_types
    assert "category_inconsistency" in issue_types