from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def create_app():
    app = Flask(__name__)

    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///epaData.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    # Maximum upload size: 50 MB
    app.config["MAX_CONTENT_LENGTH"] = 50 * 1024 * 1024

    db.init_app(app)

    # Register application routes
    from routes.main import main_bp
    from routes.upload import upload_bp
    from routes.approval import approval_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(upload_bp)
    app.register_blueprint(approval_bp)

    # Load database models
    import models
    import importdata

    with app.app_context():
        db.create_all()

    return app