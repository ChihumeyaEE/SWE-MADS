# pylint: disable=invalid-name,no-member,unused-import,unused-variable,missing-module-docstring,missing-function-docstring,wrong-import-order,redefined-builtin,multiple-imports,invalid-envvar-default,global-statement,consider-using-enumerate
from crypt import methods
import os
import requests
import flask, json
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv, find_dotenv
from models import db, User, Post, Transactions
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

shown_location = "Atlanta"

# when user clickss save, this route updates the DB and redirect to index
@app.route("/checkoutCart", methods=["POST", "GET"])
@login_required
def checkout():
    if flask.request.method == "POST":
        data = flask.request.get_json()
        for i in range(len(data["posts_id"])):
            postid = data["posts_id"][i]
            item = data["cart"][i]
            object = Post.query.filter_by(id=postid, item_name=item).first()

            if object.quantity > 0:
                object.quantity -= 1
                db.session.commit()
                savesTransactions(postid, item)

    return flask.jsonify("OK")


def savesTransactions(postid, item):
    # have a check to where there is nothing of a particular name in the database

    checkquantity = Transactions.query.filter_by(
        user_id=current_user.id, post_id=postid, item_name=item
    ).first()
    if checkquantity is None:
        print("Here1")
        new_transaction = Transactions(
            user_id=current_user.id,
            post_id=postid,
            item_name=item,
            quantity=1,
        )
        db.session.add(new_transaction)
        db.session.commit()
    else:
        if checkquantity.quantity > 0:
            checkquantity.quantity += 1
            print("Here2")
            db.session.commit()
            # updates the quantity of a particular id
        else:
            new_transaction = Transactions(
                user_id=current_user.id,
                post_id=postid,
                item_name=item,
                quantity=1,
            )
            print("Here3")
            db.session.add(new_transaction)
            db.session.commit()


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
    # current_location_data = get_location_data()
    # current_location = current_location_data["city"]
    # if shown_location == "":
    #     shown_location = current_location
    users_posts = Post.query.all()
    return flask.render_template(
        "index.html",
        postLen=len(users_posts),
        posts=users_posts,
        shown_location=shown_location,
    )


@app.route("/login", methods=["POST", "GET"])
def login():
    if flask.request.method == "POST":
        data = flask.request.form
        password = data["password"]
        user = User.query.filter_by(username=data["username"]).first()
        if user is not None and check_password_hash(user.password, password):
            login_user(user)
            # global shown_location
            # shown_location = ""
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
    # global shown_location
    # shown_location = ""
    return flask.redirect(flask.url_for("login"))


@app.route("/search", methods=["POST"])
def search():
    global shown_location
    shown_location = flask.request.form.get("location").capitalize()
    return flask.redirect(flask.url_for("index"))


def get_location_data():
    base_url = "http://ip-api.com/json/"
    response = requests.get(base_url)
    location_data = response.json()
    region = location_data["region"]
    city = location_data["city"]

    return {
        "city": city,
        "region": region,
    }


@app.route("/profilepage")
def profilepage():
    current_location_data = get_location_data()
    current_location = current_location_data["city"]

    getUsersTransactions = Transactions.query.filter_by(user_id=current_user.id).all()
    print("current user's transactions:", getUsersTransactions)

    postersNameList = []
    itemNameList = []
    quantityList = []
    locationList = []
    transactionsidList = []
    postidList = []

    for i in range(len(getUsersTransactions)):
        getPosts = Post.query.filter_by(id=getUsersTransactions[i].post_id).first()
        postersNameList.append(getPosts.username)
        itemNameList.append(getUsersTransactions[i].item_name)
        quantityList.append(getUsersTransactions[i].quantity)
        locationList.append(getPosts.location)

        transactionsidList.append(getUsersTransactions[i].id)
        postidList.append(getPosts.id)

    # User's Items
    # query all posts for this specific user id
    user_items = Post.query.filter_by(user_id=current_user.id).all()

    return flask.render_template(
        "profilepage.html",
        current_location=current_location,
        postersNameList=postersNameList,
        itemNameList=itemNameList,
        quantityList=quantityList,
        locationList=locationList,
        transactionsidList=transactionsidList,
        postidList=postidList,
        user_items=user_items,
    )


@app.route("/editQuantity", methods=["POST", "GET"])
def editQty():
    data = flask.request.form
    qty = data["qty"]
    id = data["post"]
    post_query = Post.query.filter_by(id=id).first()
    if Transactions.query.filter_by(post_id=id).first() is None:
        post_query.quantity = qty
        db.session.commit()
    else:
        flask.flash(
            "Cannot edit quantity "
            + post_query.item_name
            + " ,because its currently being rented"
        )
    return flask.redirect("/profilepage")


# Handles items getting deleted
@app.route("/deleteItems", methods=["POST", "GET"])
def deleteItems():
    data = flask.request.form
    postId = data["post"]
    post_query = Post.query.filter_by(id=postId).first()

    if Transactions.query.filter_by(post_id=postId).first() is None:
        db.session.delete(post_query)
        db.session.commit()
    else:
        flask.flash(
            "Cannot delete "
            + post_query.item_name
            + " ,because its currently being rented"
        )
    return flask.redirect("/profilepage")


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


@app.route("/returnitem", methods=["POST"])
def returnitem():
    returnedquantity = int(flask.request.form.get("returnedquantity"))

    returnedtransactionid = flask.request.form.get("transactionID")
    returnedpostid = flask.request.form.get("postID")

    transactions = Transactions.query.filter_by(id=returnedtransactionid).first()
    posts = Post.query.filter_by(id=returnedpostid).first()

    transactions.quantity = transactions.quantity - returnedquantity

    posts.quantity = posts.quantity + returnedquantity

    # removes item from transactions table
    if transactions.quantity == 0:
        db.session.delete(transactions)
    db.session.commit()

    return flask.redirect(flask.url_for("profilepage"))

@app.route("/aboutus")
def aboutus():

    return flask.render_template(
        "aboutus.html",
    )

app.run(
    host=os.getenv("IP", "0.0.0.0"),
    port=int(os.getenv("PORT", 8080)),
    debug=True,
)
