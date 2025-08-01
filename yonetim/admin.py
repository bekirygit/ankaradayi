from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User, Group
from django.utils.html import format_html
from .models import Sube, Personel, GelirGider, Mesai


# UserAdmin'i Django'nun varsayılanını kullanacak şekilde genişletiyoruz.
# Bu, gruplar ve izinler yönetimini otomatik olarak ekler.
class UserAdmin(BaseUserAdmin):
    list_display = (
        "username",
        "email",
        "first_name",
        "last_name",
        "is_staff",
        "get_groups",
    )
    list_filter = ("is_staff", "is_superuser", "is_active", "groups")
    search_fields = ("username", "first_name", "last_name", "email")
    ordering = ("username",)
    filter_horizontal = (
        "groups",
        "user_permissions",
    )

    def get_groups(self, obj):
        return ", ".join([g.name for g in obj.groups.all()])

    get_groups.short_description = "Roller (Gruplar)"


# Mevcut User admin kaydını kaldırıp yenisini ekliyoruz
admin.site.unregister(User)
admin.site.register(User, UserAdmin)

# Group admin'in varsayılan olarak görünmesini sağlıyoruz
# Eğer zaten kayıtlıysa hata vermemesi için kontrol edebiliriz, ama genelde değildir.
try:
    admin.site.unregister(Group)
except admin.sites.NotRegistered:
    pass
admin.site.register(Group)


@admin.register(Sube)
class SubeAdmin(admin.ModelAdmin):
    list_display = [
        "ad",
        "tur",
        "yonetici",
        "telefon",
        "personel_sayisi_display",
        "toplam_gelir_display",
        "toplam_gider_display",
        "net_kar_display",
    ]
    list_filter = ["tur", "olusturma_tarihi"]
    search_fields = ["ad", "yonetici", "adres"]
    readonly_fields = ["olusturma_tarihi", "guncelleme_tarihi"]

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.annotate(
            _personel_sayisi=Count("personel", distinct=True),
            _toplam_gelir=Sum(
                Case(
                    When(gelirgider__tip="gelir", then="gelirgider__tutar"),
                    default=Value(0),
                    output_field=DecimalField(),
                )
            ),
            _toplam_gider=Sum(
                Case(
                    When(gelirgider__tip="gider", then="gelirgider__tutar"),
                    default=Value(0),
                    output_field=DecimalField(),
                )
            ),
        )

    def personel_sayisi_display(self, obj):
        return obj._personel_sayisi

    personel_sayisi_display.short_description = "Personel Sayısı"
    personel_sayisi_display.admin_order_field = "_personel_sayisi"

    def toplam_gelir_display(self, obj):
        return f"{obj._toplam_gelir:,.2f} ₺"

    toplam_gelir_display.short_description = "Toplam Gelir"
    toplam_gelir_display.admin_order_field = "_toplam_gelir"

    def toplam_gider_display(self, obj):
        return f"{obj._toplam_gider:,.2f} ₺"

    toplam_gider_display.short_description = "Toplam Gider"
    toplam_gider_display.admin_order_field = "_toplam_gider"

    def net_kar_display(self, obj):
        net = obj._toplam_gelir - obj._toplam_gider
        color = "green" if net >= 0 else "red"
        return format_html('<span style="color: {};">{:.2f} ₺</span>', color, net)

    net_kar_display.short_description = "Net Kar/Zarar"
    net_kar_display.admin_order_field = "_toplam_gelir" # Can't order by calculated field directly, use one of its components


@admin.register(Personel)
class PersonelAdmin(admin.ModelAdmin):
    list_display = [
        "tam_ad",
        "sube",
        "pozisyon",
        "toplam_mesai_display",
        "ise_baslama_tarihi",
        "telefon",
    ]
    list_filter = ["sube", "pozisyon", "ise_baslama_tarihi"]
    search_fields = ["ad", "soyad", "pozisyon", "email"]
    readonly_fields = ["olusturma_tarihi", "guncelleme_tarihi"]

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.annotate(
            _toplam_mesai=Sum("mesai__saat")
        )

    def toplam_mesai_display(self, obj):
        return f"{obj._toplam_mesai or 0} saat"

    toplam_mesai_display.short_description = "Toplam Mesai"
    toplam_mesai_display.admin_order_field = "_toplam_mesai"


@admin.register(Mesai)
class MesaiAdmin(admin.ModelAdmin):
    list_display = ["personel", "tarih", "saat", "aciklama_kisa"]
    list_filter = ["tarih", "personel__sube", "personel"]
    search_fields = ["personel__ad", "personel__soyad", "aciklama"]
    readonly_fields = ["olusturma_tarihi", "guncelleme_tarihi"]
    date_hierarchy = "tarih"

    def aciklama_kisa(self, obj):
        return obj.aciklama[:50] + "..." if len(obj.aciklama) > 50 else obj.aciklama

    aciklama_kisa.short_description = "Açıklama"


@admin.register(GelirGider)
class GelirGiderAdmin(admin.ModelAdmin):
    list_display = ["sube", "tip", "kategori", "tutar", "tarih", "aciklama_kisa"]
    list_filter = ["tip", "kategori", "tarih", "sube"]
    search_fields = ["kategori", "aciklama", "sube__ad"]
    readonly_fields = ["olusturma_tarihi", "guncelleme_tarihi"]
    date_hierarchy = "tarih"

    def aciklama_kisa(self, obj):
        return obj.aciklama[:50] + "..." if len(obj.aciklama) > 50 else obj.aciklama

    aciklama_kisa.short_description = "Açıklama"

    def tutar(self, obj):
        color = "green" if obj.tip == "gelir" else "red"
        return format_html('<span style="color: {};">{:.2f} ₺</span>', color, obj.tutar)

    tutar.short_description = "Tutar"
