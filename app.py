import os
import requests
import flask
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv, find_dotenv
from models import db, User, Post
from flask_login import (
    LoginManager,
    logout_user,
    current_user,
    login_user,
    login_required,
)
from werkzeug.security import generate_password_hash, check_password_hash

load_dotenv(find_dotenv())

app = flask.Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY")
# Point SQLAlchemy to your Heroku database
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABAS_URL")
# Gets rid of a warning
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
# IMPORTANT: This must be AFTER creating db variable to prevent
# circular import issues

# db.init_app(app)

# creates all the classes(tables) in the models.py

shown_location = ""

with app.app_context():
    db.create_all()

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"


@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))


@app.route("/")
@login_required
def index():
    return flask.render_template("index.html")

@app.route("/login", methods=["POST", "GET"])
def login():
    # form = flask.request.form
    if flask.request.method == "POST":
        data = flask.request.form
        password = data["password"]
        user = User.query.filter_by(username=data["username"]).first()
        if user is not None and check_password_hash(user.password, password):
            login_user(user)
            current_location_data = get_location_data()
            current_location = current_location_data["city"]
            global shown_location
            shown_location = current_location 
            return flask.redirect(flask.url_for("index"))
        else:
            flask.flash("Username/Password does not exist!")

    return flask.render_template("login.html")


@app.route("/signup", methods=["POST", "GET"])
def signup():
    if flask.request.method == "POST":
        data = flask.request.form
        new_user = User(
            username=data["username"],
            password=generate_password_hash(data["password"], method="sha256"),
        )
        checkusername = User.query.filter_by(username=data["username"]).first()
        checkspace = data["username"].strip()
        if checkspace != "":
            db.session.add(new_user)
            db.session.commit()
            return flask.redirect(flask.url_for("login"))
        else:
            flask.flash("Username not found")

    return flask.render_template("signup.html")


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return flask.redirect(flask.url_for("login"))


@app.route("/homepage")
def homepage():
    listings = [{"name": "hammer", "quantity": 1, "location": "Atlanta", "description": "This is a hammer that is made of steel"}, {"name": "Wrench", "quantity": 3, "location": "Chicago", "description": "This is a wrench"}, {"name": "Screwdriver", "quantity": 3, "location": "Lawrenceville", "description": "This is a wrench"}]
    return flask.render_template("homepage.html", listings = listings, shown_location = shown_location)

@app.route("/search", methods = ['POST'])
def search():
    global shown_location 
    shown_location = flask.request.form.get('location')
    return flask.redirect(flask.url_for('homepage'))

def get_location_data():
    base_url = "http://ip-api.com/json/"
    response = requests.get(base_url)
    location_data = response.json()
    region = location_data["region"]
    city = location_data["city"]

    return {
        "city": city,
        "region": region
    }


@app.route("/profilepage")
def profilepage():
    return flask.render_template("profilepage.html")


@app.route("/handleforms", methods=["POST", "GET"])
def handleforms():
    if flask.request.method == "POST":
        data = flask.request.form
        new_post = Post(
            user_id=current_user.id,
            username=current_user.username,
            item_name=data["Item_Name"],
            quantity=data["Quantity"],
            description=data["Description"],
        )
        db.session.add(new_post)
        db.session.commit()

    return flask.redirect(flask.url_for("homepage"))


app.run(
    host=os.getenv("IP", "0.0.0.0"),
    port=int(os.getenv("PORT", 8080)),
    debug=True,
)
