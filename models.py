from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

class ConfigModel(db.Model):
    __tablename__ = "config"

    id = db.Column(db.Integer, primary_key=True)
    orientacao = db.Column(db.Text())
    width = db.Column(db.Text())
    height = db.Column(db.Text())
    
    def set_orientacao(self, orientacao):
        self.orientacao = orientacao

    def set_width(self, width):
        self.width = width

    def set_height(self, height):
        self.height = height


class StreamModel(db.Model):
    __tablename__ = "stream"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text(), unique=True)
    video_src = db.Column(db.Text(), unique=True)

    def set_name(self, set_name):
        self.name = set_name

    def set_video_src(self, video_src):
        self.video_src = video_src


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

