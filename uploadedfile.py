class UploadedFile(db.Model):
    __tablename__ = "uploaded_files"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    dataset_id = db.Column(
        db.Integer,
        db.ForeignKey("datasets.id"),
        nullable=False
    )

    filename = db.Column(
        db.String(255),
        nullable=False
    )

    file_type = db.Column(
        db.String(20)
    )

    file_size = db.Column(
        db.Integer
    )

    upload_date = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    validation_status = db.Column(
        db.String(50)
    )

    rejected_record_count = db.Column(
        db.Integer,
        default=0
    )
