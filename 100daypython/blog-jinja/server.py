from flask import Flask, render_template
import datetime as dt
import requests


now = dt.datetime.now()
year_now = now.year

app = Flask(__name__)

@app.route('/')
def home():
    return render_template("index.html", year=year_now)

@app.route("/guess/<name_input>")
def guess(name_input):
    name_title = name_input.title()
    gender = requests.get(f'https://api.genderize.io?name={name_input}').json()["gender"]
    years = requests.get(f'https://api.agify.io?name={name_input}').json()['age']
    return render_template("guess.html", name=name_title, gend=gender, age=years)

@app.route('/blog')
def blog():
    blog_url = 'https://api.npoint.io/c790b4d5cab58020d391'
    blogs = requests.get(blog_url).json()
    return render_template("blog.html", posts=blogs)

if __name__ == "__main__":
    app.run(debug=True)

