from flask.helpers import flash
from flask.templating import render_template
from flask_restful import Resource, Api
from flask_restful import fields, marshal_with
from flask_restful import reqparse
from .models import User, Deck, Card
from . import db
from flask import current_app as app
import werkzeug
from flask import abort, redirect, url_for
from werkzeug.security import generate_password_hash
import random

user_post_args = reqparse.RequestParser()
user_post_args.add_argument('username')
user_post_args.add_argument('password')

card_put_args = reqparse.RequestParser()
card_put_args.add_argument('score')

deck_post_args = reqparse.RequestParser()
deck_post_args.add_argument('deck_name')

card_post_args = reqparse.RequestParser()
card_post_args.add_argument('front')
card_post_args.add_argument('back')


class UserAPI(Resource):
    def post(self):
        args = user_post_args.parse_args()
        u = User.query.filter_by(username=args['username']).first()
        if u:
            flash('Username is already in use.', category='error')
            return redirect('/register')
        elif len(args['username']) < 6:
            flash('Username is too short.', category='error')
            return redirect('/register')
        elif len(args['password']) < 6:
            flash('Password is too short.', category='error')
            return redirect('/register')

        new_user = User(username=args['username'],
                        password=generate_password_hash(args['password'],
                                                        method='sha256'))
        try:
            db.session.add(new_user)
            db.session.commit()
            return redirect('/login')
        except:
            return redirect('/register')

    def get(self, username):
        u = User.query.filter_by(username=username).first()
        d = Deck.query.filter_by(user=username)
        dn = d.count()
        score = [deck.score for deck in d]
        return {"username": u.username, "deck_count": dn, "score": score}


class DeckAPI(Resource):
    def post(self, username):
        args = deck_post_args.parse_args()
        qd = Deck.query.filter_by(user=username)
        ud = []
        for c in qd:
            ud.append(c.deck_name)
        d = Deck(deck_name=args['deck_name'], user=username)
        db.session.add(d)
        db.session.commit()
        return redirect('/dashboard')

    def get(self, username):
        decks = Deck.query.filter_by(user=username)

        r = []
        for deck in decks:
            r.append({
                'deck_name': deck.deck_name,
                'score': deck.score,
                'last_rev': str(deck.last_rev)
            })
        print(r)
        return r


class CardAPI(Resource):
    def post(self, deck):
        args = card_post_args.parse_args()
        new_card = Card(front=args['front'], back=args['back'], deck=deck)
        db.session.add(new_card)
        db.session.commit()
        return redirect(f'/review/{deck}')

    def get(self, deck, username):

        decks = Deck.query.filter_by(user=username, deck_name=deck)
        decknames = [d.deck_name for d in decks]
        if deck in decknames:
            cards = Card.query.filter_by(deck=deck)
            cl = []
            if cards:
                for c in cards:
                    cl.append(c)
                random.shuffle(cl)
                rc = cl.pop()
                return {
                    "card_id": rc.card_id,
                    "deck": rc.deck,
                    "front": rc.front,
                    "back": rc.back
                }
            return {}
        return None

    def put(self, card_id):
        c = Card.query.filter_by(card_id=int(card_id)).first()
        args = card_put_args.parse_args()
        c.score = args['score']
        db.session.commit()
