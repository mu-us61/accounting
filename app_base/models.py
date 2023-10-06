from django.contrib.auth.models import AbstractUser, Group
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.db import models
from django.utils import timezone
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _


class Currency(models.Model):
    name = models.CharField(max_length=255, unique=True)
    abbreviation = models.CharField(max_length=10, unique=True)

    def __str__(self):
        return self.name


class MuUser(AbstractUser):
    username_validator = UnicodeUsernameValidator()

    username = models.CharField(_("Kullanıcı Adı"), max_length=150, unique=True, help_text=_("Max 150 karakter olabilir. Harfler, sayilar ve sadece @/./+/-/_ olabilir"), validators=[username_validator], error_messages={"unique": _("Bu isimde bir kullanici zaten var")})
    first_name = models.CharField(_("İsim"), max_length=150, blank=True)
    last_name = models.CharField(_("Soyisim"), max_length=150, blank=True)
    email = models.EmailField(_("email address"), blank=True)
    is_staff = models.BooleanField(_("Yönetici Durumu"), default=False, help_text=_("Kullanıcının bu yönetici paneline giriş yapabilmesini belirler."))
    is_active = models.BooleanField(_("active"), default=True, help_text=_("Designates whether this user should be treated as active. " "Unselect this instead of deleting accounts."))
    date_joined = models.DateTimeField(_("date joined"), default=timezone.now)
    currency = models.ForeignKey(Currency, on_delete=models.SET_NULL, null=True)


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

    tags = models.ManyToManyField(Tag)

    islem_ismi = models.CharField(max_length=250)
    islem_aciklamasi = models.TextField()

    currency = models.ForeignKey(Currency, on_delete=models.CASCADE)

    # Add fields for girdiler and ciktilar
    girdiler = models.IntegerField(default=0)
    ciktilar = models.IntegerField(default=0)

    def __str__(self):
        return self.islem_ismi


class MuGroup(Group):
    creation_date = models.DateTimeField(auto_now_add=True)
