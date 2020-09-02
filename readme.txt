scaffolded out in line with:
https://www.freecodecamp.org/news/structuring-a-flask-restplus-web-service-for-production-builds-c2ec676de563/


Useful commands:

Migrations:
sudo python manage.py db migrate --message '<Migration Message>'
sudo python manage.py db upgrade

Testing:
sudo python manage.py test

Running:
sudo python manage.py run



Example insert of property against Portfolio in shell:
port = Portfolio.query.first()
new_property = Property(portfolio_id=1, purchase_price=234561, purchase_date=datetime.datetime(2020,3,12))
port.properties.append(new_property)
db.session.commit()



test@test.com
test


Idea's
Add error logging to a mongodb database