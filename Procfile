release: python3 manage.py migrate
release: python3 manage.py createsuperuser
web: gunicorn gettingstarted.wsgi --preload --log-file -
