import datetime
import os
from statistics import mean

from flask import Flask, Response, abort, flash, render_template, request
from flask_bootstrap import Bootstrap
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_user import (UserManager, current_user, login_required,
                        roles_required, user_registered)
from werkzeug.utils import redirect

app = Flask(__name__)
bootstrap = Bootstrap(app)
app.config.from_object(os.environ.get("APP_CONFIG"))
db = SQLAlchemy(app)
migrate = Migrate(app, db)


from app.models import Rating, Restaurant, Role, User

user_manager = UserManager(app, db, User)


@user_registered.connect_via(app)
def _after_user_registered_hook(sender, user, **extra):
    """This function add default 'User' role to every new registrated guest."""

    default_role = Role.query.filter_by(name="User").first()
    admin_role = Role.query.filter_by(name="Admin").first()

    if not default_role:
        default_role = Role(name="User")

    if not admin_role:
        admin_role = Role(name="Admin")

    user.roles.append(default_role)
    db.session.add(default_role)
    db.session.add(admin_role)
    db.session.commit()


@app.route("/")
def get_all_restaurants():
    return render_template(
        template_name_or_list="leaderboard.html",
        title="Leader Board",
        restaurants=Restaurant.restaurants_df(Restaurant),
    )


@app.route("/profile")
@login_required
def profile():
    ratings = db.session.query(Rating).filter_by(rate_by=current_user.id)
    ratings = [rating.show() for rating in ratings]

    return render_template(
        template_name_or_list="profile.html",
        title="Profile",
        ratings=ratings,
    )


@app.route("/restaurant/<int:restaurant_id>")
def restaurant_profile(restaurant_id: int = None):
    restaurant = db.session.query(Restaurant).filter_by(id=restaurant_id).first()

    if not restaurant:
        abort(Response("Restaurant does not exist", 404))
    else:
        return render_template(
            template_name_or_list="restaurant.html",
            title="Restauran profile",
            place=restaurant.place,
            number_of_ratings=restaurant.number_of_ratings,
            number_of_users_rated=restaurant.number_of_users_rated,
            url=restaurant.url,
            name=restaurant.name,
        )


@app.route("/add_visit", methods=["GET", "POST"])
@login_required
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
        restaurant_in_database = (
            db.session.query(Restaurant).filter_by(name=request.form.get("name")).first()
        )

        if not restaurant_in_database:
            restaurant = Restaurant(
                name=request.form.get("name"), url=request.form.get("url"), want_to_go=False
            )
            db.session.add(restaurant)
            db.session.commit()
            restaurant_in_database = (
                db.session.query(Restaurant).filter_by(name=request.form.get("name")).first()
            )
        elif restaurant_in_database.want_to_go:
            restaurant_in_database.want_to_go = False
            db.session.commit()

        restaurant_id = restaurant_in_database.id

        rating = Rating(
            taste=request.form.get("taste_rating"),
            delivery=request.form.get("delivery_rating"),
            spiciness=request.form.get("spiciness_rating"),
            restaurant_id=restaurant_id,
            rate_by=current_user.id,
            date=datetime.datetime.today().strftime("%Y%m%d"),
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
@login_required
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

        restaurant_in_database = [restaurant.name for restaurant in db.session.query(Restaurant)]

        if request.form.get("name") in restaurant_in_database:
            feedback = f"You already have been in: {', '.join(missing)}"

            return render_template(
                "form.html",
                title="Add Visit",
                feedback=feedback,
            )

        restaurant = Restaurant(
            name=request.form.get("name"), url=request.form.get("website"), want_to_go=True
        )
        db.session.add(restaurant)
        db.session.commit()

        flash("Restaurant {} was added as want to go".format(request.form.get("name")))
        return redirect("/want_to_go")

    return render_template("add_want_to_go.html", title="Add Want To Go")


@app.route("/want_to_go")
def want_to_go():
    restaurants = db.session.query(Restaurant)

    restaurants_list = [
        {
            "name": restaurant.name,
            "url": restaurant.url,
        }
        for restaurant in restaurants
        if restaurant.want_to_go
    ]

    return render_template("show_want_to_go.html", title="Want to go", restaurants=restaurants_list)


@app.route("/admin_panel", methods=["GET", "POST"])
@roles_required(["Admin", "User"])
def admin_panel():
    if request.method == "GET":

        user_data = {}

        for user in db.session.query(User):
            roles = [role.name for role in user.roles]
            user_data[user.username] = {"User": "User" in roles, "Admin": "Admin" in roles}

        return render_template("users.html", title="Admin Panel", users=user_data)
    else:
        users = db.session.query(User)
        user_role = db.session.query(Role).filter_by(name="User").first()
        admin_role = db.session.query(Role).filter_by(name="Admin").first()

        available_roles = [user_role, admin_role]

        for user in users:
            for role in available_roles:

                role_in_db = role in user.roles
                role_in_form = user.username + "_is_" + role.name in request.form.keys()

                if role_in_form and not role_in_db:
                    user.roles.append(role)
                    db.session.commit()

                elif not role_in_form and role_in_db:
                    user.roles.remove(role)
                    db.session.commit()

                else:
                    continue

        return redirect("/admin_panel")


if __name__ == "__main__":
    app.run()
