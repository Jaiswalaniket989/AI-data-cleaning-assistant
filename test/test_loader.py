from src.data_loader import load_dataset


def test_load_csv():
    df = load_dataset("data/input/sample_sales.csv")

    assert not df.empty
    assert len(df) == 8
    assert "customer" in df.columns
    assert "salary" in df.columns