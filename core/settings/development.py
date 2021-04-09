# Development settings for Noys

import os

from core.settings.base import *  # noqa: F403,F401

MIDDLEWARE += (
    'debug_toolbar.middleware.DebugToolbarMiddleware',
    'django_pdb.middleware.PdbMiddleware',
)

INSTALLED_APPS += (
    'django_sass',
    'django_pdb',
    'template_repl',
    'debug_toolbar',
)

DEBUG_TOOLBAR_CONFIG = {
    'INTERCEPT_REDIRECTS': False,
    'SHOW_TOOLBAR_CALLBACK': (lambda x: True),
}

MEDIA_ROOT = os.path.join(PROJECT_ROOT, 'public/media')

STATIC_ROOT = os.path.join(PROJECT_ROOT, 'public/static')

# Django Extensions settings
SHELL_PLUS = "ipython"

SHELL_PLUS_PRINT_SQL = True
