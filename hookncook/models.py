from flask_login import UserMixin
from . import db

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    tracked_products = db.Column(db.String(100), nullable=True)

    
    def to_json(self):
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email,
            "tracked_products": self.tracked_products,
        }

