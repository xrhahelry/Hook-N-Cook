from flask_login import UserMixin
from . import db
import json

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    tracked_products = db.Column(db.String, nullable=True, default="[]")

    def to_json(self):
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email,
            "tracked_products": json.loads(self.tracked_products),
        }
    
    def add_tracked_product(self, product_id):
        products = json.loads(self.tracked_products)
        if product_id not in products:
            products.append(product_id)
            self.tracked_products = json.dumps(products)
            db.session.commit()
    
    def remove_tracked_product(self, product_id):
        products = json.loads(self.tracked_products)
        if product_id in products:
            products.remove(product_id)
            self.tracked_products = json.dumps(products)
            db.session.commit()
