"""import the necessary modules"""
import os
import hashlib
from flask import Flask, render_template, redirect, request, session, url_for, flash
from wtforms import Form, TextField, validators, PasswordField

app = Flask(__name__)
app.config.from_object("config")


class RegistrationForm(Form):
    """registration class defined"""
    username = TextField('Username:', validators=[validators.required()])
    email = TextField('Email:', validators=[validators.required(),
                                            validators.Length(min=6, max=35)])
    password = TextField('Password:', validators=[validators.required(),
                                                  validators.Length(min=3, max=35)])


@app.route("/", methods=["GET", "POST"])
def index():
    """define the index function"""
    return render_template("index.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    """define login function"""
    if request.method == "POST": #checks if method used is "POST"
        if "username" in session and "password" in session: #checks if user's username and passwords are in session
            password = request.form['password']
            hashed_password = hashlib.sha256(password.encode()).hexdigest()
            # session["password"] = hashed_password
            if session["username"] == request.form["username"] and session["password"] == hashed_password:#checks if the credentials match the ones used in registration form
                # session["password"] = hashed_password
                return redirect(url_for("shopping_list"))
            else:
                return render_template("login.html")
        else:
            return render_template("login.html")
    else:
        return render_template("login.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    """define register function"""
    # form = RegistrationForm(request.form)
    if request.method != "POST":
        return render_template("register.html")

    username = request.form['username']
    password = request.form['password']
    # email = request.form["email"]

    session["username"] = username

    hashed_password = hashlib.sha256(password.encode()).hexdigest()
    session["password"] = hashed_password

    # session["email"] = email

    return redirect(url_for("login"))


@app.route("/shopping_list", methods=["GET", "POST"])
def shopping_list():
    """define shopping list function"""
    return render_template("shopping_list.html")


@app.route("/logout",)
def loggout():
    """define loggout function"""
    session["logged_in"] = False
    return redirect(url_for("login.html"))


if __name__ == "__main__":
    app.secret_key = os.urandom(12)
    app.run(debug=True)
