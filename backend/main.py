from config import app, db
from flask import jsonify, request
from models import Laptop, User


@app.route("/users", methods=["GET"])
def get_users():
    users = User.query.all()
    json_users = list(map(lambda x: x.to_json(), users))
    return jsonify({"users": json_users})


@app.route("/create_user", methods=["POST"])
def create_user():
    first_name = request.json.get("firstName")
    last_name = request.json.get("lastName")
    email = request.json.get("email")

    if not first_name or not last_name or not email:
        return jsonify({"message": "Some values misssing"}), 400

    new_user = User(first_name=first_name, last_name=last_name, email=email)
    try:
        db.session.add(new_user)
        db.session.commit()
    except Exception as e:
        return jsonify({"message": str(e)}), 400

    return jsonify({"message": "User created!"}), 201


@app.route("/laptops", methods=["GET"])
def get_laptops():
    laptops = Laptop.query.all()
    json_laptops = list(map(lambda x: x.to_json(), laptops))
    return jsonify({"laptops": json_laptops})


@app.route("/create_laptop", methods=["POST"])
def create_laptop():
    data = request.json

    id = data.get("id")
    price = data.get("price")
    brand = data.get("brand")
    model = data.get("model")
    processor = data.get("processor")
    ram_memory = data.get("ramMemory")
    display_size = data.get("displaySize")
    storage_capacity = data.get("storageCapacity")
    cpu_cores = data.get("cpuCores")
    graphics_card = data.get("graphicsCard")
    rating = data.get("rating")
    reviews = data.get("reviews")
    name = data.get("name")
    url = data.get("url")

    if not (
        id
        and price
        and brand
        and model
        and processor
        and ram_memory
        and display_size
        and storage_capacity
        and cpu_cores
        and graphics_card
        and rating
        and reviews
        and name
        and url
    ):
        return jsonify({"message": "Some values missing"}), 400

    new_laptop = Laptop(
        id=id,
        price=price,
        brand=brand,
        model=model,
        processor=processor,
        ram_memory=ram_memory,
        display_size=display_size,
        storage_capacity=storage_capacity,
        cpu_cores=cpu_cores,
        graphics_card=graphics_card,
        rating=rating,
        reviews=reviews,
        name=name,
        url=url,
    )
    try:
        db.session.add(new_laptop)
        db.session.commit()
    except Exception as e:
        return jsonify({"message": str(e)}), 400

    return jsonify({"message": "Laptop created!"}), 201


if __name__ == "__main__":
    with app.app_context():
        db.create_all()

    app.run(debug=True)
