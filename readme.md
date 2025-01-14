# Dev Notes

This was just an idea for managing properties for landlords etc.

## Scaffolded out in line with

https://www.freecodecamp.org/news/structuring-a-flask-restplus-web-service-for-production-builds-c2ec676de563/

### Help

    flask --app manage.py --help

### Migrations

    flask --app manage.py db init
    flask --app manage.py db migrate -m "<Migration Message>"
    flask --app manage.py db upgrade

### Testing

    sudo python manage.py test || flask test

### Running

    sudo python manage.py run || flask run

### Seeding

    sudo python manage.py seed || flask seed

### Shell

    flask shell

### Example insert of property against Portfolio in shell

    from app.main.model.portfolio import Portfolio
    port = Portfolio.query.first()
    new_property = Property(portfolio_id=1, purchase_price=234561, purchase_date= datetime.datetime(2020,3,12))
    port.properties.append(new_property)
    db.session.commit()

#### Usernames

<test@test.com> | <marcus_stockton@hotmail.co.uk>\
test

## Idea's

* Add caching to auto-completes (AddressSearchList)
* Remove Flask-Caching and add in redis caching

### Docker Commands

``docker build -t flaskpropertymanager .``\
``docker run -it -p 5000:5000 flaskpropertymanager``\
``docker exec -it <container name> bash`` # to load up the docker image to navigate in linux\
``docker compose build`` # builds all images\
``docker compose build flask_app`` # Builds specific image\
``docker compose up -d`` # runs all images in detached mode\
``docker compose up -d --build``
``docker compose up -d flask_app`` # runs one particular image in detached mode

### Debugging against a docker container

Firstly, make sure docker desktop is running.\
Then you'll want to build the latest images (assuming something has changed since last time) and run them up\
Then, once both images are up and running, you can just hit the debug in vs code choosing the Python Debugger: Remote Attach option.\
Should get a blue bar along the bottom in vs code - should be good to go!\


### Ideas
Add deposit scheme for tenants - scheme, amount
When in rent paid, keep track of payments