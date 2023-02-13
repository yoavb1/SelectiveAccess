"""
WSGI config for IntegratedInformation project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/howto/deployment/wsgi/
"""

# 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
# https://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@github.com/yoavb1/IntegratedInformation.git

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'IntegratedInformation.settings')

application = get_wsgi_application()
