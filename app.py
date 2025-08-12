# app.py
import os
from flask import Flask, render_template, request, redirect, url_for, flash
from sqlalchemy.exc import SQLAlchemyError

from models import db, Book          # ← import the shared objects

app = Flask(__name__, instance_relative_config=True)

app.config.update(
    SECRET_KEY="replace-with-a-32-char-random-string",
    SQLALCHEMY_TRACK_MODIFICATIONS=False,
    SQLALCHEMY_DATABASE_URI="sqlite:///" + os.path.join(app.instance_path, "books.db"),
)

# ensure the instance folder exists (that’s where books.db will live)
os.makedirs(app.instance_path, exist_ok=True)

db.init_app(app)                     # bind the models to this Flask app

# create all tables once, at startup
with app.app_context():
    db.create_all()

# ------------------------------------------------------------------
# Routes
# ------------------------------------------------------------------
@app.route("/")
def index():
    books = Book.query.all()
    return render_template("index.html", books=books)


@app.route("/create", methods=["GET", "POST"])
def create():
    if request.method == "POST":
        try:
            new_book = Book(
                title=request.form["title"],
                author=request.form["author"],
            )
            db.session.add(new_book)
            db.session.commit()
            flash("Book added successfully")
            return redirect(url_for("index"))
        except SQLAlchemyError as e:
            db.session.rollback()
            flash(f"Error: {e}")
    return render_template("create.html")


@app.route("/edit/<int:id>", methods=["GET", "POST"])
def edit(id):
    book = Book.query.get_or_404(id)
    if request.method == "POST":
        try:
            book.title  = request.form["title"]
            book.author = request.form["author"]
            db.session.commit()
            flash("Book updated")
            return redirect(url_for("index"))
        except SQLAlchemyError as e:
            db.session.rollback()
            flash(f"Error: {e}")
    return render_template("edit.html", book=book)


@app.route("/delete/<int:id>", methods=["POST"])
def delete(id):
    book = Book.query.get_or_404(id)
    try:
        db.session.delete(book)
        db.session.commit()
        flash("Book deleted")
    except SQLAlchemyError as e:
        db.session.rollback()
        flash(f"Error: {e}")
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(debug=True)
