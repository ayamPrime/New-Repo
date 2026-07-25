"""
WSGI config for hub project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/6.0/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hub.settings')

application = get_wsgi_application()
Running build in Washington, D.C., USA (East) – iad1
Build machine configuration: 2 cores, 8 GB
Cloning github.com/ayamPrime/VaseCrib (Branch: main, Commit: 50efaef)
Previous build caches not available.
Cloning completed: 314.000ms
Found .vercelignore
Removed 0 ignored files defined in .vercelignore
Running "vercel build"
Vercel CLI 56.5.0
Running "install" command: `uv pip install -r requirements.txt --system`...
Using Python 3.9.25 environment at: /usr
  × No solution found when resolving dependencies:
  ╰─▶ Because the current Python version (3.9.25) does not satisfy
      Python>=3.12 and django==6.0.6 depends on Python>=3.12, we can conclude
      that django==6.0.6 cannot be used.
      And because you require django==6.0.6, we can conclude that your
      requirements are unsatisfiable.
Error: Command "uv pip install -r requirements.txt --system" exited with 1
Summary
