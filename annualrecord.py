record = AnnualRecord(
    unit_id=unit.id,
    reporting_year=row["REPORTING_YEAR"],

    operating_time=row["OPERATING_TIME"],
    gross_load_mwh=row["GROSS_LOAD_MWH"],
    steam_load=row.get("STEAM_LOAD"),
    heat_input_mmbtu=row["HEAT_INPUT_MMBTU"],

    co2_short_ton=row["CO2_SHORT_TON"],
    so2_short_ton=row["SO2_SHORT_TON"],
    nox_short_ton=row["NOX_SHORT_TON"],

    so2_control=row.get("SO2_CONTROL"),
    nox_control=row.get("NOX_CONTROL"),
    pm_control=row.get("PM_CONTROL"),
    program_code=row.get("PROGRAM_CODE")
)

db.session.add(record)
