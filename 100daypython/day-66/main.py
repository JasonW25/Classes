from crypt import methods
from flask import Flask, jsonify, render_template, request
from flask_sqlalchemy import SQLAlchemy
from itsdangerous import json
from sqlalchemy.sql import func

app = Flask(__name__)

def str2bool(v):
    return v.lower() in ("yes", "true", "t", "1")

##Connect to Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cafes.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


##Cafe TABLE Configuration
class Cafe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), unique=True, nullable=False)
    map_url = db.Column(db.String(500), nullable=False)
    img_url = db.Column(db.String(500), nullable=False)
    location = db.Column(db.String(250), nullable=False)
    seats = db.Column(db.String(250), nullable=False)
    has_toilet = db.Column(db.Boolean, nullable=False)
    has_wifi = db.Column(db.Boolean, nullable=False)
    has_sockets = db.Column(db.Boolean, nullable=False)
    can_take_calls = db.Column(db.Boolean, nullable=False)
    coffee_price = db.Column(db.String(250), nullable=True)

    def to_dict(self):
        return {column.name: getattr(self, column.name) for column in self.__table__.columns}


@app.route("/")
def home():
    return render_template("index.html")
    

## HTTP GET - Read Record
@app.route("/random")
def get_random():
    random_cafe = Cafe.query.order_by(func.random()).first()
    return jsonify(cafe=random_cafe.to_dict())

@app.route("/all")
def get_all():
    all_cafes =db.session.query(Cafe).all()
    return jsonify(cafe=[cafe.to_dict() for cafe in all_cafes])

@app.route("/search")
def search():
    place = request.args.get("loc")
    cafe_search = Cafe.query.filter_by(location=place)
    return jsonify(cafe=[cafe.to_dict() for cafe in cafe_search])

## HTTP POST - Create Record
@app.route("/add", methods=["GET","POST"])
def add():
    try:
        new_cafe = Cafe(
        name=request.form.get("name"),
        map_url=request.form.get("map_url"),
        img_url=request.form.get("img_url"),
        location=request.form.get("loc"),
        has_sockets=str2bool(request.form.get("sockets")),
        has_toilet=str2bool(request.form.get("toilet")),
        has_wifi=str2bool(request.form.get("wifi")),
        can_take_calls=str2bool(request.form.get("calls")),
        seats=request.form.get("seats"),
        coffee_price=request.form.get("coffee_price"),
        )
        db.session.add(new_cafe)
        db.session.commit()
    except:
        return jsonify(response={"Error": "There was a problem with your cafe parameters"})
    return jsonify(response={"Success": "Successfully added new cafe"})


## HTTP PUT/PATCH - Update Record

@app.route("/update-price/<cafe_id>", methods=["GET", "PATCH"])
def update_price(cafe_id):
    cafe_to_update = Cafe.query.get(cafe_id)
    new_price = request.args.get("new_price")
    if cafe_to_update:
        cafe_to_update.coffee_price = new_price
        db.session.commit()
        return jsonify(response={"Success": "Successfully added new cafe"}), 200
    else:
        return jsonify(error={"Not Found": "Sorry a cafe with that id was not found in the database."}), 404

## HTTP DELETE - Delete Record
@app.route("/report-closed/<cafe_id>", methods=["DELETE"])
def delete(cafe_id):
    API_KEY = "12345"
    user_key = request.args.get("api-key")
    if user_key == API_KEY:
        cafe_to_delete = Cafe.query.get(cafe_id)
        if cafe_to_delete:
            db.session.delete(cafe_to_delete)
            db.session.commit()
            return jsonify(response={"Success": "Successfully deleted cafe"}), 200
        else:
            return jsonify(error={"Not Found": "Sorry a cafe with that id was not found in the database."}), 404
    else:
        return jsonify(error={"Bad api-key": "You api-key does not match keys in our records"}), 403


if __name__ == '__main__':
    app.run(debug=True)
