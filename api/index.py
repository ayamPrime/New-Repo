import os
import sys

# Ensure the project root is on sys.path so Django can find hub/settings.py
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hub.settings')

from hub.wsgi import application  # noqa: E402

# Vercel expects the WSGI callable to be named `app`
app = application
