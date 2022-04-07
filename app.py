import os
import requests
from flask import Flask, jsonify, redirect, render_template, request, url_for
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv, find_dotenv
# from models import db, User, Cart

load_dotenv(find_dotenv())

app = Flask(__name__)
# Point SQLAlchemy to your Heroku database
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
# Gets rid of a warning
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
# IMPORTANT: This must be AFTER creating db variable to prevent
# circular import issues

# db.init_app(app)

# creates all the classes(tables) in the models.py
# with app.app_context():
#     db.create_all()

shown_location = ""

# login:
# current_location_data = get_location_data()
# current_location = current_location_data["city"]
# global shown_location
# shown_location = current_location 

@app.route("/homepage")
def homepage():
    listings = [{"name": "hammer", "quantity": 1, "location": "Atlanta", "description": "This is a hammer that is made of steel"}, {"name": "Wrench", "quantity": 3, "location": "Chicago", "description": "This is a wrench"}, {"name": "Screwdriver", "quantity": 3, "location": "Lawrenceville", "description": "This is a wrench"}]
    return render_template("homepage.html", listings = listings, shown_location = shown_location, ip_addr = request.remote_addr)

@app.route("/search", methods = ['POST'])
def search():
    global shown_location 
    shown_location = request.form.get('location')
    return redirect(url_for('homepage'))

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

app.run(
    host=os.getenv("IP", "0.0.0.0"),
    port=int(os.getenv("PORT", 8080)),
    debug=True,
)
