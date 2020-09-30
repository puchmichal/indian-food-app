from flask_user import UserMixin

from app.app import db


class Rating(db.Model):
    __tablename__ = "rating"

    id = db.Column(db.Integer, primary_key=True)
    taste = db.Column(db.Float)
    delivery = db.Column(db.Float)
    spiciness = db.Column(db.Float)
    restaurant_id = db.Column(db.Integer, db.ForeignKey("restaurant.id"))
    rate_by = db.Column(db.Integer)
    date = db.Column(db.Integer)

    def __repr__(self):
        return "<Taste Rating {}, Delivery Rating {}>".format(self.taste, self.delivery)


class Restaurant(db.Model):
    __tablename__ = "restaurant"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True, unique=True)
    url = db.Column(db.String(255))
    want_to_go = db.Column(db.Boolean)
    ratings = db.relationship("Rating", backref="score", lazy="dynamic")

    def __repr__(self):
        return f"Restaurant {self.name}"


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
