"""import the necessary modules"""
import os
import hashlib
from flask import Flask, render_template, redirect, request, session, url_for, flash
from wtforms import Form, StringField, validators, PasswordField, TextAreaField
# from shopping_list import shopping_list

app = Flask(__name__)
app.config.from_object("config")

@app.route("/", methods=["GET", "POST"])
def index():
    """define the index function"""
    return render_template("index.html")

class RegistrationForm(Form):
    """authorization class defined"""
    username = StringField("Username", [validators.Length(min=-1, max=50)])
    email = StringField("Email", [validators.Length(min=6, max=35)])
    password = PasswordField("Password", [validators.DataRequired(),
                validators.EqualTo("confirm", message="Passwords do not match")])
    confirm = PasswordField("Confirm Password")
@app.route("/register", methods=["GET", "POST"])
def register():
    """define register function"""
    form = RegistrationForm(request.form)
    if request.method != "POST":
        return render_template("register.html", form=form)

    username = request.form['username']
    password = request.form['password']
    # email = request.form["email"]

    session["username"] = username

    hashed_password = hashlib.sha256(password.encode()).hexdigest()
    session["password"] = hashed_password

    flash("Successfully registered. You can now log in", "success")
    return redirect(url_for("login"))

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
                flash("Successfully logged in. Proceed to shopping...", "success")
                return redirect(url_for("shopping_list"))
            else:
                error = "Username and Password did not match" 
                return render_template("login.html", error=error)
        else:
            error = "Wrong username and password" 
            return render_template("login.html", error=error)
    else:
        return render_template("login.html")

# shopping_list = shopping_list()

@app.route("/shopping_list", methods=["GET", "POST"])
def shopping_list():
    """define shopping list function"""
    return render_template("shopping_list.html") 


class ShoppingListForm(Form):
    """shoppinglistform class defined"""
    item = TextAreaField("item", [validators.Length(min=-1, max=100)])
    session["items"] = []


@app.route("/add_item", methods=["GET", "POST"])
def add_item():
    """function for adding an item"""
    if request.method == "POST":
        item = request.form["item"]

        if 'items' not in session:
            # session["items"] = []

            session["items"].append(item)
        
        flash("Added one item to your list", "success")
        return redirect(url_for("view_item"))
    
    return render_template("add_item.html")

@app.route("/view_item", methods=["GET"])
def view_item():
    """function for viewing items"""
    items =  [] if 'items' not in session else session['items']
    return render_template("view_item.html", items=items)

@app.route("/update_item/<int:item_id>", methods=["GET", "POST"])
def update_item(self, item_id, item):
    """method for editing an item in the list"""
    # Get users items
    if request.method == "POST":
        lst = self.session["items"]
        for item_id in range(len(lst)):
            out = {'item': item, "item_id": item_id}
            old_item = out['item']
            new_item = request.form.get('new_item')
            self.session["items"][item_id] = new_item

            return redirect(url_for("view_item"))
    return render_template("update_item.html", old_item =old_item, item_id=item_id)

@app.route("/delete_item", methods=["GET", "POST"])
def delete_item():
    """function for adding an item"""
    pass

@app.route("/logout",)
def logout():
    """define logout function"""
    session.clear()
    flash("You are logged out!", "success")
    return redirect(url_for("login.html"))


if __name__ == "__main__":
    app.secret_key = os.urandom(12)
    app.run(debug=True)#Helps the server to automatically save changes in the browser