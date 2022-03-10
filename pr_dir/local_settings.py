# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'iyk$#3asdfsfs##1&uvp1-gbn7%pgfgdfgdfgsagk6sa#(q=k(jjh@rk3ueo#4lgt0o'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = ['46.101.149.71', 'localhost', 'servicebay.ru', 'www.servicebay.ru']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'servicebay',
        'USER': 'servicebayadmin',
        'PASSWORD': 'ylhio65v',
        'HOST': 'localhost',
        'PORT': '5432'
    }
}