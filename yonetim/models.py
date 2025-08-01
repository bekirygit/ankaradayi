from django.db import models
from django.core.validators import MinValueValidator
from decimal import Decimal


class Sube(models.Model):
    TUR_SECENEKLERI = [
        ("cafe", "Cafe"),
        ("otel", "Otel"),
    ]

    ad = models.CharField(max_length=200, verbose_name="Şube Adı")
    tur = models.CharField(
        max_length=10, choices=TUR_SECENEKLERI, default="cafe", verbose_name="Şube Türü"
    )
    adres = models.TextField(verbose_name="Adres")
    telefon = models.CharField(max_length=20, verbose_name="Telefon")
    yonetici = models.CharField(max_length=100, verbose_name="Yönetici")
    olusturma_tarihi = models.DateTimeField(
        auto_now_add=True, verbose_name="Oluşturma Tarihi"
    )
    guncelleme_tarihi = models.DateTimeField(
        auto_now=True, verbose_name="Güncelleme Tarihi"
    )

    class Meta:
        verbose_name = "Şube"
        verbose_name_plural = "Şubeler"
        ordering = ["ad"]

    def __str__(self):
        return self.ad

    def toplam_gelir(self):
        return self.gelirgider_set.filter(tip="gelir").aggregate(
            toplam=models.Sum("tutar")
        )["toplam"] or Decimal("0.00")

    def toplam_gider(self):
        return self.gelirgider_set.filter(tip="gider").aggregate(
            toplam=models.Sum("tutar")
        )["toplam"] or Decimal("0.00")

    def net_kar(self):
        return self.toplam_gelir() - self.toplam_gider()

    def personel_sayisi(self):
        return self.personel_set.count()

    


class Personel(models.Model):
    sube = models.ForeignKey(Sube, on_delete=models.CASCADE, verbose_name="Şube")
    ad = models.CharField(max_length=100, verbose_name="Ad")
    soyad = models.CharField(max_length=100, verbose_name="Soyad")
    pozisyon = models.CharField(max_length=100, verbose_name="Pozisyon")
    ise_baslama_tarihi = models.DateField(verbose_name="İşe Başlama Tarihi")
    telefon = models.CharField(max_length=20, verbose_name="Telefon")
    email = models.EmailField(verbose_name="E-posta", blank=True, null=True)
    olusturma_tarihi = models.DateTimeField(
        auto_now_add=True, verbose_name="Oluşturma Tarihi"
    )
    guncelleme_tarihi = models.DateTimeField(
        auto_now=True, verbose_name="Güncelleme Tarihi"
    )

    class Meta:
        verbose_name = "Personel"
        verbose_name_plural = "Personeller"
        ordering = ["ad", "soyad"]

    def __str__(self):
        return f"{self.ad} {self.soyad} - {self.pozisyon}"

    @property
    def tam_ad(self):
        return f"{self.ad} {self.soyad}"

    def toplam_mesai_saati(self):
        return self.mesai_set.aggregate(toplam=models.Sum("saat"))["toplam"] or 0


class Mesai(models.Model):
    personel = models.ForeignKey(
        Personel, on_delete=models.CASCADE, verbose_name="Personel"
    )
    tarih = models.DateField(verbose_name="Tarih")
    saat = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        validators=[MinValueValidator(Decimal("0.00"))],
        verbose_name="Mesai Saati",
    )
    aciklama = models.TextField(blank=True, verbose_name="Açıklama")
    olusturma_tarihi = models.DateTimeField(
        auto_now_add=True, verbose_name="Oluşturma Tarihi"
    )
    guncelleme_tarihi = models.DateTimeField(
        auto_now=True, verbose_name="Güncelleme Tarihi"
    )

    class Meta:
        verbose_name = "Mesai"
        verbose_name_plural = "Mesailer"
        ordering = ["-tarih", "-olusturma_tarihi"]

    def __str__(self):
        return f"{self.personel.tam_ad} - {self.tarih} - {self.saat} saat"


class GelirGider(models.Model):
    TIP_SECENEKLERI = [
        ("gelir", "Gelir"),
        ("gider", "Gider"),
    ]

    KATEGORI_SECENEKLERI = [
        ("nakit", "NAKİT"),
        # Gelecekte buraya yeni seçenekler eklenebilir
    ]

    sube = models.ForeignKey(Sube, on_delete=models.CASCADE, verbose_name="Şube")
    tip = models.CharField(max_length=10, choices=TIP_SECENEKLERI, verbose_name="Tip")
    kategori = models.CharField(
        max_length=100,
        choices=KATEGORI_SECENEKLERI,
        default="nakit",
        verbose_name="Kategori",
    )
    aciklama = models.TextField(verbose_name="Açıklama", blank=True)
    tutar = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        validators=[MinValueValidator(Decimal("0.01"))],
        verbose_name="Tutar",
    )
    tarih = models.DateField(verbose_name="Tarih")
    olusturma_tarihi = models.DateTimeField(
        auto_now_add=True, verbose_name="Oluşturma Tarihi"
    )
    guncelleme_tarihi = models.DateTimeField(
        auto_now=True, verbose_name="Güncelleme Tarihi"
    )

    class Meta:
        verbose_name = "Gelir/Gider"
        verbose_name_plural = "Gelir/Giderler"
        ordering = ["-tarih", "-olusturma_tarihi"]

    def __str__(self):
        return f"{self.sube.ad} - {self.get_tip_display()} - {self.kategori} - {self.tutar}₺"
