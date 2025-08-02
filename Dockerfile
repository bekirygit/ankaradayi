# Resmi Python çalışma zamanını ana imaj olarak kullan
FROM python:3.13-slim-bookworm

# Ortam değişkenlerini ayarla
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Çalışma dizinini ayarla
WORKDIR /app

# Bağımlılıkları yükle
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Proje kodunu kopyala
COPY . /app/

# Statik dosyaları topla
RUN python manage.py collectstatic --noinput

# Gunicorn'ı çalıştır
CMD python manage.py migrate && python manage.py create_initial_superuser && gunicorn --bind 0.0.0.0:$PORT sube_yonetim.wsgi:application