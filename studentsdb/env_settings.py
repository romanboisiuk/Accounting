import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

PORTAL_URL = 'http://localhost:8000'

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '6q%3gq)&w0*#(@cq-yc_sx4x4*)aba67!5^*vixim90(+$4)u^'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

# please set here your smtp server details and admin email
ADMIN_EMAIL = '********'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = '465'
EMAIL_HOST_USER = '********'
EMAIL_HOST_PASSWORD = '********'
EMAIL_USE_TLS = False
EMAIL_USE_SSL = True


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'HOST': 'localhost',
        'USER': 'root',
        'PASSWORD': '123',
        'NAME': 'students_db',
    }
}

STATIC_URL = '/static/'
STATIC_ROOT = '/path/to/static/folder'
MEDIA_URL = '/media/' 
MEDIA_ROOT = '/path/to/media/folder'
