from flask_app import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(15), unique=True, nullable=False)
    email = db.Column(db.String(25), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    is_active = db.Column(db.Integer, default=0)

    def __repr__(self):
        return f"User('{self.id}', '{self.username}', '{self.email}', '{self.password}', '{self.active}')"


class Token(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    token = db.Column(db.String(255), nullable=False)
    short = db.Column(db.String(255), nullable=False)

    def __repr__(self):
        return f"Secure('{self.id}', '{self.token}', '{self.short}')"
