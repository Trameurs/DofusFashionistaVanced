FROM python:3.9

# Installer les dépendances système nécessaires
RUN apt-get update && apt-get install -y \
    default-libmysqlclient-dev \
    memcached \
    gettext \
    mariadb-client \
    libdbus-1-dev \
    libdbus-glib-1-dev \
    pkg-config \
    dos2unix \
    sqlite3 \
    && rm -rf /var/lib/apt/lists/*

# Définir le répertoire de travail
WORKDIR /app

# Copier les fichiers de requirements
COPY requirements.txt .

# Installer les dépendances Python
RUN pip install --no-cache-dir -r requirements.txt

# Copier le reste du code source
COPY . .

# Corriger les problèmes de fin de ligne CRLF sur tous les scripts
# La commande correcte avec parenthèses pour regrouper les expressions
RUN apt-get update && apt-get install -y dos2unix
RUN find . -name "*.py" -type f -exec dos2unix -b {} \;
RUN find . -name "*.sh" -type f -exec dos2unix -b {} \;
RUN find . -name "*.py" -type f -exec sed -i -e 's/\r$//' {} \;
RUN find . -name "*.sh" -type f -exec sed -i -e 's/\r$//' {} \;

# Correction spécifique des shebangs
RUN grep -l '^#!' $(find . -name "*.py") | xargs -r sed -i -e '1s/^#!.*python\r*$/#!\/usr\/bin\/env python/'
RUN grep -l '^#!' $(find . -name "*.sh") | xargs -r sed -i -e '1s/^#!.*sh\r*$/#!\/bin\/bash/'

# Rendre les scripts exécutables
RUN chmod +x *.py *.sh

# Créer le répertoire de configuration
RUN mkdir -p /etc/fashionista

# Créer un fichier gen_config.json de base
RUN echo '{\
    "PASSWORD_RESET_SALT": "my_salt",\
    "EMAIL_CONFIRMATION_SALT": "my_salt_2",\
    "SECRET_KEY": "django-insecure-change-me-in-production",\
    "mysql_PASSWORD": "fashionista",\
    "mysql_USER": "fashionista",\
    "EMAIL_HOST_USER": "",\
    "EMAIL_HOST_PASSWORD": "",\
    "SOCIAL_AUTH_GOOGLE_OAUTH2_KEY": null,\
    "SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET": null,\
    "SOCIAL_AUTH_FACEBOOK_KEY": null,\
    "SOCIAL_AUTH_FACEBOOK_SECRET": null,\
    "DBBACKUP_S3_ACCESS_KEY": null,\
    "DBBACKUP_S3_SECRET_KEY": null,\
    "url_captcha_secret": null,\
    "char_id_SECRET_PART_1": "my_secret",\
    "char_id_SECRET_PART_2": "my_other_secret",\
    "google_analytics_id": null,\
    "EMAIL_USE_TLS": true,\
    "EMAIL_HOST": "smtp.gmail.com",\
    "EMAIL_PORT": 587,\
    "TESTER_USERS_EMAILS": []\
}' > /etc/fashionista/gen_config.json

# Configurer le mode DEBUG par défaut
RUN echo "True" > /etc/fashionista/debug_mode

# Configurer le mode serve_static
RUN echo "True" > /etc/fashionista/serve_static

# Créer un fichier config avec le chemin du projet
RUN echo "/app" > /etc/fashionista/config

# Ajouter les répertoires au PYTHONPATH
ENV PYTHONPATH="/app:/app/fashionistapulp:/app/fashionsite"

# Exposer le port 8000
EXPOSE 8000

# Commande pour démarrer le serveur
CMD ["bash", "-c", "\
    # Convertir tous les fichiers Python et Shell en format Unix\n\
    find /app -name '*.py' -type f -exec dos2unix {} \\; && \
    find /app -name '*.sh' -type f -exec dos2unix {} \\; && \
    # Correction spécifique des shebangs\n\
    find /app -name '*.py' -type f -exec grep -l '^#!' {} \\; | xargs -r sed -i -e '1s/^#!.*python\\r*$/#!\\/usr\\/bin\\/env python/' && \
    find /app -name '*.sh' -type f -exec grep -l '^#!' {} \\; | xargs -r sed -i -e '1s/^#!.*sh\\r*$/#!\\/bin\\/bash/' && \
    # Migrations de la base de données Django\n\
    cd /app/fashionsite && python manage.py migrate && cd /app && \
    # Exécuter les commandes suivantes\n\
    python /app/wipe_solution_cache.py || echo 'Attention: wipe_solution_cache.py a échoué, mais on continue' && \
    cd fashionsite && \
    django-admin compilemessages && \
    cd .. && \
    cd /app && \
    PYTHONPATH=/app:/app/fashionsite:/app/fashionistapulp gunicorn --chdir /app/fashionsite wsgi:application --bind 0.0.0.0:8000 --timeout 150 --log-level debug \
"]
