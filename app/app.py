import os
from statistics import mean

from flask_migrate import Migrate
from flask import Flask

from flask_sqlalchemy import SQLAlchemy

from dotenv import load_dotenv


app = Flask(__name__)
load_dotenv()

app.config.from_object(os.environ["APP_SETTINGS"])
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)
migrate = Migrate(app, db)

from app.models import Restaurant


@app.route("/")
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
