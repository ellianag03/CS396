from app import db

class UploadMetadata(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    import_batch_id = db.Column(
        db.Integer,
        db.ForeignKey("import_batch.id"),
        nullable=False
    )

    original_filename = db.Column(db.String(255))
    file_type = db.Column(db.String(50))
    file_size = db.Column(db.Integer)

    uploaded_at = db.Column(db.DateTime)
    uploaded_by = db.Column(db.String(255))

    source_system = db.Column(db.String(255))
    source_description = db.Column(db.Text)
