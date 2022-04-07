import os
import flask
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv, find_dotenv
from models import db, User, Post

load_dotenv(find_dotenv())

app = flask.Flask(__name__)
# Point SQLAlchemy to your Heroku database
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
# Gets rid of a warning
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
# IMPORTANT: This must be AFTER creating db variable to prevent
# circular import issues

db.init_app(app)

# creates all the classes(tables) in the models.py
# db.drop_all()
with app.app_context():
    db.create_all()

# when user clickss save, this route updates the DB and redirect to index
@app.route("/checkoutCart", methods=["GET", "POST"])
def checkout():
    if flask.request.method == "POST":
        pass


@app.route("/")
def index():
    return flask.render_template("index.html", postLen=4)


app.run(
    host=os.getenv("IP", "0.0.0.0"),
    port=int(os.getenv("PORT", 8080)),
    debug=True,
)
