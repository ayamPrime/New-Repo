import os
import sys
import traceback

# Ensure the project root is on sys.path so Django can find hub/settings.py
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hub.settings')

try:
    from hub.wsgi import application  # noqa: E402
except Exception:
    # Print the full traceback to stderr so it appears in Vercel function logs
    traceback.print_exc()
    raise

# Vercel expects the WSGI callable to be named `app`
app = application
