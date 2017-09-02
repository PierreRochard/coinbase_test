### Decisions

1. Python because I am familiar with it and it's easy for the reviewer to setup. I would otherwise do this with pl/pgSQL and PostgREST.
2. SQLAlchemy because it is the ORM I'm most familiar with.
3. SQLite to minimize install footprint. I'm more comfortable with PostgreSQL but that would be overkill for this use case. Unfortunately SQLite does not have a decimal precision type so there may be float imprecision that we wouldn't have with PostgreSQL. (one workaround would be to multiply out to be integer)
4. Flask web framework since this it's fast to prototype with.
5. Flask-Restful (instead of Flask-Restless) since we are only building one endpoint that won't be a simple CRUD operation.
6. To keep things simple I'm not implementing a caching strategy for the order books, we're going to get the relevant order book with each request.
7. I have the products/pairs load once when the app starts, since that does not change often.
8. Again to simplify, no asynchronous requests to GDAX or worrying about what happens if multiple requests come in simultaneously.
9. Leverage the DB to perform the quote calculation instead of loading the data in memory. This is one of my pet-peeves, I think SQL is often underutilized.


### Wishlist if I had more time

1. Integration test for a range of values and for each pair, using mock data so test expectations can be hard coded.
2. Unit tests for the different queries and methods.
3. A live updating order book like I did with https://github.com/PierreRochard/coinbase-exchange-order-book using websockets so that we're not polling the Coinbase API with every request that comes in.
