from app import db
from models import Dataset, Facility, Unit, AnnualRecord

def import_dataframe(df, filename, source="User Upload"):
    """
    Import a validated DataFrame into the database.
    """

    reporting_year = int(
        df["REPORTING_YEAR"].iloc[0]
    )

    dataset = Dataset(
        name=filename,
        source=source,
        reporting_year=reporting_year,
        original_filename=filename,
        raw_record_count=len(df),
        accepted_record_count=0
    )

    db.session.add(dataset)
    db.session.flush()

    facilities = {}
    units = {}

    accepted_count = 0

    for _, row in df.iterrows():

        facility_key = row["EPA_FACILITY_ID"]

        # -------------------------
        # Facility
        # -------------------------

        if facility_key not in facilities:

            facility = Facility(
                dataset_id=dataset.id,
                epa_facility_id=str(
                    row["EPA_FACILITY_ID"]
                ),
                facility_name=row["FACILITY_NAME"],
                state=row["STATE"],
                county=row["COUNTY"],
                latitude=row.get("LATITUDE"),
                longitude=row.get("LONGITUDE"),
                source_category=row.get(
                    "SOURCE_CATEGORY"
                )
            )

            db.session.add(facility)
            db.session.flush()

            facilities[facility_key] = facility

        else:

            facility = facilities[facility_key]

        # -------------------------
        # Unit
        # -------------------------

        unit_key = (
            facility.id,
            str(row["UNIT_ID"])
        )

        if unit_key not in units:

            unit = Unit(
                facility_id=facility.id,
                epa_unit_id=str(
                    row["UNIT_ID"]
                ),
                unit_type=row.get("UNIT_TYPE"),
                primary_fuel=row.get("PRIMARY_FUEL"),
                secondary_fuel=row.get(
                    "SECONDARY_FUEL"
                )
            )

            db.session.add(unit)
            db.session.flush()

            units[unit_key] = unit

        else:

            unit = units[unit_key]

        # -------------------------
        # Annual Record
        # -------------------------

        record = AnnualRecord(
            unit_id=unit.id,
            reporting_year=int(
                row["REPORTING_YEAR"]
            ),

            operating_time=row[
                "OPERATING_TIME"
            ],

            gross_load_mwh=row[
                "GROSS_LOAD_MWH"
            ],

            steam_load=row.get(
                "STEAM_LOAD"
            ),

            heat_input_mmbtu=row[
                "HEAT_INPUT_MMBTU"
            ],

            co2_short_ton=row[
                "CO2_SHORT_TON"
            ],

            so2_short_ton=row[
                "SO2_SHORT_TON"
            ],

            nox_short_ton=row[
                "NOX_SHORT_TON"
            ],

            so2_control=row.get(
                "SO2_CONTROL"
            ),

            nox_control=row.get(
                "NOX_CONTROL"
            ),

            pm_control=row.get(
                "PM_CONTROL"
            ),

            program_code=row.get(
                "PROGRAM_CODE"
            )
        )

        db.session.add(record)

        accepted_count += 1

    dataset.accepted_record_count = accepted_count

    db.session.commit()

    return dataset