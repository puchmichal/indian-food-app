import os

from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from statistics import mean

from app.config import Config

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
SECRET_KEY = os.urandom(32)
app.config["SECRET_KEY"] = SECRET_KEY

from app.models import Restaurant

with app.app_context():
    migrate.init_app(app, db)


@app.route("/")
def get_all_restaurants():
    restaurants = db.session.query(Restaurant)
    restaurants_dict = {
        restaurant.name: mean(
            [mean([rating.delivery, rating.taste]) for rating in restaurant.ratings]
        )
        for restaurant in restaurants
    }
    return "\n".join(
        [
            restaurant + " with Rating: {}".format(rating)
            for restaurant, rating in restaurants_dict.items()
        ]
    )
