# Dev Notes

This was just an idea for managing properties for landlords etc.

## Development setup

This project runs using Docker Compose.

### Prerequisites

1. Docker Desktop
2. VS Code (recommended)
3. Python tooling is not required locally when running through Docker.

## Scaffolded out in line with

https://www.freecodecamp.org/news/structuring-a-flask-restplus-web-service-for-production-builds-c2ec676de563/

### Start the application

Build and start all services:
```docker compose up -d --build```
#### This will:

1. Start PostgreSQL
2. Wait for PostgreSQL to become healthy
3. Run database migrations
4. Start the Flask application
5. Start Redis
6. Start smtp4dev

The application is available at: ```http://localhost:5000```

## View logs

All services:

```docker compose logs -f```

Flask application only:

```docker compose logs -f flask_app```

PostgreSQL only:

```docker compose logs -f flask_db```

## Docker commands

### Start

Start the existing containers: ```docker compose up -d```

Build and start: ```docker compose up -d --build```

Stop the application: ```docker compose down```

Restart: ```docker compose restart```

### Rebuild

Rebuild everything: ```docker compose build```

Rebuild only the Flask application: ```docker compose build flask_app```

Usually, however, you can simply use: ```docker compose up -d --build``` which rebuilds what is necessary and starts the services.


## Accessing the Flask container

Open a shell inside the running Flask container: ```docker compose exec flask_app sh```

The image uses Alpine Linux, so sh is available rather than bash.

Alternatively, execute a command directly: ```docker compose exec flask_app flask --help```

## Database

PostgreSQL is available to the application at: ```flask_db:5432```
From the host machine it is exposed at: ```localhost:5433```

### Migrations

Create a migration: ```docker compose exec flask_app flask db migrate -m "Migration message"```

Apply migrations: ```docker compose exec flask_app flask db upgrade```

Check the current migration: ```docker compose exec flask_app flask db current```

View migration history: ```docker compose exec flask_app flask db history```

Database migrations are automatically applied when the Flask container starts.

#### Initialising migrations

Only required if setting up the project from scratch without an existing migrations directory: ```docker compose exec flask_app flask db init```

## Seed data

Seed the development database: ```docker compose exec flask_app flask seed```

This can be run whenever the database needs to be populated with development data.

## Testing

Run the test suite: ```docker compose exec flask_app flask test```

## Flask shell

Open a Flask shell: ```docker compose exec flask_app flask shell```

For example:

```
    from app.main.model.portfolio import Portfolio
    from app.main.model.property import Property
    from app.main import db

    portfolio = Portfolio.query.first()

    new_property = Property(
        portfolio_id=1,
        purchase_price=234561,
        purchase_date=datetime.datetime(2020, 3, 12)
    )

    portfolio.properties.append(new_property)
    db.session.commit()
```

## Development users

| Username | Password |
|--------  | -------- |
| test@test.com | test |
| marcus_stockton@hotmail.co.uk | test |

These credentials are for local development only.


## Debugging with VS Code

Make sure Docker Desktop is running.

Start the application with: ```docker compose up -d --build```

Once the containers are running, use the VS Code Python Debugger: Remote Attach configuration.

The Flask container must expose the debugger port when using the debugger configuration.

## Useful Docker commands

See running services: ```docker compose ps```

Follow application logs: ```docker compose logs -f flask_app```

Restart Flask: ```docker compose restart flask_app```

Open a shell in Flask: ```docker compose exec flask_app sh```

Open PostgreSQL: ```docker compose exec flask_db psql -U postgres -d postgres```

Stop everything: ```docker compose down```

Stop everything and remove the database volume:
> **Warning** this deletes the development database. ```docker compose down -v```

This is particularly useful when you want to simulate a completely fresh installation:

```docker compose down -v```

```docker compose up -d --build```

```docker compose exec flask_app flask seed```

## CORS testing

Test a CORS preflight request:

```curl -i -X OPTIONS http://localhost:5000/portfolio/ -H "Origin: http://localhost:3000" -H "Access-Control-Request-Method: GET"```

## Project ideas

- Add caching to autocomplete endpoints (AddressSearchList)
- Replace Flask-Caching with Redis caching
- Add tenant deposit scheme tracking:
    - Scheme
    - Deposit amount
    - Reference
    - Start/end dates
    - Track rent payments
    - Add rent payment history against tenants
    - Add deposit scheme information to tenant records
