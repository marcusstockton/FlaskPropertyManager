
scaffolded out in line with:
https://www.freecodecamp.org/news/structuring-a-flask-restplus-web-service-for-production-builds-c2ec676de563/


Useful commands:

Migrations:
may need to: export FLASK_APP=manage.py from the root:
flask db migrate -m "<Migration Message>"
flask db upgrade


Testing:
sudo python manage.py test || flask test

Running:
sudo python manage.py run || flask run

Seeding:
sudo python manage.py seed || flask seed



Example insert of property against Portfolio in shell:
port = Portfolio.query.first()
new_property = Property(portfolio_id=1, purchase_price=234561, purchase_date= datetime.datetime(2020,3,12))
port.properties.append(new_property)
db.session.commit()



test@test.com | marcus_stockton@hotmail.co.uk
test


Idea's
Add error logging to a mongodb database
Update seeder to generate many more records - for loops?
Add Pydantic - https://pypi.org/project/Flask-Pydantic/