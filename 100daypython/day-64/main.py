from flask import Flask, render_template, redirect, url_for, request
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from numpy import False_
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
import requests
import json
import urllib.parse

app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///movies.db'
db = SQLAlchemy(app)
Bootstrap(app)

api_key = "
headers = {
    'Authorization': f'Bearer {api_key}',
    'Content-Type': 'application/json;charset=utf-8'
}

class MyForm(FlaskForm):
    movie_title = StringField(label="Movie Title", validators=[ DataRequired()])
    submit = SubmitField(label="Add Movie", validators=[DataRequired()])

class Movie(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), unique=True, nullable=False)
    year = db.Column(db.Integer, nullable=False)
    description = db.Column(db.String(500), nullable=False)
    rating = db.Column(db.Float, nullable=True)
    ranking = db.Column(db.Integer, unique=False_, nullable=True)
    review = db.Column(db.String(500), nullable=True)
    img_url = db.Column(db.String(500), nullable=False)

db.create_all()

@app.route("/")
def home():
    all_movies = Movie.query.order_by(Movie.rating).all()
    
    #This line loops through all the movies
    for i in range(len(all_movies)):
        #This line gives each movie a new ranking reversed from their order in all_movies
        all_movies[i].ranking = len(all_movies) - i
    db.session.commit()

    return render_template("index.html", list=all_movies)

# new_movie = Movie(
#     title="Phone Booth",
#     year=2002,
#     description="Publicist Stuart Shepard finds himself trapped in a phone booth, pinned down by an extortionist's sniper rifle. Unable to leave or receive outside help, Stuart's negotiation with the caller leads to a jaw-dropping climax.",
#     rating=7.3,
#     ranking=10,
#     review="My favourite character was the caller.",
#     img_url="https://image.tmdb.org/t/p/w500/tjrX2oWRCM3Tvarz38zlZM7Uc10.jpg"
# )
# db.session.add(new_movie)
# db.session.commit()


@app.route("/edit", methods=["GET", "POST"] )
def edit():
    movie_id = request.args.get('id')
    movie = Movie.query.get(movie_id)
    if request.method == "POST":
        movie.rating = request.form["rating"]
        movie.review = request.form["review"]
        db.session.commit()
        return redirect(url_for('home'))
    return render_template('edit.html', movie=movie)

@app.route("/find")
def find_movie():
    movie_api_id = request.args.get("id")
    if movie_api_id:
        response = requests.get(url=f"https://api.themoviedb.org/3/movie/{movie_api_id}", headers=headers)
        data = response.json()
        new_movie = Movie(
            title=data['title'],
            year=data["release_date"].split("-")[0],
            description= data["overview"],
            img_url= f'https://image.tmdb.org/t/p/original{data["poster_path"]}'
            )
        db.session.add(new_movie)
        db.session.commit()
        movie = Movie.query.filter_by(title=data['title']).first()
        id = movie.id
        print(id)
        return redirect(url_for('edit', id=id))

@app.route("/delete")
def delete():
    movie_id = request.args.get('id')
    movie_to_delete = Movie.query.get(movie_id)
    db.session.delete(movie_to_delete)
    db.session.commit()
    return redirect(url_for('home'))


@app.route("/add", methods=["POST", "GET"])
def add():
    form = MyForm()
    if form.validate_on_submit():
        params = {
            "query": form.movie_title.data
        }
        response = requests.get(url=api_url, headers=headers, params=params)
        sheet_data = response.json()['results']
        with open("doc_save.json", "w") as file:
            json.dump(sheet_data, file, indent=4)
        return redirect(url_for('select'))
    return render_template("add.html", form=form)

@app.route("/select")
def select():
    with open("doc_save.json", "r") as file:
        data = json.load(file)
    
    return render_template("select.html", data=data)

if __name__ == '__main__':
    app.run(debug=True)
