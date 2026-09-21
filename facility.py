facility = Facility(
    dataset_id=dataset.id,
    epa_facility_id=row["EPA_FACILITY_ID"],
    facility_name=row["FACILITY_NAME"],
    state=row["STATE"],
    county=row["COUNTY"],
    latitude=row.get("LATITUDE"),
    longitude=row.get("LONGITUDE"),
    source_category=row.get("SOURCE_CATEGORY")
)
db.session.add(facility)
db.session.flush()
