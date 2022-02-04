from flask import Flask, render_template, request, url_for, redirect, flash, send_from_directory
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, login_user, LoginManager, login_required, current_user, logout_user
import time

app = Flask(__name__)
login_manager = LoginManager()

app.config['SECRET_KEY'] = 'any-secret-key-you-choose'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
login_manager.init_app(app)
db = SQLAlchemy(app)

##CREATE TABLE IN DB
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(1000))
#Line below only required once, when creating DB. 
# db.create_all()

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

@app.route('/')
def home():
    return render_template("index.html", logged_in=current_user.is_authenticated)


@app.route('/register', methods=["GET", "POST"])
def register():
    if request.method == "POST":
        email1 =request.form["email"]
        user = User.query.filter_by(email=email1)
        if user:
            flash('Email already has account tied to it. Please use another email')
        else:
            hash = generate_password_hash(request.form["password"], method='pbkdf2:sha256', salt_length=8)
            new_user = User(
                name=request.form["name"],
                email=email1,
                password=hash
            )

            db.session.add(new_user)
            db.session.commit()
            user = User.query.filter_by(email=email1).first()
            login_user(user)
            return redirect(url_for('secrets', id=user.id, logged_in=current_user.is_authenticated))
    return render_template("register.html")


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == "POST":
        # Login and validate the user.
        # user should be an instance of your `User` class
        user = User.query.filter_by(email=request.form['email']).first()
        print(type(user))
        if user:
            if check_password_hash(user.password, request.form['password']):
                login_user(user)

                flash('Logged in successfully.')
                return redirect(url_for('secrets', id=user.id))
            else:
                flash('Password incorrect')
        else:
            flash('Email not in system')
    return render_template("login.html")


@app.route('/secrets')
@login_required
def secrets():
    id = request.args.get("id")
    user = User.query.get(id)
    return render_template("secrets.html", user=user, logged_in=current_user.is_authenticated)


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))


@app.route('/download')
def download():
    return send_from_directory('static', 'files/cheat_sheet.pdf', as_attachment=True)


if __name__ == "__main__":
    app.run(debug=True)
