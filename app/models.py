from statistics import mean

import pandas as pd
from flask_user import UserMixin

from app.app import db

from .util import format_date, format_nth_place


class Rating(db.Model):
    __tablename__ = "rating"

    id = db.Column(db.Integer, primary_key=True)
    taste = db.Column(db.Float)
    delivery = db.Column(db.Float)
    spiciness = db.Column(db.Float)
    restaurant_id = db.Column(db.Integer, db.ForeignKey("restaurant.id"))
    rate_by = db.Column(db.Integer)
    date = db.Column(db.Integer)

    @property
    def general_rating(self) -> float:
        return mean([self.delivery, self.taste])

    def show(self):
        return {
            "id": self.id,
            "taste": self.taste,
            "delivery": self.delivery,
            "spiciness": self.spiciness,
            "general_rating": self.general_rating,
            "restaurant": db.session.query(Restaurant).filter_by(id=self.restaurant_id).first(),
            "rate_by": db.session.query(User).filter_by(id=self.rate_by).first(),
            "date": format_date(self.date),
        }

    def __repr__(self):
        return "<Taste Rating {}, Delivery Rating {}>".format(self.taste, self.delivery)


class Restaurant(db.Model):
    __tablename__ = "restaurant"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True, unique=True)
    url = db.Column(db.String(255))
    want_to_go = db.Column(db.Boolean)
    ratings = db.relationship("Rating", backref="score", lazy="dynamic")

    @property
    def number_of_ratings(self) -> int:
        return len([rating.taste for rating in self.ratings])

    @property
    def number_of_users_rated(self) -> int:
        return len(set(rating.rate_by for rating in self.ratings))

    @property
    def general_rating(self):
        return mean([rating.general_rating for rating in self.ratings])

    @property
    def ratings_df(self) -> pd.DataFrame:
        return pd.DataFrame([rating.show() for rating in self.ratings])

    def restaurants_df(self) -> pd.DataFrame:
        restaurant_data = [
            {
                "id": restaurant.id,
                "name": restaurant.name,
                "general_rating": restaurant.general_rating,
                "taste_rating": mean([rating.taste for rating in restaurant.ratings]),
                "delivery_rating": mean([rating.delivery for rating in restaurant.ratings]),
                "spiciness_rating": mean([rating.spiciness for rating in restaurant.ratings]),
            }
            for restaurant in db.session.query(Restaurant)
            if not restaurant.want_to_go
        ]
        return pd.DataFrame(restaurant_data)

    @property
    def place(self):
        df = self.restaurants_df().sort_values(by="general_rating", ascending=False)
        place = df[df["name"] == self.name].index.values.item() + 1

        return format_nth_place(place)

    def __repr__(self):
        return f"{self.name}"


class User(db.Model, UserMixin):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False, server_default="")
    active = db.Column(db.Boolean(), nullable=False, server_default="0")
    roles = db.relationship("Role", secondary="user_roles")

    def __repr__(self):
        return f"{self.username}"


class Role(db.Model):
    __tablename__ = "roles"

    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(50), unique=True)

    def __repr__(self):
        return f"{self.name}"


class UserRoles(db.Model):
    __tablename__ = "user_roles"

    id = db.Column(db.Integer(), primary_key=True)
    user_id = db.Column(db.Integer(), db.ForeignKey("users.id", ondelete="CASCADE"))
    role_id = db.Column(db.Integer(), db.ForeignKey("roles.id", ondelete="CASCADE"))
