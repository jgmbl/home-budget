from flask import Flask, redirect, render_template, request, session
from flask_session import Session
import db
import os
from flask_sqlalchemy import SQLAlchemy


# Configure application
app = Flask(__name__)


# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# initialize database
app.config['DATABASE'] = 'budget.db'
database = db.init_app(app)
