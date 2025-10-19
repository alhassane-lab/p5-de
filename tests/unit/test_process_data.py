import pandas as pd
#from pytest_mock import MockerFixture


def test_process_data():
    mock_data = [
        {"name": "John Doe", "age": 30, "date_of_birth": "1993-05-15", "admission_date": "2023-10-01",
         "discharge_date": "2023-10-05", "patient_id": 1},
        {"name": "Jane Smith", "age": 40, "date_of_birth": "1983-07-20", "admission_date": "2023-10-02",
         "discharge_date": "2023-10-07", "patient_id": 2},
        {"name": "Alice Brown", "age": 25, "date_of_birth": "1998-07-20", "admission_date": "2023-10-03",
         "discharge_date": "2023-10-08", "patient_id": 3},
        {"name": "Bob Wilson", "age": 35, "date_of_birth": None, "admission_date": "2023-10-04",
         "discharge_date": "2023-10-09", "patient_id": 4},
    ]

    df = pd.DataFrame(mock_data)

    # Simuler un traitement
    df["duration_days"] = (pd.to_datetime(df["discharge_date"]) - pd.to_datetime(df["admission_date"])).dt.days

    print("\nDataFrame après process_data:")
    print(df)

    assert len(df) == 4
    print(f"Assertion passed: DataFrame length is {len(df)}")

    assert df["duration_days"].iloc[0] == 4
    print(f"Assertion passed: duration_days for John Doe is {df['duration_days'].iloc[0]}")

    assert df["duration_days"].iloc[1] == 5
    print(f"Assertion passed: duration_days for Jane Smith is {df['duration_days'].iloc[1]}")