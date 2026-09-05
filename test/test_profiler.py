from src.data_loader import load_dataset
from src.profiler import profile_dataset


def test_profile_dataset():

    df = load_dataset("data/input/sample_sales.csv")

    profile = profile_dataset(df)

    assert profile["rows"] == 8
    assert profile["columns"] == 4
    assert profile["duplicate_rows"] == 1
    assert profile["missing_values"]["age"] == 1
    assert profile["missing_values"]["salary"] == 1