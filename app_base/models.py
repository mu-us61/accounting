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
from embed_video.fields import EmbedVideoField
from django.contrib.auth.models import BaseUserManager


class AllObjectsManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset()

    def get_deleted(self):
        return self.get_queryset().filter(is_active=False)


class ActiveObjectsManager(BaseUserManager):
    def get_queryset(self):
        return super().get_queryset().filter(is_active=True)

    def get_by_natural_key(self, username):
        return self.get(username=username)

    def create_user(self, username, password=None, **extra_fields):
        if not username:
            raise ValueError("The Username field must be set")
        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        return self.create_user(username, password, **extra_fields)


class BaseModelSoftDelete(models.Model):
    is_active = models.BooleanField(_("active"), default=True)
    objects = ActiveObjectsManager()  # Active objects manager
    all_objects = AllObjectsManager()  # Custom manager including soft-deleted items

    def delete(self, using=None, keep_parents=False):
        self.is_active = False
        self.save_fordelete()

    class Meta:
        abstract = True


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


class Currency(BaseModelSoftDelete):
    name = models.CharField(max_length=255, unique=True)
    abbreviation = models.CharField(max_length=10, unique=True)
    is_active = models.BooleanField(_("active"), default=True)
    objects = ActiveObjectsManager()

    def __str__(self):
        return self.name

    @property
    def balance_with_abbreviation(self):
        return f"{self.calculate_balance()} {self.abbreviation}"

    def save(self, *args, **kwargs):
        # self.is_active = True
        super().save(*args, **kwargs)

    def save_fordelete(self, *args, **kwargs):
        super().save(*args, **kwargs)


class MuGroup(Group, BaseModelSoftDelete):

    creation_date = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(_("active"), default=True)
    objects = ActiveObjectsManager()

    can_read_can_kullanicilar = models.BooleanField(default=False)
    can_read_kullanici_gruplari = models.BooleanField(default=False)
    can_read_excel_kullanici_yukleme = models.BooleanField(default=False)
    can_read_excel_kullanicilari = models.BooleanField(default=False)
    can_read_bakiye = models.BooleanField(default=False)
    can_read_harcama_kalemi = models.BooleanField(default=False)
    can_read_para_birimleri = models.BooleanField(default=False)
    can_read_Islemler = models.BooleanField(default=False)
    can_read_etkinlikler = models.BooleanField(default=False)
    can_read_evraklar = models.BooleanField(default=False)
    can_read_aylikharcamalar = models.BooleanField(default=False)
    can_read_aylikispatliharcamalar = models.BooleanField(default=False)
    can_read_smsyonetimi = models.BooleanField(default=False)
    can_read_mobileapplinkleri = models.BooleanField(default=False)

    can_write_can_kullanicilar = models.BooleanField(default=False)
    can_write_kullanici_gruplari = models.BooleanField(default=False)
    can_write_excel_kullanici_yukleme = models.BooleanField(default=False)
    can_write_excel_kullanicilari = models.BooleanField(default=False)
    can_write_bakiye = models.BooleanField(default=False)
    can_write_harcama_kalemi = models.BooleanField(default=False)
    can_write_para_birimleri = models.BooleanField(default=False)
    can_write_Islemler = models.BooleanField(default=False)
    can_write_etkinlikler = models.BooleanField(default=False)
    can_write_evraklar = models.BooleanField(default=False)
    can_write_aylikharcamalar = models.BooleanField(default=False)
    can_write_aylikispatliharcamalar = models.BooleanField(default=False)
    can_write_smsyonetimi = models.BooleanField(default=False)
    can_write_mobileapplinkleri = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        # self.is_active = True
        super().save(*args, **kwargs)

    def save_fordelete(self, *args, **kwargs):
        super().save(*args, **kwargs)


class MuUser(AbstractUser, BaseModelSoftDelete):
    username_validator = UnicodeUsernameValidator()
    username = models.CharField(_("Kullanıcı Adı"), max_length=150, unique=True, help_text=_("Max 150 karakter olabilir. Harfler, sayilar ve sadece @/./+/-/_ olabilir"), validators=[username_validator], error_messages={"unique": _("Bu isimde bir kullanici zaten var")})
    password = models.CharField(_("password"), max_length=128, null=False)
    first_name = models.CharField(_("İsim"), max_length=150, blank=True)  # AD-SOYAD ORTAK
    # last_name = models.CharField(_("Soyisim"), max_length=150, blank=True)  # first_name ad-soyad icin ortak kullanilcak
    email = models.EmailField(_("email address"), blank=True)
    is_staff = models.BooleanField(_("Yönetici Durumu"), default=False, help_text=_("Kullanıcının bu yönetici paneline giriş yapabilmesini belirler."))
    # is_uye = (models.BooleanField(default=False),)
    is_active = models.BooleanField(_("active"), default=True, help_text=_("Designates whether this user should be treated as active. " "Unselect this instead of deleting accounts."))
    objects = ActiveObjectsManager()
    date_joined = models.DateTimeField(_("date joined"), default=timezone.now)
    currency = models.ForeignKey(Currency, on_delete=models.PROTECT, null=True, blank=True)
    gruplar = models.ManyToManyField(MuGroup, blank=True)

    def calculate_currency_balance(self, currency):
        # Calculate the balance for the specified currency
        received = Islemler.objects.filter(kime_gitti=self, currency=currency).aggregate(sum=Sum("miktar"))["sum"] or 0
        sent = Islemler.objects.filter(kimden_geldi=self, currency=currency).aggregate(sum=Sum("miktar"))["sum"] or 0

        return received - sent

    def save(self, *args, **kwargs):
        # self.is_active = True
        super().save(*args, **kwargs)

    def save_fordelete(self, *args, **kwargs):
        super().save(*args, **kwargs)


