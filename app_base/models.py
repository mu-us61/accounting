from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from django.utils.text import slugify

# Create your models here.


class MuUser(AbstractUser):
    username_validator = UnicodeUsernameValidator()

    username = models.CharField(_("username"), max_length=150, unique=True, help_text=_("Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only."), validators=[username_validator], error_messages={"unique": _("A user with that username already exists.")})
    first_name = models.CharField(_("first name"), max_length=150, blank=True)
    last_name = models.CharField(_("last name"), max_length=150, blank=True)
    email = models.EmailField(_("email address"), blank=True)
    is_staff = models.BooleanField(_("staff status"), default=False, help_text=_("Designates whether the user can log into this admin site."))
    is_active = models.BooleanField(_("active"), default=True, help_text=_("Designates whether this user should be treated as active. " "Unselect this instead of deleting accounts."))
    date_joined = models.DateTimeField(_("date joined"), default=timezone.now)

    bakiye_TL = models.IntegerField(default=0)
    girdiler_TL = models.IntegerField(default=0)
    ciktilar_TL = models.IntegerField(default=0)
    # girdikaynagi =
    # ciktikaynagi =

    bakiye_Euro = models.IntegerField(default=0)
    girdiler_Euro = models.IntegerField(default=0)
    ciktilar_Euro = models.IntegerField(default=0)

    bakiye_Dolar = models.IntegerField(default=0)
    girdiler_Dolar = models.IntegerField(default=0)
    ciktilar_Dolar = models.IntegerField(default=0)

    bakiye_GBP = models.IntegerField(default=0)
    girdiler_GBP = models.IntegerField(default=0)
    ciktilar_GBP = models.IntegerField(default=0)

    bakiye_Sek = models.IntegerField(default=0)
    girdiler_Sek = models.IntegerField(default=0)
    ciktilar_Sek = models.IntegerField(default=0)


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
    islem_tarihi = models.DateField(auto_now=True, auto_now_add=False)
    # belge =
    islemsahibi = models.ForeignKey(MuUser, on_delete=models.PROTECT)
    kimden_geldi = models.ForeignKey(MuUser, related_name="gelen_paralar", on_delete=models.PROTECT, null=True, blank=True)
    kime_gitti = models.ForeignKey(MuUser, related_name="giden_paralar", on_delete=models.PROTECT, null=True, blank=True)

    tags = models.ManyToManyField(Tag)

    islem_ismi = models.CharField(max_length=250)
    islem_aciklamasi = models.TextField()

    bakiye_TL = models.IntegerField(default=0)
    girdiler_TL = models.IntegerField(default=0)
    ciktilar_TL = models.IntegerField(default=0)

    bakiye_Euro = models.IntegerField(default=0)
    girdiler_Euro = models.IntegerField(default=0)
    ciktilar_Euro = models.IntegerField(default=0)

    bakiye_Dolar = models.IntegerField(default=0)
    girdiler_Dolar = models.IntegerField(default=0)
    ciktilar_Dolar = models.IntegerField(default=0)

    bakiye_GBP = models.IntegerField(default=0)
    girdiler_GBP = models.IntegerField(default=0)
    ciktilar_GBP = models.IntegerField(default=0)

    bakiye_Sek = models.IntegerField(default=0)
    girdiler_Sek = models.IntegerField(default=0)
    ciktilar_Sek = models.IntegerField(default=0)
