### Decisions

1. Python because it is the language I'm most familiar with.
2. SQLAlchemy because it is the ORM I'm most familiar with.
3. SQLite to minimize install footprint. I'm more comfortable with PostgreSQL but that would be overkill for this use case.
4. Flask web framework since this it's fast to prototype with.
5. Flask-Restful (instead of Flask-Restless) since we are only building one endpoint that won't be a simple CRUD operation.
6. To keep things simple I'm not implementing a caching strategy for the order books, we're going to get the relevant order book with each request.
7. I have the products/pairs load once when the app starts, since that does not change often.
8. Again to simplify, no asynchronous requests to GDAX or worrying about what happens if multiple requests come in simultaneously.
