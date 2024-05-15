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
from app_base.models import MuGroup

# Use your models and perform operations
# mu_instance = Blog_model(title="deneme1", content="content1")
# mu_instance.save()

# default_group, created = MuGroup.objects.get_or_create(name="DefaultGroup")

# if created:
#     print(default_group)
# else:
#     print("else printed")
from app_base.models import Yetkiler, MuGroup

from app_base.models import MuUser

# user = MuUser.objects.get(pk=4)
# user = MuUser.objects.all()
user = MuUser.all_objects.get(pk=4)
print(user)  # Assign the Yetkiler instance to the yetkiler field
