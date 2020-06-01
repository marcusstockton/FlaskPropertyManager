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