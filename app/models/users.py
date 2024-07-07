
from app.providers.app_provider import db
from flask_login import UserMixin

class User(UserMixin, db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    azure_id = db.Column(db.String(256), unique=True)
    name = db.Column(db.String(256))
    email = db.Column(db.String(256), unique=True)
    password = db.Column(db.String(256), nullable=True)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, server_default=db.func.now(), server_onupdate=db.func.now())

    def __repr__(self):
        return f"<User {self.email}>"
