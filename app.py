from flask import Flask ,render_template , request , redirect , url_for ,flash 
from flask import session as flask_session

from models import db , Book
from sqlalchemy.exc import SQLAlchemyError

import os


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///book.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config["SECRET_KEY"] = "replace-with-a-32-char-random-string"

try:
    os.makedirs(app.instance_path)
except OSError:
    pass

db.init_app(app)


@app.route("/")
def index():
    books = Book.query.all()
    return render_template("index.html",books=books)

@app.route("/create", methods=['GET','POST'])
def create():
    if request.method == "POST":
        try :
            new_book = Book(
                title = request.form['title'],
                author = request.form['author']
            )

            db.session.add(new_book)
            db.session.commit()
            flash('Book added Successfully')
            return redirect(url_for("index"))
        except SQLAlchemyError as e:
            db.session.rollback()
            flash(f'Error: {e}')
    return render_template('create.html')

@app.route('/edit/<int:id>',methods=['GET','POST'])
def edit(id):
    book = Book.query.get_or_404(id)
    if request.method == 'POST':
        try: 
            book.title = request.form['title']
            book.author = request.form['author']
            db.session.commit()
            flash('Book Updated')
            return redirect(url_for('index'))
        except SQLAlchemyError as e:
            db.session.rollback()
            flash(f'Error {e}')
    return render_template('edit.html',book= book)


@app.route('/delete/<int:id>',methods=['POST'])
def delete(id):
    book = Book.query.get_or_404(id)
    if request.method == "POST":
        try  :
            db.session.delete(book)
            db.session.commit()
            flash('Book deleted')
        except SQLAlchemyError as e:
            db.session.rollback()
            flash(f'Error {e}')
    return redirect(url_for('index'))

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)