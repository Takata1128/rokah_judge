from flask_blog import db
from flask_login import UserMixin


class User(UserMixin, db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(100))

    def __init__(self, email, password, name):
        self.email = email
        self.password = password
        self.name = name
