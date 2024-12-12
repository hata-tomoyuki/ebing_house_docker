release: python manage.py collectstatic --noinput
web: sh -c 'gunicorn config.wsgi --bind 0.0.0.0:${PORT:-8000} --log-file -'
