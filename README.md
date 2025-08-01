# Şube Yönetim Sistemi

Bu proje, şubelerin, personelin ve gelir/gider kayıtlarının yönetimini sağlayan modern bir Django web uygulamasıdır.

## Özellikler

### 🏢 Şube Yönetimi
- Şube ekleme, düzenleme ve silme
- Şube türü seçimi (Cafe/Otel)
- Şube bazında personel ve gelir/gider takibi
- Detaylı şube bilgileri (adres, telefon, yönetici)

### 👥 Personel Yönetimi
- Personel ekleme, düzenleme ve silme
- Şube bazında personel atama
- Personel bilgileri (ad, soyad, pozisyon, iletişim)
- İşe başlama tarihi takibi
- Toplam mesai saati görüntüleme

### ⏰ Mesai Yönetimi
- Mesai kayıtları ekleme, düzenleme ve silme
- Personel bazında mesai takibi
- Tarih bazında filtreleme ve arama
- Toplam mesai saati hesaplama

### 💰 Gelir/Gider Yönetimi
- Gelir ve gider kayıtları
- Kategori bazında sınıflandırma
- Şube bazında gelir/gider takibi
- Tarih bazında filtreleme

### 📊 Özet ve İstatistikler
- Genel sistem özeti
- **Cafe ve Otel türleri için ayrı istatistikler**
- Şube bazında detaylı raporlar
- Gelir/gider karşılaştırmaları

## Teknolojiler

- **Backend**: Django 5.2.4
- **Veritabanı**: SQLite (geliştirme)
- **Frontend**: HTML, Tailwind CSS
- **Dil**: Python 3.13

## Kurulum

### Gereksinimler
- Python 3.8+
- pip

### Adımlar

1. **Projeyi klonlayın**
```bash
git clone <repository-url>
cd sube-yonetim
```

2. **Sanal ortam oluşturun ve aktifleştirin**
```bash
python -m venv venv
venv\Scripts\activate  # Windows
# veya
source venv/bin/activate  # Linux/Mac
```

3. **Bağımlılıkları yükleyin**
```bash
pip install -r requirements.txt
```

4. **Veritabanını oluşturun**
```bash
python manage.py migrate
```

5. **Admin kullanıcısı oluşturun**
```bash
python manage.py createsuperuser
```

6. **Sunucuyu başlatın**
```bash
python manage.py runserver
```

7. **Tarayıcıda açın**
```
http://127.0.0.1:8000/
```

## Kullanım

### Ana Sayfa (Özet)
- Sistem genel istatistikleri
- **Cafe ve Otel türleri için ayrı özet kartları**
- Hızlı işlem linkleri

### Şube Yönetimi
- `/subeler/` - Şube listesi
- `/subeler/ekle/` - Yeni şube ekleme
- Şube türü seçimi (Cafe/Otel)
- Şube düzenleme ve silme

### Personel Yönetimi
- `/personel/` - Personel listesi
- `/personel/ekle/` - Yeni personel ekleme
- Şube bazında personel atama
- Personel düzenleme ve silme

### Mesai Yönetimi
- `/mesai/` - Mesai listesi
- `/mesai/ekle/` - Yeni mesai ekleme
- Personel bazında mesai takibi
- Mesai düzenleme ve silme

### Gelir/Gider Yönetimi
- `/gelir-gider/` - Gelir/Gider listesi
- `/gelir-gider/ekle/` - Yeni kayıt ekleme
- Kategori ve tip bazında filtreleme
- Kayıt düzenleme ve silme

### Admin Paneli
- `/admin/` - Django admin paneli
- Tüm verilerin yönetimi
- Gelişmiş filtreleme ve arama

## Proje Yapısı

```
sube_yonetim/
├── manage.py
├── requirements.txt
├── README.md
├── sube_yonetim/          # Ana proje ayarları
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── yonetim/              # Ana uygulama
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── forms.py
│   ├── models.py
│   ├── urls.py
│   └── views.py
├── templates/            # HTML şablonları
│   ├── base.html
│   └── yonetim/
│       ├── ana_sayfa.html
│       ├── subeler_listesi.html
│       ├── sube_form.html
│       ├── sube_sil.html
│       ├── personel_listesi.html
│       ├── personel_form.html
│       ├── personel_sil.html
│       ├── gelir_gider_listesi.html
│       ├── gelir_gider_form.html
│       └── gelir_gider_sil.html
└── venv/                # Sanal ortam
```

