# Django settings for baia_dos_piratas project.

import os
PROJECT_PATH = os.path.dirname(os.path.realpath(__file__))
DEBUG = False 
TEMPLATE_DEBUG = DEBUG

LOGIN_URL = '/login/'
LOGIN_REDIRECT_URL = '/'

ADMINS = (
    # ('Your Name', 'your_email@example.com'),
)

MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'baia_dos_piratas.db',                      # Or path to database file if using sqlite3.
        # The following settings are not used with sqlite3:
        'USER': '',
        'PASSWORD': '',
        'HOST': '',                      # Empty for localhost through domain sockets or '127.0.0.1' for localhost through TCP.
        'PORT': '',                      # Set to empty string for default.
    }
}

# Hosts/domain names that are valid for this site; required if DEBUG is False
# See https://docs.djangoproject.com/en/1.5/ref/settings/#allowed-hosts
ALLOWED_HOSTS = []

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# In a Windows environment this must be set to your system time zone.
TIME_ZONE = 'America/Chicago'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale.
USE_L10N = True

# If you set this to False, Django will not use timezone-aware datetimes.
USE_TZ = True

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/var/www/example.com/media/"
MEDIA_ROOT = ''

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://example.com/media/", "http://media.example.com/"
MEDIA_URL = ''

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/var/www/example.com/static/"
STATIC_ROOT = 'static'

# URL prefix for static files.
# Example: "http://example.com/static/", "http://static.example.com/"
STATIC_URL = '/static/'

# Additional locations of static files
STATICFILES_DIRS = (
        os.path.join(PROJECT_PATH, 'static'),
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

# For pipeline :D
PIPELINE = True
PIPELINE_VERSION = True
PIPELINE_URL = '/static/'

STATICFILES_STORAGE = 'pipeline.storage.PipelineCachedStorage'
PIPELINE_STORAGE = 'pipeline.storage.PipelineFinderStorage'

# PIPELINE_CSSMIN_BINARY = 'cssmin'
# PIPELINE_CSS_COMPRESSOR = 'pipeline.compressors.cssmin.CSSMinCompressor'
# PIPELINE_JS_COMPRESSOR = 'pipeline.compressors.slimit.SlimItCompressor'

PIPELINE_CSS_COMPRESSOR = 'pipeline.compressors.yuglify.YuglifyCompressor'
PIPELINE_JS_COMPRESSOR = 'pipeline.compressors.yuglify.YuglifyCompressor'

PIPELINE_CSS = {
    'base': {
        'source_filenames': (
            'css/*',
        ),
        'output_filename': 'min.css',
        'variant': 'datauri',
    },
}

PIPELINE_JS = {
    'jquery': {
        'source_filenames': (
            'js/jquery/*.js',
        ),
        'output_filename': 'jquery.js',
    },
    'base': {
        'source_filenames': (
            'js/*.js',
        ),
        'output_filename': 'min.js',
    },
}


# PIPELINE_CSS_COMPRESSOR = 'pipeline.compressors.yuglify.YuglifyCompressor'
# PIPELINE_JS_COMPRESSOR = 'pipeline.compressors.yuglify.YuglifyCompressor'
# PIPELINE_JS = {
#     'base_scripts': {
#         'source_filenames': (
#           'js/main.js',
#           'js/vote.js',
#         ),
#         'output_filename': '/js/min/all.js',
#     }
# }

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'a44yucl0(4j6^@bj%%)1rw6p3p6tfdmp61u^2e^3_e_ryn)mp4'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)

USE_X_FORWARDED_HOST = True

ALLOWED_HOSTS = ['bdp.denislee.net', '.denislee.net', 'web410.webfaction.com', \
    'localhost.localdomain', 'localhost', '127.0.0.1', '10.61.31.82', '108.168.242.154', \
    '0.0.0.0', '.bdp.denislee.net', 'denislee.webfaction.com', '*']

MIDDLEWARE_CLASSES = (
    'django.middleware.gzip.GZipMiddleware',
    'htmlmin.middleware.HtmlMinifyMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',

    # 'webfaction.multipleProxyMiddleware',
    # Uncomment the next line for simple clickjacking protection:
    # 'django.middleware.clickjacking.XFrameOptionsMiddleware',
)



ROOT_URLCONF = 'main.urls'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'main.wsgi.application'

TEMPLATE_DIRS = (
    os.path.join(PROJECT_PATH, 'templates'),
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # Uncomment the next line to enable the admin:
    'django.contrib.admin',
    # Uncomment the next line to enable admin documentation:
    # 'django.contrib.admindocs',
    # 'torrent',
    'pipeline',
    'opensubtitles',
)

# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error when DEBUG=False.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}
