# Home Budget Website

## About a website

This website is made to help with managing monthly budgeting. Click the link below to check website.

## Functionalities

Functionalities of the site include:
- adding income
- creating monthly budgeting
- adding value, category and a note to each spending
- displaying spendings by a period of time
- adding savings and displaying the history of it
- displaying balance of budgeting and spendings

## Technologies

Technologies used:
- Flask
- SQLite
- SQLAlchemy
- HTML
- Jinja

Frontend is based on [Bootstrap](https://getbootstrap.com/).

## Tests

The code is tested manually and by unit tests.

## How to run
To install the required libraries run:

```
pip install -r requirements.txt
```

To initialize the database run:
```
flask shell
from app import db
db.create_all()
```

To run the app, simply run:
```
python app.py
```
