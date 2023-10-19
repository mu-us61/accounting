from django.contrib.auth.models import AbstractUser, Group
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.db import models
from django.utils import timezone
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _
from django.db.models import Sum


class Currency(models.Model):
    name = models.CharField(max_length=255, unique=True)
    abbreviation = models.CharField(max_length=10, unique=True)

    def __str__(self):
        return self.name


class MuGroup(Group):
    creation_date = models.DateTimeField(auto_now_add=True)


class MuUser(AbstractUser):
    username_validator = UnicodeUsernameValidator()

    username = models.CharField(_("Kullanıcı Adı"), max_length=150, unique=True, help_text=_("Max 150 karakter olabilir. Harfler, sayilar ve sadece @/./+/-/_ olabilir"), validators=[username_validator], error_messages={"unique": _("Bu isimde bir kullanici zaten var")})
    first_name = models.CharField(_("İsim"), max_length=150, blank=True)
    last_name = models.CharField(_("Soyisim"), max_length=150, blank=True)
    email = models.EmailField(_("email address"), blank=True)
    is_staff = models.BooleanField(_("Yönetici Durumu"), default=False, help_text=_("Kullanıcının bu yönetici paneline giriş yapabilmesini belirler."))
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


class Tag(models.Model):
    name = models.CharField(max_length=255, unique=True)
    slug = models.SlugField(unique=True, blank=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


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

    def __str__(self):
        return self.islem_ismi


class EvrakModel(models.Model):
    evrak_date = models.DateTimeField(auto_now_add=True)
    evrak_owner = models.ForeignKey(MuUser, on_delete=models.PROTECT)
    evrak_tags = models.ManyToManyField(Tag, blank=True)
    evrak_name = models.CharField(max_length=250)
    evrak_description = models.TextField()
    # evrak_status= GELEN VEYA GIDEN EVRAK OLCAK
    evrak_picture = models.ImageField(upload_to="images/")
    evrak_pdf = models.FileField(upload_to="pdfs/")


class EtkinlikModel:
    etkinlik_date = models.DateTimeField(auto_now_add=True)
    etkinlik_name = models.CharField(max_length=250)
    etkinlik_description = models.TextField()
    etkinlik_tags = models.ManyToManyField(Tag, blank=True)
    # etkinlik_youtubelink =
    # etkinlik_picture
