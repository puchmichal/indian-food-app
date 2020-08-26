import os
from statistics import mean

from flask import Flask, render_template, flash, request
from flask_migrate import Migrate

from flask_sqlalchemy import SQLAlchemy

from werkzeug.utils import redirect

from app.forms import NewRatingForm

app = Flask(__name__)
app.config.from_object(os.environ.get("APP_SETTINGS",  "config.Config"))
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)
migrate = Migrate(app, db)

from app.models import Restaurant, Rating


@app.route('/')
def get_all_restaurants():
    restaurants = db.session.query(Restaurant)

    if not restaurants:
        return "No ratings by now :C"

    restaurants_list = [
        {"name": restaurant.name, "general_rating": mean(
            [mean([rating.delivery, rating.taste]) for rating in restaurant.ratings]
        ),
         "taste_rating":  mean(
            [rating.taste for rating in restaurant.ratings]
        ),
         "delivery_rating": mean(
            [rating.delivery for rating in restaurant.ratings]
        )}
        for restaurant in restaurants
    ]

    return render_template('leaderboard.html', title='Leader Board', restaurants=restaurants_list)


@app.route('/add_visit', methods=['GET', 'POST'])
def add_rating():
    if request.method == "POST":
        restaurant_in_database = list(db.session.query(Restaurant).filter_by(name=request.form.get("name")))

        if len(restaurant_in_database) == 0:
            restaurant = Restaurant(name=request.form.get("name"))
            db.session.add(restaurant)
            db.session.commit()
            restaurant_in_database = list(
                db.session.query(Restaurant).filter_by(name=request.form.get("name")))

        restaurant_id = restaurant_in_database[0].id

        rating = Rating(
            taste=request.form.get("taste_rating"),
            delivery=request.form.get("delivery_rating"),
            spiciness=request.form.get("spiciness_rating"),
            restaurant_id=restaurant_id,
        )
        db.session.add(rating)
        db.session.commit()

        flash("Visit in restauarant {} has been added 🕉".format(request.form.get("name")))
        return redirect("/")

    restaurant_in_database = list(db.session.query(Restaurant))

    return render_template('form.html', title='Sign In', restaurants=[restaurant.name for restaurant in restaurant_in_database] or ["hej"])


if __name__ == "__main__":
    app.run()
