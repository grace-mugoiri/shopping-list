"""import the necessary modules"""
from flask import Flask, render_template, redirect, request, session, url_for
app = Flask(__name__)
app.config.from_object("config")

"""define your function for the first route"""
@app.route("/", methods=["GET", "POST"])
def index():
    return render_template("index.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        session.pop("user", None)
        if request.form["password"] == "password":
            session["user"] = request.form["username"]
        return redirect(url_for("login.html"))
    return render_template("login.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    return render_template("register.html")

@app.route("/shopping_list", methods=["GET", "POST"])
def shopping_list():
    return render_template("shopping_list.html")

@app.route("/logout",)
def loggout():
    logout_user()
    return redirect(url_for("login.html"))

if __name__ == "__main__":
    app.run(debug=True)
