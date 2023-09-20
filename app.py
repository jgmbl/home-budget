from flask import Flask, redirect, render_template, request, session, url_for
from flask_session import Session
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import select, ForeignKey
from sqlalchemy.orm import relationship, backref
from flask_login import LoginManager, UserMixin, login_user, LoginManager, logout_user, current_user, login_required
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Length, ValidationError, EqualTo
from flask_bcrypt import Bcrypt
import getpass

#configure database
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///budget.db'
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)


#configure security session cookie
app.config['SECRET_KEY'] = 'e338ad3e3496373c1be998218674fa2876bd05fb95879f17d4e10b4b79124416'


#configure log in
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))



#database tables
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(300), nullable=False)

    def __repr__(self):
        return '<User %r>' % self.username


class Spendings(db.Model):
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user_database = db.relationship("User", backref=backref("user_spendings", uselist=False))
    category = db.Column(db.String(20), nullable=False)
    value = db.Column(db.Integer, nullable=False)
    date = db.Column(db.DateTime, nullable=False)


class Budgeting(db.Model):
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user_database = db.relationship("User", backref=backref("user_budgeting", uselist=False))
    category = db.Column(db.String(20), nullable=False)
    value = db.Column(db.Integer, nullable=False)
    value_percent = db.Column(db.Integer, nullable=False)
    date = db.Column(db.DateTime, nullable=False)


class Savings(db.Model):
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user_database = db.relationship("User", backref=backref("user_savings", uselist=False))
    value = db.Column(db.Integer, nullable=False)
    value_summary = db.Column(db.Integer, nullable=False)
    date = db.Column(db.DateTime, nullable=False)



class RegisterForm(FlaskForm):
    username = StringField(validators=[InputRequired(), Length(min=6, max=25)], render_kw={"placeholder": "Username"})
    password = StringField(validators=[InputRequired(), Length(min=6, max=25)], render_kw={"placeholder": "Password"})
    confirm_password = StringField(validators=[InputRequired(), Length(min=6, max=25), EqualTo('password')], render_kw={"placeholder": "Confirm password"})
    submit = SubmitField("Register")

    def validate_username(self, username):
        existing_user_username = User.query.filter_by(username=username.data).first()
        if existing_user_username:
            raise ValidationError("Username is taken")



class LoginForm(FlaskForm):
    username = StringField(validators=[InputRequired(), Length(min=6, max=25)], render_kw={"placeholder": "Username"})
    password = StringField(validators=[InputRequired(), Length(min=6, max=25)], render_kw={"placeholder": "Password"})
    submit = SubmitField("Login")


@app.route("/", methods=["GET", "POST"])
@login_required
def index():
    print(current_user)
    return render_template("homepage.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()

    if request.method == "POST":
        if form.validate_on_submit():
            user = User.query.filter_by(username=form.username.data).first()
            if user:
                if bcrypt.check_password_hash(user.password, form.password.data):
                    login_user(user)
                    return redirect("/")
    
    else:
        return render_template("login.html", form=form)


@app.route("/logout", methods = ["GET", "POST"])
@login_required
def logout():
    logout_user()
    return redirect("/login")


@app.route("/register", methods=["GET", "POST"])
def register():
    form = RegisterForm()

    if request.method == "POST":
        if form.validate_on_submit():
            hashed_password = bcrypt.generate_password_hash(form.password.data)
            new_user = User(username=form.username.data, password=hashed_password)
            db.session.add(new_user)
            db.session.commit()

            return redirect("/login")

    else:
        return render_template("register.html", form=form)
    

@app.route("/spendings", methods=["GET", "POST"])
def spendings():
    if request.method == "POST":
        return redirect("/spendings")
    
    else:
        return render_template("spendings.html")


@app.route("/savings", methods=["GET", "POST"])
def savings():
    if request.method == "POST":
        return redirect("/savings")
    
    else:
        return render_template("savings.html")



if __name__ == "__main__":
    app.run(debug=True)