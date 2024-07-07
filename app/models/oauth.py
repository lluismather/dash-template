
from app.providers.app_provider import db
from app.models.users import User
from flask_dance.consumer.storage.sqla import OAuthConsumerMixin

class OAuth(OAuthConsumerMixin, db.Model):
    __tablename__ = "flask_dance_oauth"
    id = db.Column(db.Integer, primary_key=True)
    provider_user_id = db.Column(db.String(256), unique=True, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey(User.id), nullable=False)
    provider = db.Column(db.String(256))
    token = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=db.func.now())
    updated_at = db.Column(db.DateTime, default=db.func.now(), onupdate=db.func.now())
    user = db.relationship(User)

    def __repr__(self):
        return f"<OAuth {self.provider_user_id}>"
