import os
import sys

# Get the current script's directory
script_dir = os.path.dirname(os.path.abspath(__file__))

# Calculate the path to the project's root directory (two levels up from script_dir)
project_dir = os.path.dirname(os.path.dirname(script_dir))

# Modify sys.path to include the project's root directory
sys.path.insert(0, project_dir)

# Now you can import the Django settings and use your models
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "pr_main.settings")
import django
from django.conf import settings

# Initialize Django
django.setup()

# Now you can import your models and perform operations
from app_base.models import MuUser, Currency, Islemler


user = MuUser.objects.get(id=1)
currency = Currency.objects.get(id=3)
balance = user.calculate_currency_balance(currency)
print(balance)
