from app import db
from datetime import datetime
from sqlalchemy.sql import func


class Occurrences(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, unique=False, nullable=False)
    pain =  db.Column(db.Integer, unique=False, nullable=False)
    description = db.Column(db.String(250), unique=False, nullable=True)
    created = db.Column(db.DateTime, default=func.now, nullable=False)


   