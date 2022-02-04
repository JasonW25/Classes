from crypt import methods
from flask import Flask, render_template
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import DataRequired, URL
import csv

app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
Bootstrap(app)


class CafeForm(FlaskForm):
    cafe = StringField('Cafe name', validators=[DataRequired()])
    location = StringField('Cafe Location on Google Maps (URL)', validators=[URL(), DataRequired()])
    open_time = StringField('Open Time e.g. 8AM', validators=[DataRequired()]) 
    close_time = StringField('Close Time e.g. 5:30PM', validators=[DataRequired()])
    coffee = SelectField('Coffee Rating', choices=["☕☕☕☕☕", "☕☕☕☕",  "☕☕☕", "☕☕", "☕"], validators=[DataRequired()])
    wifi = SelectField('Wifi Strength Rating', choices=["💪💪💪💪💪", "💪💪💪💪", "💪💪💪", "💪💪", "💪", "✘"], validators=[DataRequired()])
    power = SelectField('Power Socket Availability', choices=["🔌🔌🔌🔌🔌", "🔌🔌🔌🔌", "🔌🔌🔌", "🔌🔌", "🔌", "✘"], validators=[DataRequired()])
    submit = SubmitField('Submit', validators=[DataRequired()])

# Exercise:
# add: Location URL, open time, closing time, coffee rating, wifi rating, power outlet rating fields
# make coffee/wifi/power a select element with choice of 0 to 5.
#e.g. You could use emojis ☕️/💪/✘/🔌
# make all fields required except submit
# use a validator to check that the URL field has a URL entered.
# ---------------------------------------------------------------------------


# all Flask routes below
@app.route("/")
def home():
    return render_template("index.html")


@app.route('/add', methods=["GET", "POST"])
def add_cafe():
    form = CafeForm()
    if form.validate_on_submit():
        print("True")
        with open("cafe-data.csv", "a") as file:
            data = f"\n{form.cafe.data},{form.location.data},{form.open_time.data},{form.close_time.data},{form.coffee.data},{form.wifi.data},{form.power.data}"
            file.write(data)
    return render_template('add.html', form=form)


@app.route('/cafes')
def cafes():
    with open('cafe-data.csv', newline='') as csv_file:
        csv_data = csv.reader(csv_file, delimiter=',')
        list_of_rows = []
        for row in csv_data:
            list_of_rows.append(row)
    return render_template('cafes.html', cafes=list_of_rows)


if __name__ == '__main__':
    app.run(debug=True)
