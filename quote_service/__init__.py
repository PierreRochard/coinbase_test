from flask import Flask

from quote_service.api import QuoteService
from quote_service.extensions import api, db
from quote_service.models import CurrencyPairs, Orders


def create_app():
    app = Flask(__name__)

    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///quote_service.sqlite'
    app.config['SQLALCHEMY_ECHO'] = False
    db.init_app(app)

    api.add_resource(QuoteService, '/')
    api.init_app(app)

    return app
