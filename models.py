# models.py
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()          # the single SQLAlchemy instance


class Book(db.Model):
    __tablename__ = "book"

    id     = db.Column(db.Integer, primary_key=True)
    title  = db.Column(db.String(120), nullable=False)
    author = db.Column(db.String(120), nullable=False)

    def __repr__(self):
        return f"<Book {self.title}>"
