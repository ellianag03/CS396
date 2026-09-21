import os

import pandas as pd
from flask import Blueprint, render_template, request

from app import db 
from importdata import ImportBatch
from services.validator import validate_dataframe
from pathlib import Path

upload_bp = Blueprint("upload", __name__)

ALLOWED_EXTENSIONS = {".csv", ".xlsx", ".xls"}
MAX_FILE_SIZE = 50 * 1024 * 1024  # 50 MB


def allowed_file(filename):
    """Check whether the uploaded file has a supported extension."""
    if not filename:
        return False

    extension = os.path.splitext(filename)[1].lower()

    return extension in ALLOWED_EXTENSIONS


@upload_bp.route("/upload", methods=["GET", "POST"])
def upload():

    if request.method == "GET":
        return render_template("upload.html")

    # ---------------------------------------------------------
    # 1. Make sure a file was submitted
    # ---------------------------------------------------------

    uploaded_file = request.files.get("data_file")

    if uploaded_file is None:
        return render_template(
            "upload.html",
            error="No file was selected."
        )

    if uploaded_file.filename == "":
        return render_template(
            "upload.html",
            error="No file was selected."
        )

    # ---------------------------------------------------------
    # 2. Check file extension
    # ---------------------------------------------------------

    if not allowed_file(uploaded_file.filename):
        return render_template(
            "upload.html",
            error="Invalid file type. Please upload a CSV or Excel file."
        )

    # ---------------------------------------------------------
    # 3. Check file size
    # ---------------------------------------------------------

    uploaded_file.seek(0, os.SEEK_END)
    file_size = uploaded_file.tell()
    uploaded_file.seek(0)

    if file_size > MAX_FILE_SIZE:
        return render_template(
            "upload.html",
            error="File is too large. Maximum size is 50 MB."
        )

    # ---------------------------------------------------------
    # 4. Read the file with pandas
    # ---------------------------------------------------------

    try:
        extension = os.path.splitext(
            uploaded_file.filename
        )[1].lower()

        if extension == ".csv":
            df = pd.read_csv(uploaded_file)
        else:
            df = pd.read_excel(uploaded_file)

    except Exception as e:
        return render_template(
            "upload.html",
            error=f"Could not read the file: {str(e)}"
        )

    # ---------------------------------------------------------
    # 5. Validate the dataframe
    # ---------------------------------------------------------

    validation = validate_dataframe(df)

    # Count rejected rows
    rejected_row_count = len(
    validation.get("invalid_year_rows", [])
    )

    # Calculate accepted rows
    valid_row_count = len(df) - rejected_row_count

    # ---------------------------------------------------------
    # 6. Create an ImportBatch
    # ---------------------------------------------------------

    import_batch = ImportBatch(
     filename=uploaded_file.filename,
     row_count=len(df),
     valid_row_count=valid_row_count,
     rejected_row_count=rejected_row_count,
        status="VALIDATED"
    )

    db.session.add(import_batch)
    db.session.commit()

    # ---------------------------------------------------------
    # 7. Show validation report
    # ---------------------------------------------------------

    return render_template(
     "validation.html",
     filename=uploaded_file.filename,
     validation=validation,
     import_batch=import_batch
    )