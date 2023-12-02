import os
import sys
from django.contrib.auth.hashers import make_password
from faker import Faker  # Install faker using: pip install faker
from phonenumber_field.phonenumber import PhoneNumber
from random import randint, choice
from decimal import Decimal


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

# Import your Django models
from app_base.models import Tag

# Create Tag instances from tag1 to tag9
tag_names = ["tag1", "tag2", "tag3", "tag4", "tag5", "tag6", "tag7", "tag8", "tag9", "tag10", "tag11", "tag12", "tag13", "tag14", "tag15", "tag16", "tag17", "tag18", "tag19", "tag20", "tag21", "tag22", "tag23", "tag24", "tag25", "tag26", "tag27", "tag28", "tag29"]

for tag_name in tag_names:
    tag, created = Tag.objects.get_or_create(name=tag_name)

    if created:
        print(f"Tag '{tag_name}' created successfully.")
    else:
        print(f"Tag '{tag_name}' already exists.")

# //------------------------~~--------------------------------------------------------------------------

# Import your Django models
from app_base.models import MuGroup
from django.utils import timezone

# Create 25 MuGroup instances
for i in range(1, 26):
    group_name = f"Group {i}"
    group, created = MuGroup.objects.get_or_create(name=group_name, defaults={"creation_date": timezone.now(), "is_active": True})

    if created:
        print(f"MuGroup '{group_name}' created successfully.")
    else:
        print(f"MuGroup '{group_name}' already exists.")
# //------------------------~~--------------------------------------------------------------------------
# Import your Django models
from app_base.models import Currency

# List of real-world currencies and their abbreviations
currencies = [
    {"name": "US Dollar", "abbreviation": "USD"},
    {"name": "Euro", "abbreviation": "EUR"},
    {"name": "Japanese Yen", "abbreviation": "JPY"},
    {"name": "British Pound", "abbreviation": "GBP"},
    {"name": "Australian Dollar", "abbreviation": "AUD"},
    {"name": "Canadian Dollar", "abbreviation": "CAD"},
    {"name": "Swiss Franc", "abbreviation": "CHF"},
    {"name": "Chinese Yuan", "abbreviation": "CNY"},
    {"name": "Swedish Krona", "abbreviation": "SEK"},
    {"name": "New Zealand Dollar", "abbreviation": "NZD"},
    {"name": "Mexican Peso", "abbreviation": "MXN"},
    {"name": "Singapore Dollar", "abbreviation": "SGD"},
    {"name": "Hong Kong Dollar", "abbreviation": "HKD"},
    {"name": "Norwegian Krone", "abbreviation": "NOK"},
    {"name": "South Korean Won", "abbreviation": "KRW"},
    {"name": "Turkish Lira", "abbreviation": "TRY"},
    {"name": "Russian Ruble", "abbreviation": "RUB"},
    {"name": "Indian Rupee", "abbreviation": "INR"},
    {"name": "Brazilian Real", "abbreviation": "BRL"},
    {"name": "South African Rand", "abbreviation": "ZAR"},
    {"name": "Danish Krone", "abbreviation": "DKK"},
    {"name": "Polish Zloty", "abbreviation": "PLN"},
    {"name": "Thai Baht", "abbreviation": "THB"},
    {"name": "Indonesian Rupiah", "abbreviation": "IDR"},
    {"name": "Saudi Riyal", "abbreviation": "SAR"},
]

# Create instances for each currency
for currency_data in currencies:
    currency_name = currency_data["name"]
    currency_abbreviation = currency_data["abbreviation"]

    currency, created = Currency.objects.get_or_create(name=currency_name, abbreviation=currency_abbreviation, defaults={"is_active": True})

    if created:
        print(f"Currency '{currency_name}' ({currency_abbreviation}) created successfully.")
    else:
        print(f"Currency '{currency_name}' ({currency_abbreviation}) already exists.")

# //------------------------~~--------------------------------------------------------------------------
# Import your Django models
from app_base.models import MuUser

# Initialize Faker
fake = Faker()

# Create instances for MuUser
for _ in range(25):
    username = fake.user_name()
    password = make_password(fake.password())  # Hash the password
    full_name = fake.name()  # Generate a full name

    # Splitting the full name into first name and last name
    first_name, *_ = full_name.split()

    # Create MuUser instance
    mu_user, created = MuUser.objects.get_or_create(username=username, defaults={"password": password, "first_name": first_name, "email": fake.email(), "is_staff": False, "is_active": True, "date_joined": fake.date_time_between(start_date="-2y", end_date="now", tzinfo=None)})

    if created:
        print(f"MuUser '{username}' created successfully.")
    else:
        print(f"MuUser '{username}' already exists.")

# //------------------------~~--------------------------------------------------------------------------
# Import your Django models
from app_base.models import ExelUsers
from app_base.models import Islemler, EvrakModel, EtkinlikModel

# Initialize Faker
fake = Faker()

