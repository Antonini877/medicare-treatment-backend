from app import db

class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(250), unique=True, nullable=False)
    api_key = db.Column(db.String(250), unique=True, nullable=False)

    def __repr__(self):
        return f"User('{self.username}')"