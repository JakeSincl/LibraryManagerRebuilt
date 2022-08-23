from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func

class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150))
    author = db.Column(db.String(150))
    description = db.Column(db.String(1000))
    publish_year = db.Column(db.Integer)
    currently_loaned = db.Column(db.Boolean())
    loaned_to = db.Column(db.Integer, db.ForeignKey("user.id"))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))
    access_level = db.Column(db.Integer)
    books = db.relationship("Book", backref="user")