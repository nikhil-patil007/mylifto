"""
WSGI config for project project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')

application = get_wsgi_application()



# import sys, os

# cwd = os.getcwd()
# sys.path.append(cwd)
# sys.path.append(cwd + '/project')

# INTERP = os.path.expanduser("~/.virtualenvs/project/bin/python3")

# if sys.executable != INTERP: os.execl(INTERP, INTERP, *sys.argv)

# sys.path.insert(0,'$HOME/.virtualenvs/project/bin')
# sys.path.insert(0,'$HOME/.virtualenvs/project/lib/python3.5/site-packages/django')
# sys.path.insert(0,'$HOME/.virtualenvs/project/lib/python3.5/site-packages')

# os.environ['DJANGO_SETTINGS_MODULE'] = 'project.settings'
# from django.core.wsgi import get_wsgi_application
# application = get_wsgi_application()
# application = PassengerPathInfoFix(application)