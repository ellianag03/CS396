from app import db
from datetime import datetime

class DataProvenance(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    import_batch_id = db.Column(
        db.Integer,
        db.ForeignKey("import_batch.id"),
        nullable=False
    )

    target_table = db.Column(db.String(255))
    source_file = db.Column(db.String(255))

    source_row = db.Column(db.Integer)

    imported_at = db.Column(db.DateTime)

    transformation_notes = db.Column(db.Text)
