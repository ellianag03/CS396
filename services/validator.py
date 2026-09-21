import pandas as pd

from services.column_mapping import COLUMN_MAPPING, REQUIRED_COLUMNS


def validate_dataframe(df):
    """
    Validate an uploaded EPA dataset.

    Returns a dictionary containing:
    - whether the file is valid
    - missing required columns
    - extra columns
    - missing-value information
    - invalid-value information
    - duplicate records
    - a preview of the uploaded data
    """

    errors = []
    warnings = []

    # ---------------------------------------------------------
    # 1. Check required columns
    # ---------------------------------------------------------

    missing_columns = [
        column
        for column in REQUIRED_COLUMNS
        if column not in df.columns
    ]

    if missing_columns:
        errors.append(
            f"Missing required columns: {', '.join(missing_columns)}"
        )

    # ---------------------------------------------------------
    # 2. Identify extra columns
    # ---------------------------------------------------------

    extra_columns = [
        column
        for column in df.columns
        if column not in COLUMN_MAPPING
    ]

    if extra_columns:
        warnings.append(
            f"Extra columns found: {', '.join(extra_columns)}"
        )

    # ---------------------------------------------------------
    # 3. Check missing values
    # ---------------------------------------------------------

    missing_values = {}

    for column in REQUIRED_COLUMNS:
        if column in df.columns:
            count = int(df[column].isna().sum())

            if count > 0:
                missing_values[column] = count

    if missing_values:
        warnings.append(
            "Some required fields contain missing values."
        )

    # ---------------------------------------------------------
    # 4. Check numeric columns
    # ---------------------------------------------------------

    numeric_columns = [
        "Year",
        "Facility ID",
        "Operating Time Count",
        "Sum of the Operating Time",
        "Gross Load (MWh)",
        "Steam Load (1000 lb)",
        "SO2 Mass (short tons)",
        "SO2 Rate (lbs/mmBtu)",
        "CO2 Mass (short tons)",
        "CO2 Rate (short tons/mmBtu)",
        "NOx Mass (short tons)",
        "NOx Rate (lbs/mmBtu)",
        "Heat Input (mmBtu)",
    ]

    invalid_numeric_values = {}

    for column in numeric_columns:

        if column not in df.columns:
            continue

        original = df[column]

        converted = pd.to_numeric(
            original,
            errors="coerce"
        )

        invalid_count = int(
            converted.isna().sum() - original.isna().sum()
        )

        if invalid_count > 0:
            invalid_numeric_values[column] = invalid_count

    if invalid_numeric_values:
        errors.append(
            "Some numeric fields contain invalid values."
        )

    # ---------------------------------------------------------
    # 5. Check year values
    # ---------------------------------------------------------

    invalid_year_rows = []

    if "Year" in df.columns:

        years = pd.to_numeric(
            df["Year"],
            errors="coerce"
        )

        invalid_year_rows = df[
            years.isna() |
            (years < 1900) |
            (years > 2100)
        ].index.tolist()

        if invalid_year_rows:
            errors.append(
                f"{len(invalid_year_rows)} record(s) contain "
                "an invalid year."
            )

    # ---------------------------------------------------------
    # 6. Check duplicate facility/unit/year records
    # ---------------------------------------------------------

    duplicate_records = pd.DataFrame()

    required_duplicate_columns = [
        "Facility ID",
        "Unit ID",
        "Year"
    ]

    if all(
        column in df.columns
        for column in required_duplicate_columns
    ):

        duplicate_mask = df.duplicated(
            subset=required_duplicate_columns,
            keep=False
        )

        duplicate_records = df[duplicate_mask]

        if not duplicate_records.empty:
            warnings.append(
                f"{len(duplicate_records)} row(s) belong to "
                "duplicate facility-unit-year records."
            )

    # ---------------------------------------------------------
    # 7. Determine overall validity
    # ---------------------------------------------------------

    is_valid = len(errors) == 0

    # ---------------------------------------------------------
    # 8. Create preview
    # ---------------------------------------------------------

    preview = df.head(10).fillna("").to_dict(
        orient="records"
    )

    return {
        "is_valid": is_valid,
        "errors": errors,
        "warnings": warnings,
        "missing_columns": missing_columns,
        "extra_columns": extra_columns,
        "missing_values": missing_values,
        "invalid_numeric_values": invalid_numeric_values,
        "invalid_year_rows": invalid_year_rows,
        "duplicate_records": duplicate_records.to_dict(
            orient="records"
        ),
        "row_count": len(df),
        "column_count": len(df.columns),
        "preview": preview,
    }