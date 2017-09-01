from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy


errors = {
    'InvalidOperation': {
        'message': "A user with that username already exists.",
        'status': 409,
    },
}


api = Api(errors=errors)
db = SQLAlchemy()
