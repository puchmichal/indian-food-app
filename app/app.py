import os
from statistics import mean

from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_user import UserManager, roles_required

app = Flask(__name__)
app.config.from_object(os.environ.get("APP_CONFIG"))
db = SQLAlchemy(app)
migrate = Migrate(app, db)

from app.models import Restaurant, User

user_manager = UserManager(app, db, User)


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


@app.route("/admin_panel")
@roles_required(["Admin"])
def admin_page():
    return "You are admin!"


if __name__ == "__main__":
    app.run()
