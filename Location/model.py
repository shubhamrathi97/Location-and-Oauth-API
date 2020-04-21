from sqlalchemy import func, Index

from app.model import db


# Define model
class Location(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80))
    lat = db.Column(db.Float())
    lng = db.Column(db.Float())
    # for faster calculation of Distance Difference
    Index('dist', func.ll_to_earth(lat, lng), postgresql_using='gist')

    def __init__(self, name, lat, lng):
        self.name = name
        self.lat = lat
        self.lng = lng
