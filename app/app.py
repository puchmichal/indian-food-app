import os
from statistics import mean

from flask import Flask, render_template, flash, request
from flask_bootstrap import Bootstrap
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_user import UserManager, roles_required

from werkzeug.utils import redirect


app = Flask(__name__)
bootstrap = Bootstrap(app)
app.config.from_object(os.environ.get("APP_CONFIG"))
db = SQLAlchemy(app)
migrate = Migrate(app, db)


from app.models import Restaurant, Rating, User

user_manager = UserManager(app, db, User)


@app.route("/")
def get_all_restaurants():
    restaurants = db.session.query(Restaurant)

    if not restaurants:
        return "No ratings by now :C"

    restaurants_list = [
        {
            "name": restaurant.name,
            "general_rating": mean(
                [mean([rating.delivery, rating.taste]) for rating in restaurant.ratings]
            ),
            "taste_rating": mean([rating.taste for rating in restaurant.ratings]),
            "delivery_rating": mean([rating.delivery for rating in restaurant.ratings]),
            "spiciness_rating": mean([rating.spiciness for rating in restaurant.ratings]),
        }
        for restaurant in restaurants if not restaurant.want_to_go
    ]

    return render_template("leaderboard.html", title="Leader Board", restaurants=restaurants_list)


@app.route("/add_visit", methods=["GET", "POST"])
def add_rating():
    if request.method == "POST":
        # validate form
        req = request.form
        missing = list()

        for k, v in req.items():
            if v == "":
                missing.append(k)

        if missing:
            feedback = f"Please fill fields: {', '.join(missing)}"
            restaurant_in_database = [
                restaurant.name for restaurant in db.session.query(Restaurant)
            ]
            if len(restaurant_in_database) == 0:
                restaurant_in_database = ["No restaurant added yet."]
            return render_template(
                "form.html",
                title="Add Visit",
                feedback=feedback,
                restaurants=restaurant_in_database,
            )

        # add data to database
        restaurant_in_database = list(
            db.session.query(Restaurant).filter_by(name=request.form.get("name"))
        )

        if len(restaurant_in_database) == 0:
            restaurant = Restaurant(name=request.form.get("name"), url=request.form.get("url"), want_to_go=False)
            db.session.add(restaurant)
            db.session.commit()
            restaurant_in_database = list(
                db.session.query(Restaurant).filter_by(name=request.form.get("name"))
            )

        restaurant_id = restaurant_in_database[0].id

        rating = Rating(
            taste=request.form.get("taste_rating"),
            delivery=request.form.get("delivery_rating"),
            spiciness=request.form.get("spiciness_rating"),
            restaurant_id=restaurant_id,
        )
        db.session.add(rating)
        db.session.commit()

        flash("Visit in restaurant {} has been added 🕉".format(request.form.get("name")))
        return redirect("/")

    restaurant_in_database = [restaurant.name for restaurant in db.session.query(Restaurant)]
    if len(restaurant_in_database) == 0:
        restaurant_in_database = ["No restaurant added yet."]

    return render_template("form.html", title="Add Visit", restaurants=restaurant_in_database)


@app.route("/add_want_to_go", methods=["GET", "POST"])
def add_want_to_go():
    if request.method == "POST":
        # validate form
        req = request.form
        missing = list()

        for k, v in req.items():
            if v == "":
                missing.append(k)

        if missing:
            feedback = f"Please fill fields: {', '.join(missing)}"

            return render_template(
                "add_want_to_go.html",
                title="Add Want To Go",
                feedback=feedback,
            )

        restaurant_in_database = [
            restaurant.name for restaurant in db.session.query(Restaurant)
        ]

        if request.form.get("name") in restaurant_in_database:
            feedback = f"You already have been in: {', '.join(missing)}"

            return render_template(
                "form.html",
                title="Add Visit",
                feedback=feedback,
            )

        restaurant = Restaurant(name=request.form.get("name"), url=request.form.get("url"), want_to_go=True)
        db.session.add(restaurant)
        db.session.commit()

        flash("Restaurant {} was added as want to go".format(request.form.get("name")))
        return redirect("/want_to_go")

    return render_template("add_want_to_go.html", title="Add Want To Go")


@app.route("/want_to_go")
def want_to_go():
    restaurants = db.session.query(Restaurant)

    if not restaurants:
        return "No ratings by now :C"

    restaurants_list = [
        {
            "name": restaurant.name,
            "general_rating": mean(
                [mean([rating.delivery, rating.taste]) for rating in restaurant.ratings]
            ),
            "taste_rating": mean([rating.taste for rating in restaurant.ratings]),
            "delivery_rating": mean([rating.delivery for rating in restaurant.ratings]),
        }
        for restaurant in restaurants if restaurant.want_to_go
    ]

    if len(restaurants_list) == 0:
        return "No restaurants to want to go to :C"

    return render_template("show_want_to_go.html", title="Want to go", restaurants=restaurants_list)



@app.route("/admin_panel")
@roles_required(["Admin"])
def admin_page():
    return "You are admin!"


if __name__ == "__main__":
    app.run()