# Create instances for ExelUsers
for _ in range(25):
    name = fake.name()
    phone_number = PhoneNumber.from_string(fake.phone_number())

    exel_user, created = ExelUsers.objects.get_or_create(name=name, defaults={"phonenumber": phone_number, "date": fake.date_time_this_year(before_now=True, after_now=False, tzinfo=None), "last_updated": fake.date_time_between(start_date="-1y", end_date="now", tzinfo=None), "is_active": True})

    if created:
        print(f"ExelUser '{name}' created successfully.")
    else:
        print(f"ExelUser '{name}' already exists.")
# //------------------------~~--------------------------------------------------------------------------
# Initialize Faker
fake = Faker()

# Fetching all users, exel users, tags, and currencies
mu_users = MuUser.objects.all()
exel_users = ExelUsers.objects.all()
tags = Tag.objects.all()
currencies = Currency.objects.all()

# Create instances for Islemler
for _ in range(25):
    islem_tarihi = fake.date_time_this_year(before_now=True, after_now=False, tzinfo=None)
    islemsahibi = choice(mu_users)
    kimden_geldi = choice(mu_users) if randint(0, 1) == 1 else None
    kime_gitti = choice(mu_users) if randint(0, 1) == 1 else None
    exel_users_list = [choice(exel_users) for _ in range(randint(0, 3))]
    tags_list = [choice(tags) for _ in range(randint(0, 3))]
    islem_ismi = fake.catch_phrase()
    islem_aciklamasi = fake.paragraph()
    currency = choice(currencies)
    miktar = Decimal(randint(100, 10000))

    # Create Islemler instance
    islemler_instance = Islemler.objects.create(islem_tarihi=islem_tarihi, islemsahibi=islemsahibi, kimden_geldi=kimden_geldi, kime_gitti=kime_gitti, islem_ismi=islem_ismi, islem_aciklamasi=islem_aciklamasi, currency=currency, miktar=miktar, is_active=True)

    islemler_instance.exelusers.set(exel_users_list)
    islemler_instance.tags.set(tags_list)

    # Assuming the functions generate_unique_imagename and generate_unique_filename are available and working
    # islemler_instance.islemler_picture = 'your_generated_image_field_value'
    # islemler_instance.islemler_pdf = 'your_generated_file_field_value'

    islemler_instance.save()
    print(f"Islemler '{islem_ismi}' created successfully.")
# //------------------------~~--------------------------------------------------------------------------
# Initialize Faker
fake = Faker()

# Fetching all users and tags
mu_users = MuUser.objects.all()
tags = Tag.objects.all()

# Choices for evrak_type
EVRAK_TYPE_CHOICES = ["gelen", "giden"]

# Create instances for EvrakModel
for _ in range(25):
    evrak_date = fake.date_time_this_year(before_now=True, after_now=False, tzinfo=None)
    evrak_last_updated = fake.date_time_between(start_date="-1y", end_date="now", tzinfo=None)
    evrak_owner = choice(mu_users)
    evrak_tags_list = [choice(tags) for _ in range(fake.random_int(0, 3))]
    evrak_name = fake.catch_phrase()
    evrak_description = fake.paragraph()
    evrak_type = choice(EVRAK_TYPE_CHOICES)

    # Create EvrakModel instance
    evrak_instance = EvrakModel.objects.create(evrak_date=evrak_date, evrak_last_updated=evrak_last_updated, evrak_owner=evrak_owner, evrak_name=evrak_name, evrak_description=evrak_description, evrak_type=evrak_type, is_active=True)

    evrak_instance.evrak_tags.set(evrak_tags_list)

    # Assuming the functions generate_unique_imagename and generate_unique_filename are available and working
    # evrak_instance.evrak_picture = 'your_generated_image_field_value'
    # evrak_instance.evrak_pdf = 'your_generated_file_field_value'

    evrak_instance.save()
    print(f"EvrakModel '{evrak_name}' created successfully.")
# //------------------------~~--------------------------------------------------------------------------
# Initialize Faker
fake = Faker()

# Fetching all users and tags
mu_users = MuUser.objects.all()
tags = Tag.objects.all()

# Create instances for EtkinlikModel
for _ in range(25):
    etkinlik_date = fake.date_time_this_year(before_now=True, after_now=False, tzinfo=None)
    etkinlik_last_updated = fake.date_time_between(start_date="-1y", end_date="now", tzinfo=None)
    etkinlik_owner = choice(mu_users)
    etkinlik_name = fake.catch_phrase()
    etkinlik_description = fake.paragraph()
    etkinlik_tags_list = [choice(tags) for _ in range(fake.random_int(0, 3))]
    etkinlik_youtubelink = fake.url() if fake.boolean(chance_of_getting_true=70) else None

    # Create EtkinlikModel instance
    etkinlik_instance = EtkinlikModel.objects.create(etkinlik_date=etkinlik_date, etkinlik_last_updated=etkinlik_last_updated, etkinlik_owner=etkinlik_owner, etkinlik_name=etkinlik_name, etkinlik_description=etkinlik_description, etkinlik_youtubelink=etkinlik_youtubelink, is_active=True)

    etkinlik_instance.etkinlik_tags.set(etkinlik_tags_list)

    # Assuming the function generate_unique_imagename is available and working
    # etkinlik_instance.etkinlik_picture = 'your_generated_image_field_value'

    etkinlik_instance.save()
    print(f"EtkinlikModel '{etkinlik_name}' created successfully.")
