from flask import Flask, redirect, render_template, request, session
from flask_session import Session
from flask_sqlalchemy import SQLAlchemy
from classes import HomeBudget, Users


# Configure application
db = SQLAlchemy()
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///budget.db"
db.init_app(app)


@app.route("/", methods=["GET", "POST"])
def index():
    return render_template("homepage.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    session.clear()

    if request.method == "POST":
        

        return redirect("/")
    
    else:
        return render_template("login.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    """User registration"""
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        confirm_password = request.form.get("confirm_password")

        if password != confirm_password:
            return render_template("error.html")
        
        return redirect("/")
    
    else:
        return render_template("register.html")


if __name__ == "__main__":
    app.run()