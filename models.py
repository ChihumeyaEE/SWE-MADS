from enum import unique
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class User(db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120), nullable=False)


# product class is used to add individual items by user, the cart should be implemented in another file on the page
# because the the cart is always inter-changeable
class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(90), unique=True)
    img = db.Column(db.String(150))
    price = db.Column(db.Float, nullable=False)
