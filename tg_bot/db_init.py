import json
import os
import sys
import random
import string

from django.core.exceptions import ImproperlyConfigured
from django.conf import settings
import django

sys.path.append(
    os.path.join(os.path.dirname(__file__), 'MentalStateTracker')
)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "django_project.settings")
django.setup()


from accounts.models import MentalState

get = lambda node_id: MentalState.objects.get(pk=node_id)

MentalState.objects.all().delete()
