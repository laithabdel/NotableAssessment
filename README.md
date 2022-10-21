# NotableAssessment - Assessment for Notable Interview

This assessment was developed using the Django framework. This implements the
Calendar API according to the specs given. It also uses an SQLLite local database
for storage.

Install dependencies through requirements.txt using pip

To run migrations:
./manage.py migrate

To run the server:
./manage.py runserver

To run unit tests:
rm -rf unit.xml;source env1/bin/activate; python3 manage.py test