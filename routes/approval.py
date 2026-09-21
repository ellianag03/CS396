import os 
import pandas as pd 

from flask import Blueprint, render_template, redirect, url_for
from app import db
from importdata import ImportBatch
#from import_data import import_dataframe


approval_bp = Blueprint("approval", __name__)

@approval_bp.route("/approval/<int:import_id>", methods=["GET"])
def approval(import_id):

    import_batch = ImportBatch.query.get_or_404(import_id)

    return render_template(
        "approval.html",
        import_batch=import_batch
    )

@approval_bp.route(
    "/approval/<int:import_id>/approve",
    methods=["POST"]
)
def approve(import_id):

    import_batch = ImportBatch.query.get_or_404(import_id)

    # Make sure this import hasn't already been processed
    if import_batch.status != "VALIDATED":
        return redirect(
            url_for(
                "approval.approval",
                import_id=import_batch.id
            )
        )

    # ---------------------------------------------------------
    # Locate uploaded file
    # ---------------------------------------------------------

    file_path = os.path.join(
        "uploads",
        import_batch.filename
    )

    # ---------------------------------------------------------
    # Read uploaded file
    # ---------------------------------------------------------

    extension = os.path.splitext(
        import_batch.filename
    )[1].lower()

    try:

        if extension == ".csv":
            df = pd.read_csv(file_path)

        else:
            df = pd.read_excel(file_path)

    except Exception as e:

        import_batch.status = "IMPORT_FAILED"

        db.session.commit()

        return render_template(
            "approval.html",
            import_batch=import_batch,
            error=f"Could not read file for import: {str(e)}"
        )

    # ---------------------------------------------------------
    # Import data
    # ---------------------------------------------------------

    try:

        dataset = import_dataframe(
            df,
            import_batch
        )

    except Exception as e:

        db.session.rollback()

        import_batch.status = "IMPORT_FAILED"

        db.session.commit()

        return render_template(
            "approval.html",
            import_batch=import_batch,
            error=f"Database insertion failed: {str(e)}"
        )

    # ---------------------------------------------------------
    # Show completed approval/import page
    # ---------------------------------------------------------

    return redirect(
        url_for(
            "approval.approval",
            import_id=import_batch.id
        )
    )

@approval_bp.route(
    "/approval/<int:import_id>/reject",
    methods=["POST"]
)
def reject(import_id):

    import_batch = ImportBatch.query.get_or_404(import_id)

    import_batch.status = "REJECTED"

    db.session.commit()

    return redirect(
        url_for(
            "upload.upload"
        )
    )

