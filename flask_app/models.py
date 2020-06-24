from flask_app import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    active = db.Column(db.Integer, default=0)

    def __repr__(self):
        return f"User('{self.id}', '{self.username}', '{self.email}', '{self.password}', '{self.active}')"