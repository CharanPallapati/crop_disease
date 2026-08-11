from datetime import datetime, timezone
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

def utcnow():
    return datetime.now(timezone.utc)

class User(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    name=db.Column(db.String(120), nullable=False)
    email=db.Column(db.String(255), unique=True, nullable=False, index=True)
    password_hash=db.Column(db.String(255), nullable=False)
    language=db.Column(db.String(20), default="en")
    created_at=db.Column(db.DateTime(timezone=True), default=utcnow)

    def set_password(self, password):
        self.password_hash=generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Scan(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    user_id=db.Column(db.Integer, db.ForeignKey("user.id"), nullable=True, index=True)
    image_path=db.Column(db.String(500), nullable=False)
    crop=db.Column(db.String(100))
    disease=db.Column(db.String(150))
    confidence=db.Column(db.Float)
    latitude=db.Column(db.Float)
    longitude=db.Column(db.Float)
    decision=db.Column(db.String(30))
    weather_score=db.Column(db.Float)
    result_json=db.Column(db.JSON)
    created_at=db.Column(db.DateTime(timezone=True), default=utcnow)
