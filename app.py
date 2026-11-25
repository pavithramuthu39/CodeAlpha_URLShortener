
from flask import Flask, request, redirect, render_template, jsonify
from flask_sqlalchemy import SQLAlchemy
import string
import random
import os
from urllib.parse import urlparse

app = Flask(__name__)

database_url = os.environ.get("DATABASE_URL", "sqlite:///urls.db")
if database_url.startswith("postgres://"):
    database_url = database_url.replace("postgres://", "postgresql+psycopg://", 1)
elif database_url.startswith("postgresql://"):
    database_url = database_url.replace("postgresql://", "postgresql+psycopg://", 1)

app.config["SQLALCHEMY_DATABASE_URI"] = database_url
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)


class URL(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    original_url = db.Column(db.String(2048), nullable=False)
    short_code = db.Column(db.String(10), unique=True, nullable=False)


def generate_short_code():
    characters = string.ascii_letters + string.digits

    while True:
        code = ''.join(random.choices(characters, k=6))

        if not URL.query.filter_by(short_code=code).first():
            return code


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/shorten", methods=["POST"])
def shorten_url():
    original_url = request.form.get("original_url", "").strip()
    parsed_url = urlparse(original_url)

    if parsed_url.scheme not in ("http", "https") or not parsed_url.netloc:
        return jsonify({"error": "Enter a valid URL starting with http:// or https://"}), 400

    code = generate_short_code()

    new_url = URL(original_url=original_url, short_code=code)
    db.session.add(new_url)
    db.session.commit()

    short_url = request.host_url + code

    return jsonify({"short_url": short_url})


@app.route("/<short_code>")
def redirect_url(short_code):
    url_entry = URL.query.filter_by(short_code=short_code).first()

    if url_entry:
        return redirect(url_entry.original_url)

    return "Short URL not found!", 404


with app.app_context():
    db.create_all()


if __name__ == "__main__":
    app.run(debug=True)
