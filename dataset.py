dataset = Dataset(
    name="CAMPD 2025 Upload",
    source="CAMPD",
    reporting_year=2025,
    original_filename=file.filename,
    raw_record_count=len(df),
    accepted_record_count=0
)

db.session.add(dataset)
db.session.flush()

dataset.id