## Veritabanı Modelleri

### Sube (Şube)
- `ad`: Şube adı
- `tur`: Şube türü (Cafe/Otel)
- `adres`: Şube adresi
- `telefon`: İletişim telefonu
- `yonetici`: Şube yöneticisi
- `olusturma_tarihi`: Oluşturulma tarihi
- `guncelleme_tarihi`: Son güncelleme tarihi

### Personel
- `sube`: Bağlı olduğu şube (ForeignKey)
- `ad`: Personel adı
- `soyad`: Personel soyadı
- `pozisyon`: İş pozisyonu
- `ise_baslama_tarihi`: İşe başlama tarihi
- `telefon`: İletişim telefonu
- `email`: E-posta adresi

### Mesai
- `personel`: Bağlı olduğu personel (ForeignKey)
- `tarih`: Mesai tarihi
- `saat`: Mesai saati (ondalık)
- `aciklama`: Mesai açıklaması (opsiyonel)

### GelirGider
- `sube`: Bağlı olduğu şube (ForeignKey)
- `tip`: Gelir veya Gider
- `kategori`: Gelir/Gider kategorisi
- `aciklama`: Detaylı açıklama
- `tutar`: Tutar
- `tarih`: İşlem tarihi

## URL Yapısı

```
/                           # Ana sayfa (Özet)
/subeler/                   # Şube listesi
/subeler/ekle/              # Yeni şube ekleme
/subeler/<id>/duzenle/      # Şube düzenleme
/subeler/<id>/sil/          # Şube silme
/personel/                  # Personel listesi
/personel/ekle/             # Yeni personel ekleme
/personel/<id>/duzenle/     # Personel düzenleme
/personel/<id>/sil/         # Personel silme
/mesai/                     # Mesai listesi
/mesai/ekle/                # Yeni mesai ekleme
/mesai/<id>/duzenle/        # Mesai düzenleme
/mesai/<id>/sil/            # Mesai silme
/gelir-gider/               # Gelir/Gider listesi
/gelir-gider/ekle/          # Yeni kayıt ekleme
/gelir-gider/<id>/duzenle/  # Kayıt düzenleme
/gelir-gider/<id>/sil/      # Kayıt silme
/admin/                     # Django admin paneli
```

## API Endpoints

```
/api/subeler/               # Şube listesi (JSON)
/api/personel/              # Personel listesi (JSON)
/api/mesai/                 # Mesai listesi (JSON)
/api/gelir-gider/           # Gelir/Gider listesi (JSON)
```

## Özelleştirme

### Yeni Şube Türü Ekleme
`yonetim/models.py` dosyasında `TUR_SECENEKLERI` listesine yeni seçenekler ekleyebilirsiniz:

```python
TUR_SECENEKLERI = [
    ('cafe', 'Cafe'),
    ('otel', 'Otel'),
    ('restoran', 'Restoran'),  # Yeni tür
    ('market', 'Market'),      # Yeni tür
]
```

### Yeni Gelir/Gider Kategorileri
Gelir/Gider kategorileri serbest metin olarak girilir, ancak önceden tanımlı kategoriler için form widget'ı özelleştirilebilir.

## Geliştirme

### Yeni Özellik Ekleme
1. Model değişikliklerini `models.py`'de yapın
2. `python manage.py makemigrations` ile migration oluşturun
3. `python manage.py migrate` ile veritabanını güncelleyin
4. Gerekli view'ları `views.py`'de ekleyin
5. URL'leri `urls.py`'de tanımlayın
6. Template'leri `templates/` klasöründe oluşturun

### Test Etme
```bash
python manage.py test
```

## Lisans

Bu proje MIT lisansı altında lisanslanmıştır.

## İletişim

Sorularınız için: bekir@bekir.com 