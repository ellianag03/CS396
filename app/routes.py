# NOT NEEEDED ANYMORE SINCE main.py and upload.py

from flask import Blueprint, render_template, request

main = Blueprint("main", __name__)


@main.route("/")
def home():
    return render_template("index.html")


@main.route("/upload", methods=["GET", "POST"])
def upload():
    if request.method == "POST":

        uploaded_file = request.files.get("data_file")

        if uploaded_file is None:
            return "No file selected."

        if uploaded_file.filename == "":
            return "No file selected."

        return f"File received: {uploaded_file.filename}"

    return render_template("upload.html")
