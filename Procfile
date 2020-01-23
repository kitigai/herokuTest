web: gunicorn -k flask_sockets.worker main:app
worker: celery worker -A app.celery --loglevel=info