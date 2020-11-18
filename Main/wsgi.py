
import os
import sys
sys.path.append("/opt/bitnami/projects/SocioMeet")
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('PYTHON_EGG_CACHE', '/opt/bitnami/projects/SocioMeet/egg_cache')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Main.settings')

application = get_wsgi_application()
