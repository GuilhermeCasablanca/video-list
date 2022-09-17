from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

class UserModel(UserMixin, db.Model):
    __tablename__ = "user"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.Text(), unique=True)
    email = db.Column(db.Text(), unique=True)
    password = db.Column(db.Text())
    isadmin = db.Column(db.Integer)

    def set_username (self, username):
        self.username = username

    def set_email(self, email):
        self.email = email

    def set_isadmin(self, isadmin):
        self.isadmin = isadmin
   
    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)


class VideoModel(db.Model):
    __tablename__ = "videos"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text())
    stream = db.Column(db.Text())
    source = db.Column(db.Text())
    isactive = db.Column(db.Integer)

    def __init__(self, name, stream, source):
        self.name = name
        self.stream = stream
        self.source = source
        self.isactive = 0
