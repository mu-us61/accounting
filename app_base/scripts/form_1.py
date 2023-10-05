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
from app_base.models import Islemler, Tag, MuUser


# Get the MuUser instances for islemsahibi, kimden_geldi, and kime_gitti
islemsahibi_user = MuUser.objects.get(username="admin")
kimden_geldi_user = MuUser.objects.get(username="a")
kime_gitti_user = MuUser.objects.get(username="a")
# Check if the tags exist, and create them if they don't
tag1, created1 = Tag.objects.get_or_create(name="Tag1")
tag2, created2 = Tag.objects.get_or_create(name="Tag2")

# Create a new transaction object
new_transaction = Islemler(
    islemsahibi=islemsahibi_user,
    kimden_geldi=kimden_geldi_user,
    kime_gitti=kime_gitti_user,
    islem_ismi="Some Transaction",
    islem_aciklamasi="Description of the transaction",
    bakiye_ilk_TL=100,
    girdiler_TL=50,
    ciktilar_TL=50,
)

# Save the transaction
new_transaction.save()

# Associate tags with the transaction
# tag1 = Tag.objects.get(name="Tag1")
# tag2 = Tag.objects.get(name="Tag2")
new_transaction.tags.add(tag1, tag2)
