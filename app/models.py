from app.app import db


class Rating(db.Model):
    __tablename__ = "rating"

    id = db.Column(db.Integer, primary_key=True)
    taste = db.Column(db.Float)
    delivery = db.Column(db.Float)
    spiciness = db.Column(db.Float)
    restaurant_id = db.Column(db.Integer, db.ForeignKey("restaurant.id"))

    def __repr__(self):
        return "<Taste Rating {}, Delivery Rating {}>".format(self.taste, self.delivery)


class Restaurant(db.Model):
    __tablename__ = "restaurant"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True, unique=True)
    ratings = db.relationship("Rating", backref="score", lazy="dynamic")

    def __repr__(self):
        return f"Restaurant {self.name}"
