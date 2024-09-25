"""
WSGI config for movie_review_project project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/howto/deployment/wsgi/
"""

# import os



# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'movie_review_project.settings')

# application = get_wsgi_application()





import os
import sys
from django.core.wsgi import get_wsgi_application

# Add your project directory to the sys.path
project_home = '/home/your_username/yourprojectdirectory'
if project_home not in sys.path:
    sys.path = [project_home] + sys.path

# Set environment variable for Django settings module
os.environ['DJANGO_SETTINGS_MODULE'] = 'yourprojectname.settings'

# Activate virtual environment
activate_this = '/home/your_username/yourprojectdirectory/venv/bin/activate_this.py'
with open(activate_this) as file_:
    exec(file_.read(), dict(__file__=activate_this))

# Import Django's WSGI handler to handle requests
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
