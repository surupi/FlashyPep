from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func

class User(db.Model, UserMixin):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(30), unique=True, nullable = False)
    password = db.Column(db.String(300), nullable=False)
    date_created = db.Column(db.DateTime(timezone=True), default=func.now())
    score = db.Column(db.Integer, default = 0)
    udeck = db.relationship('Deck', cascade='all, delete-orphan', backref='deck')

class Deck(db.Model):
    __tablename__ = 'deck'
    id = db.Column(db.Integer, primary_key=True)
    deck_name = db.Column(db.String(30))
    user = db.Column(db.String, db.ForeignKey('user.username'), nullable=False)
    date_created = db.Column(db.DateTime(timezone=True), default=func.now())
    score = db.Column(db.Integer, default=0)
    is_public = db.Column(db.Boolean, default = False)
    last_rev = db.Column(db.DateTime(timezone=True), default=func.now())
    dcard = db.relationship('Card', cascade='all, delete-orphan', backref='card')

class Card(db.Model):
    __tablename__ = 'card'
    card_id = db.Column(db.Integer, primary_key=True)
    front = db.Column(db.String(512), nullable = False)
    back = db.Column(db.String(512), nullable = False)
    score = db.Column(db.Integer, default = 0)
    deck = db.Column(db.String, db.ForeignKey('deck.deck_name'), nullable = False)
