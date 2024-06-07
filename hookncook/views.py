from flask import Blueprint, render_template, request

from model import one_hot

views = Blueprint("views", __name__)


@views.route("/", methods=["GET", "POST"])
def home():
    columns = {
        "processor": {
            "ancient processor": 2,
            "i3 or Ryzen 3": 3,
            "i5 or Ryzen 5": 5,
            "i7 or Ryzen 7": 7,
            "i9 or Ryzen 9": 9,
            "M1": 6.5,
            "M2": 7.5,
            "M3": 8.5,
        },
        "Ram": {
            "4 GB": 4,
            "6 GB": 6,
            "8 GB": 8,
            "12 GB": 12,
            "16 GB": 16,
            "24 GB": 24,
            "32 GB": 32,
        },
        "Display": {
            "10.5 inches": 10.5,
            "11.6 inches": 11.6,
            "12.0 inches": 12.0,
            "13.3 inches": 13.3,
            "13.5 inches": 13.5,
            "13.6 inches": 13.6,
            "14.0 inches": 14.0,
            "14.1 inches": 14.1,
            "14.5 inches": 14.5,
            "15.0 inches": 15.0,
            "15.6 inches": 15.6,
            "16.0 inches": 16.0,
            "16.1 inches": 16.1,
            "16.2 inches": 16.2,
            "17.0 inches": 17.0,
            "17.3 inches": 17.3,
        },
        "storage capacity": {
            "64 GB": 64,
            "128 GB": 128,
            "256 GB": 256,
            "512 GB": 512,
            "1024 GB": 1024,
            "2048 GB": 2048,
        },
        "cpu cores": {
            "1": 1,
            "2": 2,
            "4": 4,
            "5": 5,
            "6": 6,
            "8": 8,
            "10": 10,
            "12": 12,
            "14": 14,
            "16": 16,
            "20": 20,
            "24": 24,
        },
    }
    selected_items = {
        "id": "00000",
        "brand": "ABC",
        "model": "DEF",
        "price": None,
        "processor": None,
        "ram memory": None,
        "display size": None,
        "storage capacity": None,
        "cpu cores": None,
    }
    cols = ["processor", "ram memory", "display size", "storage capacity", "cpu cores"]
    searched_items = []
    price_input = ""
    levels = {
        "Exact Match": 0,
        "High Similarity": 1,
        "Moderate Similarity(recommended)": 3,
        "Low Similarity": 4,
        "No Match": 8,
    }

    if request.method == "POST":
        price_input = request.form.get("price_input", "")
        selected_items["price"] = int(price_input)
        for c, i in enumerate(columns):
            selected_item = request.form.get(f"dropdown_{i}")
            if selected_item:
                selected_items[cols[c]] = selected_item
        limit = request.form.get("dropdown_level", "3")
        searched_items = one_hot.one_hot(selected_items, int(limit))
    return render_template(
        "home.html", columns=columns, searched_items=searched_items, levels=levels
    )
