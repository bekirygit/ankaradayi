from django.test import TestCase, Client
from django.urls import reverse
from yonetim.models import Sube


class YonetimViewsTestCase(TestCase):
    def setUp(self):
        """Her test öncesi çalışacak başlangıç kurulumu."""
        self.client = Client()
        self.sube_data = {
            "ad": "Test Şube",
            "tur": "cafe",
            "adres": "Test Adres",
            "telefon": "1234567890",
            "yonetici": "Test Yönetici",
        }
        self.sube = Sube.objects.create(**self.sube_data)

    def test_login_page_loads_successfully(self):
        """Giriş sayfasının başarıyla yüklenip yüklenmediğini test eder."""
        # 'login' URL'ini reverse lookup ile al
        login_url = reverse("login")

        # Bu URL'e bir GET isteği gönder
        response = self.client.get(login_url)

        # 1. Sayfanın başarılı bir şekilde açıldığını doğrula (HTTP 200)
        self.assertEqual(response.status_code, 200)

        # 2. Doğru şablonun kullanıldığını doğrula
        self.assertTemplateUsed(response, "giris.html")

        # 3. Sayfa içeriğinde beklenen bir metin olup olmadığını kontrol et (opsiyonel ama önerilir)
        self.assertContains(response, "Kullanıcı Adı")
        self.assertContains(response, "Şifre")

    def test_sube_creation(self):
        """Yeni bir şube oluşturma test eder."""
        self.assertEqual(Sube.objects.count(), 1)
        new_sube = Sube.objects.create(
            ad="Yeni Şube",
            tur="otel",
            adres="Yeni Adres",
            telefon="0987654321",
            yonetici="Yeni Yönetici",
        )
        self.assertEqual(Sube.objects.count(), 2)
        self.assertEqual(new_sube.ad, "Yeni Şube")

    def test_sube_read(self):
        """Mevcut bir şubeyi okuma test eder."""
        retrieved_sube = Sube.objects.get(ad="Test Şube")
        self.assertEqual(retrieved_sube.adres, "Test Adres")

    def test_sube_update(self):
        """Mevcut bir şubeyi güncelleme test eder."""
        self.sube.adres = "Güncellenmiş Adres"
        self.sube.save()
        updated_sube = Sube.objects.get(ad="Test Şube")
        self.assertEqual(updated_sube.adres, "Güncellenmiş Adres")

    def test_sube_delete(self):
        """Mevcut bir şubeyi silme test eder."""
        self.sube.delete()
        self.assertEqual(Sube.objects.count(), 0)
        with self.assertRaises(Sube.DoesNotExist):
            Sube.objects.get(ad="Test Şube")