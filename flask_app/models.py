from flask_login import UserMixin
from datetime import datetime
from . import db, login_manager


@login_manager.user_loader
def load_user(user_id):
    return User.objects(username=user_id).first()

class User(db.Document, UserMixin):
    username = db.StringField(unique=True, required=True, max_length=40, min_length=1)
    email = db.EmailField(unique=True, required=True)
    password = db.StringField(required=True)
    profile_pic = db.ImageField()

    # Returns unique string identifying our object
    def get_id(self):
        return self.username


class Review(db.Document):
    commenter = db.ReferenceField(User, required=True)
    content = db.StringField(required=True, max_length=500, min_length=5)
    date = db.StringField(required=True)
    imdb_id = db.StringField(required=True, max_length=9, min_length=9)
    movie_title = db.StringField(required=True, max_length=100, min_length=1)
    image = db.StringField()