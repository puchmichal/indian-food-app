import os
from statistics import mean

from flask_migrate import Migrate
from flask_basicauth import BasicAuth
from flask import Flask

from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_object(os.environ["APP_SETTINGS"])
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

app.config["BASIC_AUTH_USERNAME"] = "kocham"
app.config["BASIC_AUTH_PASSWORD"] = "naany"
basic_auth = BasicAuth(app)

db = SQLAlchemy(app)
migrate = Migrate(app, db)

from app.models import Restaurant


@app.route("/")
@basic_auth.required
def get_all_restaurants():
    restaurants = db.session.query(Restaurant)

    if not restaurants:
        return "No ratings by now :C"

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


if __name__ == "__main__":
    app.run()
