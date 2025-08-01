from django.urls import path
from . import views

app_name = "yonetim"

urlpatterns = [
    # Ana sayfa
    path("", views.ana_sayfa, name="ana_sayfa"),
    # Şube işlemleri
    path("subeler/", views.subeler_listesi, name="subeler_listesi"),
    path("subeler/ekle/", views.sube_ekle, name="sube_ekle"),
    path("subeler/<int:pk>/duzenle/", views.sube_duzenle, name="sube_duzenle"),
    path("subeler/<int:pk>/sil/", views.sube_sil, name="sube_sil"),
    # Personel işlemleri
    path("personel/", views.personel_listesi, name="personel_listesi"),
    path("personel/ekle/", views.personel_ekle, name="personel_ekle"),
    path("personel/<int:pk>/duzenle/", views.personel_duzenle, name="personel_duzenle"),
    path("personel/<int:pk>/sil/", views.personel_sil, name="personel_sil"),
    path(
        "personel/print/", views.print_personel_listesi, name="print_personel_listesi"
    ),
    path(
        "personel/export/excel/",
        views.export_personel_excel,
        name="export_personel_excel",
    ),
    # Mesai işlemleri
    path("mesai/", views.mesai_listesi, name="mesai_listesi"),
    path("mesai/ekle/", views.mesai_ekle, name="mesai_ekle"),
    path("mesai/<int:pk>/duzenle/", views.mesai_duzenle, name="mesai_duzenle"),
    path("mesai/<int:pk>/sil/", views.mesai_sil, name="mesai_sil"),
    path("mesai/print/", views.print_mesai_listesi, name="print_mesai_listesi"),
    path("mesai/export/excel/", views.export_mesai_excel, name="export_mesai_excel"),
    # Gelir/Gider işlemleri
    path("gelir-gider/", views.gelir_gider_listesi, name="gelir_gider_listesi"),
    path("gelir-gider/ekle/", views.gelir_gider_ekle, name="gelir_gider_ekle"),
    path(
        "gelir-gider/<int:pk>/duzenle/",
        views.gelir_gider_duzenle,
        name="gelir_gider_duzenle",
    ),
    path("gelir-gider/<int:pk>/sil/", views.gelir_gider_sil, name="gelir_gider_sil"),
    path(
        "gelir-gider/print/",
        views.print_gelir_gider_listesi,
        name="print_gelir_gider_listesi",
    ),
    path(
        "gelir-gider/export/excel/",
        views.export_gelir_gider_excel,
        name="export_gelir_gider_excel",
    ),
    # API Endpoint'leri
    path(
        "api/personel-by-sube/", views.api_personel_by_sube, name="api_personel_by_sube"
    ),
]
