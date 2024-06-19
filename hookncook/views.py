import json

import pandas as pd
import plotly.express as px
from flask import Blueprint, redirect, render_template, request, url_for
from flask_login import current_user, login_required

from model import one_hot, one_n

from . import db
from .models import User

views = Blueprint("views", __name__)


@views.route("/", methods=["GET", "POST"])
def home():
    columns = {
        "processor": {
            "ancient processor": 2,
            "i3 or Ryzen 3": 3,
            "i5 or Ryzen 5": 5,
            "M1": 6.5,
            "i7 or Ryzen 7": 7,
            "M2": 7.5,
            "M3": 8.5,
            "i9 or Ryzen 9": 9,
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
        "graphics": {
            "No Graphics Card": 0,
            "Integrated Graphics Card": 1000,
            "GTX 1050": 1050,
            "MX 330": 1300,
            "MX 350": 1300,
            "MX 450": 1400,
            "MX 550": 1500,
            "GTX 1650 Ti": 1650,
            "GTX 1660": 1660,
            "Radeon 2000": 2000,
            "RTX 2040": 2040,
            "Iris Xe": 2050,
            "RTX 2060": 2060,
            "RTX 2070": 2070,
            "M1 Integrated Card": 2500,
            "M2 Integrated Card": 2800,
            "M3 Integrated Card": 2900,
            "RTX 3050": 3050,
            "RTX 3060": 3060,
            "RTX 3070": 3070,
            "RTX 4050": 4050,
            "RTX 4060": 4060,
            "RTX 4070": 4070,
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
        "graphics card": None,
    }
    cols = [
        "processor",
        "ram memory",
        "display size",
        "storage capacity",
        "cpu cores",
        "graphics card",
    ]
    searched_items = []
    price_input = ""
    levels = {
        "Exact Match": 0,
        "High Similarity": 1,
        "Moderate Similarity(recommended)": 3,
        "Low Similarity": 4,
        "No Match": 8,
    }
    models = {"One Hot": 0, "One N": 1}
    numbers = {"No limit": -1, "5": 5, "10": 10, "20": 20}
    sorts = {
        "Price": "price",
        "Similarity": "distance",
        "Graphics Card": "graphics card",
        "Processor": "processor",
        "No. of Cores": "cpu cores",
        "Ram": "ram memory",
        "Display Size": "display size",
        "Storage capacity": "storage capacity",
    }
    if request.method == "POST":
        price_input = request.form.get("price_input", "")
        selected_items["price"] = int(price_input)
        for c, i in enumerate(columns):
            selected_item = request.form.get(f"dropdown_{i}")
            if selected_item:
                selected_items[cols[c]] = selected_item
        limit = request.form.get("dropdown_level", "3")
        method = request.form.get("dropdown_model", "")
        sort = request.form.get("dropdown_sort", "")
        num = request.form.get("dropdown_num", "")
        if int(method) == 0:
            searched_items = one_hot.one_hot(
                selected_items, int(limit), str(sort), int(num)
            )
        else:
            searched_items = one_n.one_n(
                selected_items, int(limit), str(sort), int(num)
            )
    return render_template(
        "home.html",
        columns=columns,
        searched_items=searched_items,
        levels=levels,
        models=models,
        numbers=numbers,
        sorts=sorts,
    )


@views.route("/product/<product_id>")
def product(product_id):
    laptop = pd.read_csv("data/laptop.csv")
    data = laptop.set_index("id")
    product = data.loc[product_id, :].to_dict()
    product["id"] = product_id
    history = pd.read_csv(f"data/prices/{product_id}.csv")
    history["Date"] = pd.to_datetime(history["Date"])
    figure = px.line(history, x="Date", y="Discount Price", title="Price vs Date")
    figure.update_yaxes(title_text="Price")
    history_html = figure.to_html(full_html=False)

    return render_template("product.html", product=product, history=history_html)


@views.route("/track_product/<product_id>", methods=["POST"])
@login_required
def track_product(product_id):
    current_user.add_tracked_product(product_id)
    return redirect(url_for("views.product", product_id=product_id))


@views.route("/untrack_product/<product_id>", methods=["POST"])
@login_required
def untrack_product(product_id):
    current_user.remove_tracked_product(product_id)
    return redirect(url_for("views.product", product_id=product_id))


@views.route("/tracked_products")
@login_required
def tracked_products():
    tracked_product_ids = json.loads(current_user.tracked_products)
    laptop_data = pd.read_csv("data/laptop.csv")
    tracked_products = laptop_data[laptop_data["id"].isin(tracked_product_ids)].to_dict(
        orient="records"
    )
    return render_template("tracked_products.html", tracked_products=tracked_products)
