from app import db
from datetime import datetime


class Dataset(db.Model):
    __tablename__ = "datasets"

    id = db.Column(db.Integer, primary_key=True)

    import_batch_id = db.Column(
        db.Integer,
        db.ForeignKey("import_batch.id"),
        nullable=True
        )
    
    name = db.Column(
        db.String(200),
        nullable=False
    )

    source = db.Column(
        db.String(100),
        nullable=False
    )

    reporting_year = db.Column(
        db.Integer
    )

    retrieval_date = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    original_filename = db.Column(
        db.String(255)
    )

    raw_record_count = db.Column(
        db.Integer,
        default=0
    )

    accepted_record_count = db.Column(
        db.Integer,
        default=0
    )

    notes = db.Column(
        db.Text
    )
    #Facility Class
class Facility(db.Model):
    __tablename__ = "facilities"

    id = db.Column(db.Integer, primary_key=True)

    dataset_id = db.Column(
        db.Integer,
        db.ForeignKey("datasets.id"),
        nullable=False
    )

    epa_facility_id = db.Column(
        db.String(50),
        nullable=False
    )

    facility_name = db.Column(
        db.String(255)
    )

    state = db.Column(
        db.String(2)
    )

    county = db.Column(
        db.String(100)
    )

    latitude = db.Column(
        db.Float
    )

    longitude = db.Column(
        db.Float
    )

    source_category = db.Column(
        db.String(100)
    )

    __table_args__ = (
        db.UniqueConstraint(  # detects duplicate dataset and facility combinations
            "dataset_id",
            "epa_facility_id",
            name="unique_dataset_facility"
        ),
    )
# Unit Class
class Unit(db.Model):
    __tablename__ = "units"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    facility_id = db.Column(
        db.Integer,
        db.ForeignKey("facilities.id"),
        nullable=False
    )

    epa_unit_id = db.Column(
        db.String(50),
        nullable=False
    )

    unit_type = db.Column(
        db.String(100)
    )

    primary_fuel = db.Column(
        db.String(100)
    )

    secondary_fuel = db.Column(
        db.String(100)
    )

    operating_date = db.Column(
        db.Date
    )

    retirement_date = db.Column(
        db.Date
    )

    __table_args__ = (
        db.UniqueConstraint(  # detects duplicate facility and unit combinations
            "facility_id",
            "epa_unit_id",
            name="unique_facility_unit"
        ),
    )
#Annual Record Class
class AnnualRecord(db.Model):
    __tablename__ = "annual_records"

    id = db.Column(db.Integer, primary_key=True)

    unit_id = db.Column(
        db.Integer,
        db.ForeignKey("units.id"),
        nullable=False
    )

    reporting_year = db.Column(db.Integer, nullable=False)

    operating_time = db.Column(db.Float)
    gross_load_mwh = db.Column(db.Float)
    steam_load = db.Column(db.Float)
    heat_input_mmbtu = db.Column(db.Float)

    co2_short_ton = db.Column(db.Float)
    so2_short_ton = db.Column(db.Float)
    nox_short_ton = db.Column(db.Float)

    so2_control = db.Column(db.String(255))
    nox_control = db.Column(db.String(255))
    pm_control = db.Column(db.String(255))
    program_code = db.Column(db.String(100))

    __table_args__ = (
        db.UniqueConstraint( #detects duplicate facility, unit, and year combinations
            "unit_id",
            "reporting_year",
            name="unique_unit_year"
        ),
    )