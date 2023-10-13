# filters.py
import django_filters
from .models import Islemler, MuUser, Tag, Currency


class IslemlerFilter(django_filters.FilterSet):
    miktar = django_filters.NumberFilter()
    islem_tarihi = django_filters.DateFromToRangeFilter(field_name="islem_tarihi")
    kimden_geldi = django_filters.ModelChoiceFilter(queryset=MuUser.objects.all())
    kime_gitti = django_filters.ModelChoiceFilter(queryset=MuUser.objects.all())
    tags = django_filters.ModelMultipleChoiceFilter(queryset=Tag.objects.all())
    islem_ismi = django_filters.CharFilter(lookup_expr="icontains")
    islemsahibi = django_filters.ModelChoiceFilter(queryset=MuUser.objects.all())
    currency = django_filters.ModelChoiceFilter(queryset=Currency.objects.all())

    class Meta:
        model = Islemler
        fields = ["miktar", "islem_tarihi", "kimden_geldi", "kime_gitti", "tags", "islem_ismi", "islemsahibi", "currency"]


# class IslemlerFilter(django_filters.FilterSet):
#     miktar = django_filters.NumberFilter()


#     class Meta:
#         model = Islemler
#         fields = ["miktar"]

# islem_tarihi = models.DateTimeField(auto_now_add=True)
# # belge =
# islemsahibi = models.ForeignKey(MuUser, on_delete=models.PROTECT)
# kimden_geldi = models.ForeignKey(MuUser, related_name="gelen_paralar", on_delete=models.PROTECT, null=True, blank=True)
# kime_gitti = models.ForeignKey(MuUser, related_name="giden_paralar", on_delete=models.PROTECT, null=True, blank=True)
# tags = models.ManyToManyField(Tag, blank=True)
# islem_ismi = models.CharField(max_length=250)
# islem_aciklamasi = models.TextField()
# currency = models.ForeignKey(Currency, on_delete=models.PROTECT)
# miktar = models.IntegerField(default=0)

# username = django_filters.CharFilter(lookup_expr="icontains")
