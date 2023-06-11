<<<<<<< HEAD
"""
WSGI config for pr_dir project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application
from dj_static import Cling

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pr_dir.settings')

#application = get_wsgi_application()
application = Cling(get_wsgi_application())
=======
"""
WSGI config for pr_dir project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application
#from dj_static import Cling

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pr_dir.settings')

application = get_wsgi_application()
#application = Cling(get_wsgi_application())
>>>>>>> 4c2209e31cccae233283679f39cee79e6eabf3af
