release: python3 manage.py migrate
release: python3 manage.py createsuperuser
web: gunicorn core.wsgi --preload --log-file -
