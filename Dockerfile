# Kendi Python sürümünüze uygun resmi imajı seçin
FROM python:3.13-slim

# 2. Konteyner içinde çalışacak dizini belirle
WORKDIR /app

# 3. Bağımlılıklar dosyasını kopyala ve kur
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 4. Proje dosyalarını konteynere kopyala
COPY . .

# 5. Konteyner başladığında çalışacak komut
CMD ["python", "main.py"]