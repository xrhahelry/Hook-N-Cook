from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, current_user, login_required
from flask_wtf import FlaskForm
from flask_bcrypt import Bcrypt

from .models import User
from . import db

auth = Blueprint("auth", __name__)
bcrypt = Bcrypt()

@auth.route("/signup", methods=['GET', 'POST'])
def signup():
    if request.method == 'GET':
        return render_template('signup.html')
    elif request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')

        hashed_password = bcrypt.generate_password_hash(password)

        user = User(username=username, email=email, password=hashed_password)

        db.session.add(user)
        db.session.commit()

        login_user(user, remember=True)
        return redirect(url_for('views.home'))

    return render_template('signup.html')

@auth.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    elif request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(username=username).first()  

        if bcrypt.check_password_hash(user.password, password):
            login_user(user, remember=True)
            return redirect(url_for('views.home'))
        else:
            flash('Invalid email or password', 'error')
            return render_template('login.html')  

    return render_template('login.html')

@auth.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('views.home'))

def register_routes(app, db):
    app.register_blueprint(auth)
