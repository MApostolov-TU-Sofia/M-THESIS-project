from flask_sqlalchemy import SQLAlchemy
from application import app, db

class User(db.Model):
    __tablename__ = 'at_users'

    id = db.Column(db.Integer, primary_key=True)
    login_type = db.Column(db.String(32), nullable=False)
    username = db.Column(db.String(256), unique=True, nullable=False)
    password = db.Column(db.String(256), nullable=False)
    salt = db.Column(db.String(128), nullable=False)
    role = db.Column(db.String(32), nullable=False)
    name = db.Column(db.String(512), nullable=True)
    address = db.Column(db.String(256), nullable=True)
    phone_nbr = db.Column(db.String(32), nullable=True)
    created_at = db.Column(db.Date, nullable=True)

    @property
    def serialize(self):
        return {
            'id': self.id,
            'login_type': self.login_type,
            'username': self.username,
            'password': self.password,
            'salt': self.salt,
            'role': self.role,
            'name': self.name,
            'address': self.address,
            'phone_nbr': self.phone_nbr,
            'created_at': self.created_at
        }
