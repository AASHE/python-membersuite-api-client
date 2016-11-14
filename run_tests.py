import os
import sys
import django

BASE_PATH = os.path.dirname(__file__)

def main():
    """
    Standalone django model test with a 'memory-only-django-installation'.
    You can play with a django model without a complete django app installation.
    http://www.djangosnippets.org/snippets/1044/
    """

    os.environ["DJANGO_SETTINGS_MODULE"] = "django.conf.global_settings"
    from django.conf import global_settings

    global_settings.USE_TZ = True

    BASE_DIR = os.path.join(
        os.path.dirname(os.path.dirname(__file__)), "bulletin")

    global_settings.STATIC_URL = os.environ.get('STATIC_URL', '/static/')
    global_settings.STATIC_ROOT = os.environ.get(
        'STATIC_ROOT',
        os.path.join(BASE_DIR,
                     global_settings.STATIC_URL.strip('/')))

    global_settings.INSTALLED_APPS = (
        'django.contrib.admin',
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.sessions',
        'django.contrib.messages',
        'django.contrib.staticfiles',
        'django.contrib.sites',

        # AASHE Apps
        'membersuite-api-client.client'
    )

    if django.VERSION > (1, 2):
        global_settings.DATABASES = {
            'default': {
                'ENGINE': 'django.db.backends.sqlite3',
                'NAME': os.path.join(BASE_PATH, 'membersuite-api-client.sqlite'),
                'USER': '',
                'PASSWORD': '',
                'HOST': '',
                'PORT': '',
            }
        }
    else:
        global_settings.DATABASE_ENGINE = "sqlite3"
        global_settings.DATABASE_NAME = ":memory:"

    global_settings.SECRET_KEY = "blahblah"

    global_settings.SITE_ID = 1

    global_settings.AASHE_DRUPAL_URI = (
        "http://test.aashe.org/services/xmlrpc")

    from django.test.utils import get_runner
    test_runner = get_runner(global_settings)

    django.setup()

    if django.VERSION > (1, 2):
        test_runner = test_runner()
        failures = test_runner.run_tests(['membersuite-api-client'], fail_fast=True)
    else:
        failures = test_runner(['membersuite-api-client'], verbosity=1, fail_fast=True)
    sys.exit(failures)

if __name__ == '__main__':
    main()
