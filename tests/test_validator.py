import pandas as pd

from services.validator import (
    validate_columns,
    validate_values,
    find_duplicates
)


def test_required_columns():

    df = pd.DataFrame({
        "EPA_FACILITY_ID": [100],
        "FACILITY_NAME": ["Test Plant"],
        "STATE": ["KY"],
        "COUNTY": ["Allen"],
        "UNIT_ID": ["1"],
        "REPORTING_YEAR": [2025],
        "OPERATING_TIME": [5000],
        "GROSS_LOAD_MWH": [100000],
        "HEAT_INPUT_MMBTU": [500000],
        "CO2_SHORT_TON": [500000],
        "SO2_SHORT_TON": [100],
        "NOX_SHORT_TON": [50]
    })

    result = validate_columns(df)

    assert result["valid"] is True


def test_negative_value():

    df = pd.DataFrame({
        "OPERATING_TIME": [-10]
    })

    result = validate_values(df)

    assert len(result["errors"]) > 0


def test_duplicate_detection():

    df = pd.DataFrame({
        "EPA_FACILITY_ID": [100, 100],
        "UNIT_ID": ["1", "1"],
        "REPORTING_YEAR": [2025, 2025]
    })

    duplicates = find_duplicates(df)

    assert len(duplicates) == 2