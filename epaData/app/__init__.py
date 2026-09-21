from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os

db = SQLAlchemy()


def create_app():
    app = Flask(__name__)

    # Store the SQLite database in the project's instance folder
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///epaData.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)

    from app.routes import main
    app.register_blueprint(main)

    from app import models

    with app.app_context():
        db.create_all()

    return app
