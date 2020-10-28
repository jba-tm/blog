release: python manage.py migrate
heroku run python manage.py shell
web: gunicorn blog.wsgi --log-file -