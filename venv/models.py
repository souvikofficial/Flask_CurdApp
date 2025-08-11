from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

class Book(db.model):
    id = db.column(db.integer,primary_key=True)
    title = db.column(db.String(120), nullable=False)
    author  = db.column(db.String(50),nullable=False)

    def __repr__ (self):
        return f'<Book {self.title}>'

