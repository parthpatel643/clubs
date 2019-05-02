from .common import *  # noqa

# database settings
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
        # 'ENGINE': 'django.db.backends.mysql',
        # 'OPTIONS': {
        #     'read_default_file': os.path.join(BASE_DIR, 'portal.cnf'),
        # },
    }
}

# email settings
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# django-cors-headers settings
CORS_ORIGIN_WHITELIST = (
    'localhost:3000',
)
