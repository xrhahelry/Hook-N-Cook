from flask_login import UserMixin
from . import db

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    tracked_product = db.Column(db.String(32), nullable=True)

    
    def to_json(self):
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email,
        }

class Laptop(db.Model):
    id = db.Column(db.String, primary_key=True)
    price = db.Column(db.Integer, unique=False, nullable=False)
    brand = db.Column(db.String, unique=False, nullable=False)
    model = db.Column(db.String, unique=False, nullable=False)
    processor = db.Column(db.Integer, unique=False, nullable=False)
    ram_memory = db.Column(db.Integer, unique=False, nullable=False)
    display_size = db.Column(db.Float, unique=False, nullable=False)
    storage_capacity = db.Column(db.Integer, unique=False, nullable=False)
    cpu_cores = db.Column(db.Integer, unique=False, nullable=False)
    graphics_card = db.Column(db.Float, unique=False, nullable=False)
    rating = db.Column(db.Float, unique=False, nullable=False)
    reviews = db.Column(db.Integer, unique=False, nullable=False)
    name = db.Column(db.String, unique=False, nullable=False)
    url = db.Column(db.String, unique=True, nullable=False)

    def to_json(self):
        return {
            "id": self.id,
            "price": self.price,
            "brand": self.brand,
            "model": self.model,
            "processor": self.processor,
            "ramMemory": self.ram_memory,
            "displaySize": self.display_size,
            "storageCapacity": self.storage_capacity,
            "cpuCores": self.cpu_cores,
            "graphicsCard": self.graphics_card,
            "rating": self.rating,
            "reviews": self.reviews,
            "name": self.name,
            "url": self.url,
        }
