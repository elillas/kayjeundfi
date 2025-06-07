FROM python:3.11-slim

# Installer les bibliothèques système nécessaires à Pillow + mysqlclient
RUN apt-get update && apt-get install -y \
    gcc \
    build-essential \
    libjpeg-dev \
    zlib1g-dev \
    libpng-dev \
    default-libmysqlclient-dev \
    pkg-config \
    && apt-get clean

# Créer le dossier de travail
WORKDIR /app

# Copier les fichiers de l'app
COPY . .

# Installer les dépendances Python
RUN pip install --upgrade pip && pip install -r requirements.txt

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
