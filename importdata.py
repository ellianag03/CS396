from datetime import datetime

from app import db


class ImportBatch(db.Model):
    __tablename__ = "import_batch"

    id = db.Column(db.Integer, primary_key=True)

    filename = db.Column(
        db.String(255),
        nullable=False
    )

    uploaded_at = db.Column(
        db.DateTime,
        nullable=False,
        default=datetime.utcnow
    )

    status = db.Column(
        db.String(50),
        nullable=False,
        default="VALIDATED"
    )

    row_count = db.Column(db.Integer)
    valid_row_count = db.Column(db.Integer)
    rejected_row_count = db.Column(db.Integer)

    approved_at = db.Column(db.DateTime, nullable=True)

    imported_at = db.Column(db.DateTime, nullable=True)
