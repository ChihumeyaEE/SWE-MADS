# pylint: disable=invalid-name,no-member,unused-import,unused-variable,missing-module-docstring,missing-function-docstring,wrong-import-order,redefined-builtin,multiple-imports,invalid-envvar-default,missing-class-docstring
from enum import unique
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

db = SQLAlchemy()


class User(db.Model, UserMixin):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120), nullable=False)
    password = db.Column(db.String(100))


class Post(db.Model):
    __tablename__ = "post"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    username = db.Column(db.String(120))
    location = db.Column(db.String(120), nullable=False)
    item_name = db.Column(db.String(120), nullable=False)
    quantity = db.Column(db.Integer)
    description = db.Column(db.String(240), nullable=False)


class Transactions(db.Model):
    __tablename__ = "transactions"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)  # current user
    post_id = db.Column(db.Integer)
    item_name = db.Column(db.String(120), nullable=False)
    quantity = db.Column(db.Integer)
