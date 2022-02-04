from flask import Flask, render_template,redirect
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, Length
from flask_bootstrap import Bootstrap

app = Flask(__name__)
Bootstrap(app)
app.secret_key = ""

class MyForm(FlaskForm):
    email = StringField(label="email", validators=[Email(), DataRequired()])
    password = PasswordField(label='password', validators=[Length(min=8),DataRequired()])
    submit = SubmitField(label="Log In", validators=[DataRequired()])


@app.route("/")
def home():
    return render_template('index.html')

@app.route("/login", methods=["GET","POST"])
def login():
    form = MyForm()
    if form.validate_on_submit():
        email = form.email.data
        passw = form.password.data
        if email == "admin@email.com" and passw == "12345678":
            return redirect('/success')
        else:
            return redirect('denied')
    return render_template('login.html', form=form)

@app.route("/success")
def success():
    return render_template('success.html')

@app.route("/denied")
def denied():
    return render_template('denied.html')

if __name__ == '__main__':
    app.run(debug=True)
