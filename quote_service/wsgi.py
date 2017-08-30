from quote_service import create_app
from quote_service.extensions import db
from quote_service.models.currency_pairs import CurrencyPairs

app = create_app()
with app.app_context():
    db.drop_all()
    db.create_all()
    CurrencyPairs.insert_pairs()

if __name__ == '__main__':
    app.run(debug=True)
