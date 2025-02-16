# Python image'ını kullan
FROM python:3.10

# Çalışma dizinini ayarla
WORKDIR /app

# Gereksinim dosyasını kopyala ve bağımlılıkları yükle
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Proje dosyalarını kopyala
COPY . /app/

# Django uygulamasını çalıştır
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]