from django.contrib.auth.models import AbstractUser, Group
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.db import models
from django.utils import timezone
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _
from django.db.models import Sum
import os
import random
import string
from datetime import datetime
from phonenumber_field.modelfields import PhoneNumberField

# //------------------------~~--------------------------------------------------------------------------


def generate_unique_filename(instance, filename):
    # Get the file's extension (e.g., '.pdf')
    ext = filename.split(".")[-1]
    # Generate a unique filename using a timestamp
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    # Generate a random string of characters
    random_string = "".join(random.choice(string.ascii_letters) for _ in range(6))
    # Combine the timestamp, random string, and extension to create a unique filename
    unique_filename = f"{timestamp}_{random_string}.{ext}"
    # Return the path to save the file (e.g., 'pdfs/20231019123456_ABCDEF.pdf')
    return os.path.join("pdfs", unique_filename)


def generate_unique_imagename(instance, filename):
    # Get the file's extension (e.g., '.jpg')
    ext = filename.split(".")[-1]
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    # Generate a random string of characters
    random_string = "".join(random.choice(string.ascii_letters) for _ in range(6))
    # Combine the timestamp, random string, and extension to create a unique filename
    unique_filename = f"{timestamp}_{random_string}.{ext}"
    # Return the path to save the file (e.g., 'images/unique-filename.jpg')
    return os.path.join("images", unique_filename)


# //------------------------~~--------------------------------------------------------------------------
class Currency(models.Model):
    name = models.CharField(max_length=255, unique=True)
    abbreviation = models.CharField(max_length=10, unique=True)

    def __str__(self):
        return self.name


# //------------------------~~--------------------------------------------------------------------------


class MuGroup(Group):
    creation_date = models.DateTimeField(auto_now_add=True)


# //------------------------~~--------------------------------------------------------------------------
class MuUser(AbstractUser):
    username_validator = UnicodeUsernameValidator()
    username = models.CharField(_("Kullanıcı Adı"), max_length=150, unique=True, help_text=_("Max 150 karakter olabilir. Harfler, sayilar ve sadece @/./+/-/_ olabilir"), validators=[username_validator], error_messages={"unique": _("Bu isimde bir kullanici zaten var")})
    password = models.CharField(_("password"), max_length=128, null=False)
    first_name = models.CharField(_("İsim"), max_length=150, blank=True)  # AD-SOYAD ORTAK
    last_name = models.CharField(_("Soyisim"), max_length=150, blank=True)  # first_name ad-soyad icin ortak kullanilcak
    email = models.EmailField(_("email address"), blank=True)
    is_staff = models.BooleanField(_("Yönetici Durumu"), default=False, help_text=_("Kullanıcının bu yönetici paneline giriş yapabilmesini belirler."))
    # is_uye = (models.BooleanField(default=False),)
    is_active = models.BooleanField(_("active"), default=True, help_text=_("Designates whether this user should be treated as active. " "Unselect this instead of deleting accounts."))
    date_joined = models.DateTimeField(_("date joined"), default=timezone.now)
    currency = models.ForeignKey(Currency, on_delete=models.PROTECT, null=True)
    gruplar = models.ManyToManyField(MuGroup, blank=True)

    def calculate_currency_balance(self, currency):
        # Calculate the balance for the specified currency
        received = Islemler.objects.filter(kime_gitti=self, currency=currency).aggregate(sum=Sum("miktar"))["sum"] or 0
        sent = Islemler.objects.filter(kimden_geldi=self, currency=currency).aggregate(sum=Sum("miktar"))["sum"] or 0

        return received - sent

    # user = MuUser.objects.get(id=user_id)
    # currency = Currency.objects.get(id=currency_id)
    # balance = user.calculate_currency_balance(currency)  how to use


# //------------------------~~--------------------------------------------------------------------------
class Tag(models.Model):
    name = models.CharField(max_length=255, unique=True)
    slug = models.SlugField(unique=True, blank=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


# //------------------------~~--------------------------------------------------------------------------
class Islemler(models.Model):
    islem_tarihi = models.DateTimeField(auto_now_add=True)
    # belge =
    islemsahibi = models.ForeignKey(MuUser, on_delete=models.PROTECT)
    kimden_geldi = models.ForeignKey(MuUser, related_name="gelen_paralar", on_delete=models.PROTECT, null=True, blank=True)
    kime_gitti = models.ForeignKey(MuUser, related_name="giden_paralar", on_delete=models.PROTECT, null=True, blank=True)
    tags = models.ManyToManyField(Tag, blank=True)
    islem_ismi = models.CharField(max_length=250)
    islem_aciklamasi = models.TextField()
    currency = models.ForeignKey(Currency, on_delete=models.PROTECT)
    # miktar = models.IntegerField(default=0)
    miktar = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    islemler_picture = models.ImageField(upload_to=generate_unique_imagename, blank=True, null=True)
    islemler_pdf = models.FileField(upload_to=generate_unique_filename, blank=True, null=True)

    def __str__(self):
        return self.islem_ismi


# //------------------------~~--------------------------------------------------------------------------

EVRAK_TYPE_CHOICES = [
    ("gelen", "Gelen"),
    ("giden", "Giden"),
]


class EvrakModel(models.Model):
    evrak_date = models.DateTimeField(auto_now_add=True)
    evrak_last_updated = models.DateTimeField(auto_now=True)
    evrak_owner = models.ForeignKey(MuUser, on_delete=models.PROTECT)
    evrak_tags = models.ManyToManyField(Tag, blank=True)
    evrak_name = models.CharField(max_length=250)
    evrak_description = models.TextField()
    evrak_type = models.CharField(max_length=7, choices=EVRAK_TYPE_CHOICES, default="gelen")
    evrak_picture = models.ImageField(upload_to=generate_unique_imagename, blank=True, null=True)
    evrak_pdf = models.FileField(upload_to=generate_unique_filename, blank=True, null=True)

    def __str__(self):
        return self.evrak_name


# //------------------------~~--------------------------------------------------------------------------
class EtkinlikModel(models.Model):
    etkinlik_date = models.DateTimeField(auto_now_add=True)
    etkinlik_last_updated = models.DateTimeField(auto_now=True)  # Auto-updated on every save
    etkinlik_owner = models.ForeignKey(MuUser, on_delete=models.PROTECT)
    etkinlik_name = models.CharField(max_length=250)
    etkinlik_description = models.TextField()
    etkinlik_tags = models.ManyToManyField(Tag, blank=True)
    etkinlik_youtubelink = models.CharField(max_length=200, blank=True, null=True)
    etkinlik_picture = models.ImageField(upload_to=generate_unique_imagename, blank=True, null=True)

    def __str__(self):
        return self.etkinlik_name


class DummyModel(models.Model):
    pass


class ExelUsers(models.Model):
    name = models.CharField(max_length=250)
    surname = models.CharField(max_length=250)
    phonenumber = PhoneNumberField(blank=True, null=True)
    date = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)
