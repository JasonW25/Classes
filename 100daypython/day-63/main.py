from crypt import methods
from flask import Flask, render_template, request, redirect, url_for
from flask import Flask, render_template
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///new-books-collection.db'
db = SQLAlchemy(app)
Bootstrap(app)

class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), unique=True, nullable=False)
    author = db.Column(db.String(120), unique=False, nullable=False)
    rating =  db.Column(db.Float, unique=False, nullable=False)

    def __repr__(self):
        return f'<Book {self.title}>'

db.create_all()

# class BookForm(FlaskForm):
#     book = StringField('Book Name', validators=[DataRequired()])
#     author = StringField('Book Author', validators=[DataRequired()])
#     rating = StringField('Rating', validators=[DataRequired()])
#     submit = SubmitField('Add Book', validators=[DataRequired()])

all_books = []

@app.route('/')
def home():
    all_books =db.session.query(Book).all()
    return render_template('index.html', list=all_books)


@app.route("/add", methods=["POST", "GET"])
def add():
    if request.method == "POST":
        new_book = Book(
            title=request.form["book"],
            author=request.form["author"],
            rating=request.form["rating"]
        )

        db.session.add(new_book)
        db.session.commit()
        return redirect(url_for('home'))
    return render_template('add.html')

@app.route("/edit/<id>", methods=["GET", "POST"])
def edit(id):
    book_id = id
    book_to_update = Book.query.get(book_id)
  
    if request.method == "POST":
        book_to_update.rating = request.form["new_rating"]
        db.session.commit()
        return redirect(url_for('home'))  
    return render_template('edit.html', book=book_to_update, num=id)

@app.route("/delete/<id>")
def delete(id):
    book_id = id
    book_to_delete = Book.query.get(book_id)
    db.session.delete(book_to_delete)
    db.session.commit()
    return redirect(url_for('home'))



if __name__ == "__main__":
    app.run(debug=True)

