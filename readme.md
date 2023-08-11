# Dev Notes
This was just an idea for managing properties for landlords etc.

## Scaffolded out in line with:
https://www.freecodecamp.org/news/structuring-a-flask-restplus-web-service-for-production-builds-c2ec676de563/

## Useful commands:
may need to:
* Ubuntu: ``export FLASK_APP=manage.py`` from the root
* Windows: ``set FLASK_APP=manage.py`` from the root or ``set FLASK_APP=FlaskPropertyManager``

### Migrations:
    python -m flask --app manage.py db migrate -m "<Migration Message>"
    python -m flask --app manage.py db upgrade

### Testing:
    sudo python manage.py test || flask test

### Running:
    sudo python manage.py run || flask run

### Seeding:
    sudo python manage.py seed || flask seed

### Shell:
    flask shell

### Example insert of property against Portfolio in shell:
    from app.main.model.portfolio import Portfolio
    port = Portfolio.query.first()
    new_property = Property(portfolio_id=1, purchase_price=234561, purchase_date= datetime.datetime(2020,3,12))
    port.properties.append(new_property)
    db.session.commit()


## Usernames
test@test.com | marcus_stockton@hotmail.co.uk
test


## Idea's
* Add error logging to a mongodb database
* Add caching to auto-completes (AddressSearchList)
