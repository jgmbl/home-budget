from flask import Flask, redirect, render_template, request, session, url_for, abort
from flask_session import Session
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import select, ForeignKey
from sqlalchemy.orm import relationship, backref
from flask_login import LoginManager, UserMixin, login_user, LoginManager, logout_user, current_user, login_required
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Length, ValidationError, EqualTo
from flask_bcrypt import Bcrypt
from datetime import date
from userbudgeting import UserBudgeting
from userspendings import UserSpendings
from usersavings import UserSavings
from usersummary import UserSummary



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
    note = db.Column(db.String(100))
    date = db.Column(db.DateTime, nullable=False)


class Budgeting(db.Model):
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user_database = db.relationship("User", backref=backref("user_budgeting", uselist=False))
    income = db.Column(db.Integer, nullable=False)
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
    password = PasswordField(validators=[InputRequired(), Length(min=6, max=25)], render_kw={"placeholder": "Password"})
    confirm_password = PasswordField(validators=[InputRequired(), Length(min=6, max=25), EqualTo('password')], render_kw={"placeholder": "Confirm password"})
    submit = SubmitField("Register")

    def validate_username(self, username):
        existing_user_username = User.query.filter_by(username=username.data).first()
        if existing_user_username:
            raise ValidationError("Username is taken")


class LoginForm(FlaskForm):
    username = StringField(validators=[InputRequired(), Length(min=6, max=25)], render_kw={"placeholder": "Username"})
    password = PasswordField(validators=[InputRequired(), Length(min=6, max=25)], render_kw={"placeholder": "Password"})
    submit = SubmitField("Login")



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
                    return render_template("error.html", statement="Invalid password.")
        
            else:
                return render_template("error.html", statement="Invalid username.")
    
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
            return render_template("error.html", statement="Invalid username or password.")

    else:
        return render_template("register.html", form=form)


@app.route("/", methods=["GET"])
@login_required
def summary():
    date_today = date.today()
    week_day = date_today.strftime('%A')
    user_id = session["_user_id"]
    database = "instance/budget.db"

    logged_user_savings = UserSavings()
    logged_user_spendings = UserSpendings()
    logged_user_summary = UserSummary(UserBudgeting.display_last_income(user_id, database))

    current_month_savings = logged_user_savings.sum_of_savings_current_month(user_id, database)
    current_month_spendings = logged_user_spendings.sum_of_categories_from_current_month(user_id, database)
    current_month_income = UserBudgeting.display_last_income(user_id, database)
    current_month_budgeting = UserBudgeting.display_budgeting(user_id, database)

    balance_budgeting_spendings = logged_user_summary.balance_of_budgeting_spendings_month(user_id, database)

    return render_template("summary.html", week_day=week_day, date_today=date_today, savings=current_month_savings, budgeting=current_month_budgeting, spendings=current_month_spendings, income=current_month_income, balance=balance_budgeting_spendings)


@app.route("/budgeting", methods=["GET", "POST"])
@login_required
def budgeting():
    date_today = date.today()
    week_day = date_today.strftime('%A')

    user_id = session["_user_id"]
    database = "instance/budget.db"

    #show data in table
    budgeting_table = UserBudgeting.display_budgeting(user_id, database)

    if request.method == "POST":
        #get requests from form
        income = float(request.form.get("income"))
        daily_spendings = int(request.form.get("daily_spendings"))
        large_spendings = int(request.form.get("large_spendings"))
        investments = int(request.form.get("investments"))
        education = int(request.form.get("education"))
        others = int(request.form.get("others"))

        logged_user_budgeting = UserBudgeting(income)

        #change income from dollars to cents
        logged_user_budgeting.float_to_int_value()

        #check errors
        if UserBudgeting.check_sum_of_percent(daily_spendings, large_spendings, investments, education, others) == False:
            abort(400, "Sum of percent must be equal 100")

        #add values to table budgeting
        logged_user_budgeting.add_budgeting_to_table("daily spendings", daily_spendings, user_id, database)
        logged_user_budgeting.add_budgeting_to_table("large spendings", large_spendings, user_id, database)
        logged_user_budgeting.add_budgeting_to_table("investments", investments, user_id, database)
        logged_user_budgeting.add_budgeting_to_table("education", education, user_id, database)
        logged_user_budgeting.add_budgeting_to_table("others", others, user_id, database)

        return redirect("/budgeting")
    
    else:
        return render_template("budgeting.html", week_day=week_day, date_today=date_today, table=budgeting_table)


@app.route("/spendings", methods=["GET", "POST"])
@login_required
def spendings():
    logged_user_spendings = UserSpendings()

    date_today = date.today()
    week_day = date_today.strftime('%A')
    user_id = session["_user_id"]
    database = "instance/budget.db"

    if request.method == "POST":
        #get requests from form
        value = float(request.form.get("value"))
        note = request.form.get("note")
        category = request.form.get("category")

        #change dollars to cents
        value = logged_user_spendings.float_to_int_value(value)

        #add data to table spendings
        logged_user_spendings.add_spendings_to_table(category, value, note, user_id, database)
            
        return redirect("/spendings")
    
    else:
        return render_template("spendings.html", week_day=week_day, date_today=date_today)


@app.route("/showspendings", methods=["GET", "POST"])
@login_required
def show_spendings():
    logged_user_spendings = UserSpendings()
    user_id = session["_user_id"]
    database = "instance/budget.db"

    current_month_spendings = logged_user_spendings.get_spendings_from_current_month(user_id, database)
    current_week_spendings = logged_user_spendings.get_spendings_from_current_week(user_id, database)
    all_spendings = logged_user_spendings.get_all_spendings(user_id, database)

    period = ""
    sum_categories = {}

    date_today = date.today()
    week_day = date_today.strftime('%A')

    if request.method == "POST":
        display_spendings = request.form.get("display_spendings")
        
        if display_spendings == "last_month":
            period_of_spendings = current_month_spendings
            period = "last month"

        elif display_spendings == "last_week":
            period_of_spendings = current_week_spendings
            period = "last week"

        elif display_spendings == "all":
            period_of_spendings = all_spendings
            period = "all periods"

        sum_categories = logged_user_spendings.display_sum_of_categories(display_spendings, user_id, database)


        return render_template("showspendings.html", week_day=week_day, date_today=date_today, display_data=period_of_spendings, period=period, sum_categories=sum_categories)
    
    else:
        return render_template("showspendings.html", week_day=week_day, date_today=date_today, sum_categories=sum_categories)


@app.route("/savings", methods=["GET", "POST"])
@login_required
def savings():
    logged_user_savings = UserSavings()
    user_id = session["_user_id"]
    database = "instance/budget.db"

    date_today = date.today()
    week_day = date_today.strftime('%A')

    month_information = {}

    if request.method == "POST":
        value = float(request.form.get("value"))

        #change dollars to cents
        value = logged_user_savings.float_to_int_value(value)

        #add data to table
        logged_user_savings.add_data_to_table(value, user_id, database)


        return redirect("/savings")
    
    else:
        #add data to current month savings
        month_information = logged_user_savings.display_current_month_information

        #add data to history table
        display_data_to_table = logged_user_savings.display_data_table_savings(user_id, database)

        return render_template("savings.html", week_day=week_day, date_today=date_today,month_information=month_information, display_data=display_data_to_table)
    


if __name__ == "__main__":
    app.run(debug=True)