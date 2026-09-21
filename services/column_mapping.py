# Maps column names from the uploaded EPA CSV
# to the field names used by our database models.

COLUMN_MAPPING = {
    "State": "state",
    "Facility Name": "facility_name",
    "Facility ID": "epa_facility_id",
    "Unit ID": "epa_unit_id",
    "Year": "reporting_year",

    "Operating Time Count": "operating_time_count",
    "Sum of the Operating Time": "operating_time",

    "Gross Load (MWh)": "gross_load_mwh",
    "Steam Load (1000 lb)": "steam_load",

    "SO2 Mass (short tons)": "so2_short_ton",
    "CO2 Mass (short tons)": "co2_short_ton",
    "NOx Mass (short tons)": "nox_short_ton",

    "Heat Input (mmBtu)": "heat_input_mmbtu",

    "Primary Fuel Type": "primary_fuel",
    "Secondary Fuel Type": "secondary_fuel",
    "Unit Type": "unit_type",

    "SO2 Controls": "so2_control",
    "NOx Controls": "nox_control",
    "PM Controls": "pm_control",

    "Program Code": "program_code",
}


# Columns that must be present for an upload
REQUIRED_COLUMNS = [
    "State",
    "Facility Name",
    "Facility ID",
    "Unit ID",
    "Year",
    "Gross Load (MWh)",
    "Heat Input (mmBtu)",
    "CO2 Mass (short tons)",
    "SO2 Mass (short tons)",
    "NOx Mass (short tons)",
    "Primary Fuel Type",
    "Unit Type",
]
