"""import the necessary modules"""
import os
from flask import Flask, render_template, redirect, request, session, url_for, flash
from wtforms import Form, TextField, validators

app = Flask(__name__)
app.config.from_object("config")

class RegistrationForm(Form):
    """class method for registration form"""
    firstName = TextField("First Name:", validators=[validators.required()])
    secondName = TextField("Second Name:", validators=[validators.required()])
    email = TextField("e-mail:", validators=[validators.required(), validators.Length(min=6, max=35)])
    password = TextField('Generate Password:', validators=[validators.required(), validators.Length(min=3, max=35)])

@app.route("/", methods=["GET", "POST"])
def index():
    """define the index function"""
    return render_template("index.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    """define loggin function"""
    if request.form["password"] == "password" and request.form["username"] == "admin":
        session["logged_in"] = True
    else:
        flash("wrong password!")
    return render_template("login.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    """define register function"""
    form = RegistrationForm(request.form)
    print form.errors
    if request.method == "POST":
        firstName = request.form["firstName"]
        secondName = request.form["secondName"]
        email = request.form["email"]
        password = request.form["password"]
        print firstName, " ", email, " ", password, " "

        if form.validate():
            flash("Thanks for registration ", + firstName + secondName)
        else:
            flash("Error: All the fileds arerequired. ")
    return render_template("register.html", form=form)

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
