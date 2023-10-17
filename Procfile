release: python manage.py makemigrations && python manage.py migrate && python manage.py collectstatic
 web: gunicorn pp5_api.wsgi