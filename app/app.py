import os

from flask import Flask, render_template, flash
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from statistics import mean

from werkzeug.utils import redirect

from app.config import Config
from app.forms import NewRatingForm

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
SECRET_KEY = os.urandom(32)
app.config["SECRET_KEY"] = SECRET_KEY

from app.models import Restaurant, Rating

with app.app_context():
    migrate.init_app(app, db)


@app.route('/')
@app.route("/index")
def get_all_restaurants():
    restaurants = db.session.query(Restaurant)
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


@app.route('/form', methods=['GET', 'POST'])
def adding_rating():
    form = NewRatingForm()
    if form.validate_on_submit():
        restaurant_in_database = list(db.session.query(Restaurant).filter_by(name=form.name.data))

        if len(restaurant_in_database) == 0:
            restaurant = Restaurant(name=form.name.data)
            db.session.add(restaurant)
            db.session.commit()
            restaurant_in_database = list(
                db.session.query(Restaurant).filter_by(name=form.name.data))

        restaurant_id = restaurant_in_database[0].id

        rating = Rating(taste=form.taste_rating.data, delivery=form.delivery_rating.data, restaurant_id=restaurant_id)
        db.session.add(rating)
        db.session.commit()

        flash('Visit in restauarant {} has been added 🕉'.format(form.name.data))
        return redirect("/index")
    return render_template('form.html', title='Sign In', form=form)
