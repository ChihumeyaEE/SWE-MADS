from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

db = SQLAlchemy()


class User(db.Model,UserMixin):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120), nullable=False)
    password = db.Column(db.String(100))

#class Cart(db.Model):
   # __tablename__ = "cart"
   # pass

   

class Post(db.Model):
    __tablename__ = "post"
    id = db.Column(db.Integer, primary_key=True)
    # location = db.Column(db.String(120), nullable=False)
    item_name = db.Column(db.String(120), nullable=False)
    quantity = db.Column(db.Integer)
    description = db.Column(db.String(240), nullable=False)


