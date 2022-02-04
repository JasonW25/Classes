from wsgiref.handlers import format_date_time
from flask import Flask, render_template, redirect, url_for, request
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from sqlalchemy import all_
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, URL
from flask_ckeditor import CKEditor, CKEditorField
import datetime as dt


## Delete this code:
# import requests
# posts = requests.get("https://api.npoint.io/43644ec4f0013682fc0d").json()

app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
ckeditor = CKEditor(app)
Bootstrap(app)

##CONNECT TO DB
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///posts.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

##CONFIGURE TABLE
class BlogPost(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(250), unique=True, nullable=False)
    subtitle = db.Column(db.String(250), nullable=False)
    date = db.Column(db.String(250), nullable=False)
    body = db.Column(db.Text, nullable=False)
    author = db.Column(db.String(250), nullable=False)
    img_url = db.Column(db.String(250), nullable=False)


##WTForm
class CreatePostForm(FlaskForm):
    title = StringField("Blog Post Title", validators=[DataRequired()])
    subtitle = StringField("Subtitle", validators=[DataRequired()])
    author = StringField("Your Name", validators=[DataRequired()])
    img_url = StringField("Blog Image URL", validators=[DataRequired(), URL()])
    body = CKEditorField("Blog Content", validators=[DataRequired()])
    submit = SubmitField("Submit Post")


@app.route('/')
def get_all_posts():
    posts = db.session.query(BlogPost).all()
    return render_template("index.html", all_posts=posts)


@app.route("/post/<int:index>")
def show_post(index):
    posts = db.session.query(BlogPost).all()
    for blog_post in posts:
        if blog_post.id == index:
            requested_post = blog_post
    return render_template("post.html", post=requested_post)

@app.route("/edit/<int:index>")
def edit_post(index):
    return redirect("url_for('get_all_posts')")


@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/new-post", methods=["GET", "POST"])
def new_post():
    form = CreatePostForm()
    edit_arg = request.args.get("edit")
    edit_id = request.args.get("id")
    if edit_arg == "yes":
        title="Edit Post"
        post = BlogPost.query.get(edit_id)
        form = CreatePostForm(
        title=post.title,
        subtitle=post.subtitle,
        img_url=post.img_url,
        author=post.author,
        body=post.body
        )
        if request.method == 'POST':
            post.title = request.form.get('title')
            post.subtitle = request.form.get('subtitle')
            post.body = request.form.get('body')
            post.author = request.form.get('author')
            post.img_url = request.form.get('img_url')
            db.session.commit()
            return redirect( url_for('get_all_posts'))
        return render_template("make-post.html", form=form, title=title)
    else:
        title = "New Post"
        if request.method == 'POST':
            now = dt.datetime.now()
            new_post= BlogPost(
                title = request.form.get('title'),
                date = now.strftime("%B %d, %Y"),
                subtitle = request.form.get('subtitle'),
                body = request.form.get('body'),
                author = request.form.get('author'),
                img_url = request.form.get('img_url'),
                )
            db.session.add(new_post)
            db.session.commit()
            return redirect( url_for('get_all_posts'))
    return render_template("make-post.html", form=form, title=title)

@app.route("/delete")
def delete():
    id = request.args.get("id")
    post = BlogPost.query.get(id)
    db.session.delete(post)
    db.session.commit()
    return redirect(url_for('get_all_posts'))

@app.route("/contact")
def contact():
    return render_template("contact.html")

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)


#   <a class="btn btn-primary float-right" href="{{url_for('edit_post', id=post.id)}}">Edit Post</a>