class Tag(BaseModelSoftDelete):
    name = models.CharField(max_length=255, unique=True)
    slug = models.SlugField(unique=True, blank=True)
    is_active = models.BooleanField(_("active"), default=True)
    objects = ActiveObjectsManager()

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        # self.is_active = True
        super().save(*args, **kwargs)

    def save_fordelete(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class ExelUsers(BaseModelSoftDelete):
    name = models.CharField(max_length=250)
    # surname = models.CharField(max_length=250)
    phonenumber = PhoneNumberField(blank=True, null=True)
    date = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(_("active"), default=True)
    objects = ActiveObjectsManager()

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        # self.is_active = True
        super().save(*args, **kwargs)

    def save_fordelete(self, *args, **kwargs):
        super().save(*args, **kwargs)


ISLEMLER_TYPE_CHOICES = [
    ("gelen", "Gelen"),
    ("giden", "Giden"),
    ("vakifici", "Vakifici"),
]


class Islemler(BaseModelSoftDelete):
    islem_tarihi = models.DateTimeField(auto_now_add=True)
    # belge =
    islemsahibi = models.ForeignKey(MuUser, on_delete=models.PROTECT)
    kimden_geldi = models.ForeignKey(MuUser, related_name="gelen_paralar", on_delete=models.PROTECT, null=True, blank=True)
    kime_gitti = models.ForeignKey(MuUser, related_name="giden_paralar", on_delete=models.PROTECT, null=True, blank=True)
    islemler_type = models.CharField(max_length=10, choices=ISLEMLER_TYPE_CHOICES, null=True, blank=True)
    exelusers = models.ManyToManyField(ExelUsers, blank=True)
    tags = models.ManyToManyField(Tag, blank=True)
    islem_ismi = models.CharField(max_length=250)
    islem_aciklamasi = models.TextField()
    currency = models.ForeignKey(Currency, on_delete=models.PROTECT)
    # miktar = models.IntegerField(default=0)
    miktar = models.DecimalField(max_digits=18, decimal_places=4, default=0)
    islemler_picture = models.ImageField(upload_to=generate_unique_imagename, blank=True, null=True)
    islemler_pdf = models.FileField(upload_to=generate_unique_filename, blank=True, null=True)
    is_active = models.BooleanField(_("active"), default=True)
    objects = ActiveObjectsManager()

    def __str__(self):
        return self.islem_ismi

    def save(self, *args, **kwargs):
        # self.is_active = True
        super().save(*args, **kwargs)

    def save_fordelete(self, *args, **kwargs):
        super().save(*args, **kwargs)


EVRAK_TYPE_CHOICES = [
    ("gelen", "Gelen"),
    ("giden", "Giden"),
]


class EvrakModel(BaseModelSoftDelete):
    evrak_takipno = models.CharField(max_length=250, blank=True, null=True)
    evrak_date = models.DateTimeField(auto_now_add=True)
    evrak_last_updated = models.DateTimeField(auto_now=True)
    evrak_owner = models.ForeignKey(MuUser, on_delete=models.PROTECT)
    evrak_tags = models.ManyToManyField(Tag, blank=True)
    evrak_name = models.CharField(max_length=250)
    evrak_description = models.TextField()
    evrak_type = models.CharField(max_length=7, choices=EVRAK_TYPE_CHOICES, default="gelen")
    evrak_picture = models.ImageField(upload_to=generate_unique_imagename, blank=True, null=True)
    evrak_pdf = models.FileField(upload_to=generate_unique_filename, blank=True, null=True)
    is_active = models.BooleanField(_("active"), default=True)
    objects = ActiveObjectsManager()

    def __str__(self):
        return self.evrak_name

    def save(self, *args, **kwargs):
        # self.is_active = True
        super().save(*args, **kwargs)

    def save_fordelete(self, *args, **kwargs):
        super().save(*args, **kwargs)


class EtkinlikModel(BaseModelSoftDelete):
    etkinlik_date = models.DateTimeField(auto_now_add=True)
    etkinlik_last_updated = models.DateTimeField(auto_now=True)  # Auto-updated on every save
    etkinlik_owner = models.ForeignKey(MuUser, on_delete=models.PROTECT)
    etkinlik_name = models.CharField(max_length=250)
    etkinlik_description = models.TextField()
    etkinlik_tags = models.ManyToManyField(Tag, blank=True)
    etkinlik_youtubelink = EmbedVideoField(max_length=200, blank=True, null=True)
    etkinlik_picture = models.ImageField(upload_to=generate_unique_imagename, blank=True, null=True)
    is_active = models.BooleanField(_("active"), default=True)
    objects = ActiveObjectsManager()

    def __str__(self):
        return self.etkinlik_name

    def save(self, *args, **kwargs):
        # self.is_active = True
        super().save(*args, **kwargs)

    def save_fordelete(self, *args, **kwargs):
        super().save(*args, **kwargs)


class DummyModel(models.Model):
    pass


class MobileFile(models.Model):
    file = models.FileField(upload_to="mobile_files/")

    def __str__(self):
        return self.file.name
