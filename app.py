
from flask import Flask, request, redirect, render_template, jsonify
from flask_sqlalchemy import SQLAlchemy
import string
import random

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///urls.db"
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

    if not original_url.startswith(("http://", "https://")):
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
