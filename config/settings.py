from pathlib import Path
from decouple import Config, RepositoryEnv, Csv
from django.core.exceptions import ImproperlyConfigured

BASE_DIR = Path(__file__).resolve().parent.parent
env = Config(RepositoryEnv(str(BASE_DIR / '.env.example' if not (BASE_DIR / '.env').exists() else BASE_DIR / '.env')))
SECRET_KEY = env('SECRET_KEY')
DEBUG = env('DEBUG', default=False, cast=bool)
if not DEBUG and (SECRET_KEY.startswith('development-') or len(SECRET_KEY) < 50):
    raise ImproperlyConfigured('Configure una SECRET_KEY privada de al menos 50 caracteres.')
ALLOWED_HOSTS = env('ALLOWED_HOSTS', default='localhost,127.0.0.1', cast=Csv())
INSTALLED_APPS = ['django.contrib.admin', 'django.contrib.auth', 'django.contrib.contenttypes', 'django.contrib.sessions', 'django.contrib.messages', 'django.contrib.staticfiles', 'blog']
MIDDLEWARE = ['django.middleware.security.SecurityMiddleware', 'django.contrib.sessions.middleware.SessionMiddleware', 'django.middleware.common.CommonMiddleware', 'django.middleware.csrf.CsrfViewMiddleware', 'django.contrib.auth.middleware.AuthenticationMiddleware', 'django.contrib.messages.middleware.MessageMiddleware', 'django.middleware.clickjacking.XFrameOptionsMiddleware']
ROOT_URLCONF = 'config.urls'
TEMPLATES = [{'BACKEND': 'django.template.backends.django.DjangoTemplates', 'DIRS': [BASE_DIR / 'templates'], 'APP_DIRS': True, 'OPTIONS': {'context_processors': ['django.template.context_processors.request', 'django.contrib.auth.context_processors.auth', 'django.contrib.messages.context_processors.messages']}}]
WSGI_APPLICATION = 'config.wsgi.application'
DATABASES = {'default': {'ENGINE': 'django.db.backends.sqlite3', 'NAME': BASE_DIR / 'db.sqlite3'}}
AUTH_PASSWORD_VALIDATORS = [{'NAME': 'django.contrib.auth.password_validation.' + name} for name in ['UserAttributeSimilarityValidator', 'MinimumLengthValidator', 'CommonPasswordValidator', 'NumericPasswordValidator']]
LANGUAGE_CODE = 'es-ar'
TIME_ZONE = 'America/Argentina/Buenos_Aires'
USE_I18N = True
USE_TZ = True
STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
STATIC_ROOT = BASE_DIR / 'staticfiles'
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
LOGIN_URL = 'login'
LOGIN_REDIRECT_URL = 'post_list'
LOGOUT_REDIRECT_URL = 'post_list'
SESSION_COOKIE_HTTPONLY = True
SESSION_COOKIE_SECURE = not DEBUG
CSRF_COOKIE_SECURE = not DEBUG
SECURE_SSL_REDIRECT = not DEBUG
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'
