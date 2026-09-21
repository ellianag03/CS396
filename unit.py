unit = Unit(
    facility_id=facility.id,
    epa_unit_id=row["UNIT_ID"],
    unit_type=row.get("UNIT_TYPE"),
    primary_fuel=row.get("PRIMARY_FUEL"),
    secondary_fuel=row.get("SECONDARY_FUEL")
)

db.session.add(unit)
db.session.flush()

unit.id
