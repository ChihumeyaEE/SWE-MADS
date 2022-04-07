from enum import unique
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class User(db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120), nullable=False, unique=True)


# this table is for user posts of items
class Post(db.Model):
    __tablename__ = "post"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120), db.ForeignKey("user.username"))
    location = db.Column(db.String(120), nullable=False)
    name = db.Column(db.String(120), nullable=False)
    qty = db.Column(db.Integer)
    description = db.Column(db.String(240), nullable=False)
