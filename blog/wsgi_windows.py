import os
import sys
import site
from django.core.wsgi import get_wsgi_application

# add python site packages, you can use virtualenvs also
# site.addsitedir("C:/xampp/htdocs/App/venv/Lib/site-packages/")
site.addsitedir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
site.addsitedir(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'blog'))
site.addsitedir(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'venv/Lib/site-packages/'))


# Add the app's directory to the PYTHONPATH 
# sys.path.append('C:/Projects/Application')
# sys.path.append('C:/Projects/Application/Application')

os.environ['DJANGO_SETTINGS_MODULE'] = 'blog.settings.production'
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "blog.settings.production")

application = get_wsgi_application()
