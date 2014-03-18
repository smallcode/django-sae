import os
import sys

root = os.path.dirname(__file__)
sys.path.insert(0, os.path.join(root, 'site-packages123.zip'))

import sae

from app_name import wsgi

application = sae.create_wsgi_app(wsgi.application)