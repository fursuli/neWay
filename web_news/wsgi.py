"""
WSGI config for web_news project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangopfrom helloworld.wsgi import HelloWorldApplication
application = HelloWorldApplication(application)roject.com/en/3.0/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'web_news.settings')

application = get_wsgi_application()

