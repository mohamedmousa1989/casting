web: gunicorn casting_platform.wsgi
release: export SECRET_KEY='django-insecure-m^q+w19@p^zrqoi_twi2^95@9$&fw!m6y684ax8@a@!#4syn!e'
release: python manage.py makemigrations --noinput
release: python manage.py collectstatic --noinput
release: python manage.py migrate --noinput