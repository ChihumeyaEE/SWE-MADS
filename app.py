import os
import requests
import flask,json
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

db.init_app(app)

# creates all the classes(tables) in the models.py

# db.session.remove()
# db.drop_all()

with app.app_context():
    db.create_all()

shown_location = ""

# when user clickss save, this route updates the DB and redirect to index
@app.route("/checkoutCart", methods=["POST","GET"])
@login_required
def checkout():
    if flask.request.method == "POST":
        data = flask.request.get_json()
        for i in data["cart"]:
            splitted = i.split("_")
            id = splitted[1]
            item = splitted[0]
            # print("inside for loop: ", id, item)
            object = Post.query.filter_by(user_id=id, item_name=item).first()
            if object.quantity > 0:
                print("BEFORE: ", object.quantity)
                object.quantity -= 1
                print("AFTER: ", object.quantity)
                db.session.commit()
            else:
                print("object quantity is 0: ", object.quantity)
    print("This should redirect")
    return flask.redirect(flask.url_for("index"))


login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"


@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))


@app.route("/")
@login_required
def index():
    global shown_location
    current_location_data = get_location_data()
    current_location = current_location_data["city"]
    if shown_location == "":
        shown_location = current_location 
    users_posts = Post.query.all()
    # print(users_posts[1].item_name)
    return flask.render_template(
        "index.html", postLen=len(users_posts), posts=users_posts, shown_location = shown_location, current_location = current_location
    )

@app.route("/login", methods=["POST", "GET"])
def login():
    # form = flask.request.form
    if flask.request.method == "POST":
        data = flask.request.form
        password = data["password"]
        user = User.query.filter_by(username=data["username"]).first()
        if user is not None and check_password_hash(user.password, password):
            login_user(user)
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
    global shown_location
    shown_location = ""
    return flask.redirect(flask.url_for("login"))

@app.route("/search", methods = ['POST'])
def search():
    global shown_location 
    shown_location = flask.request.form.get('location')
    return flask.redirect(flask.url_for('index'))

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
    current_location_data = get_location_data()
    current_location = current_location_data["city"]
    global shown_location
    shown_location = ""
    return flask.render_template("profilepage.html", current_location = current_location)


@app.route("/handleforms", methods=["POST", "GET"])
def handleforms():
    if flask.request.method == "POST":
        data = flask.request.form
        new_post = Post(
            user_id=current_user.id,
            username=current_user.username,
            location=data["Location"],
            item_name=data["Item_Name"],
            quantity=data["Quantity"],
            description=data["Description"],
        )
        db.session.add(new_post)
        db.session.commit()

    return flask.redirect(flask.url_for("index"))


app.run(
    host=os.getenv("IP", "0.0.0.0"),
    port=int(os.getenv("PORT", 8080)),
    debug=True,
)
