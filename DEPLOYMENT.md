# 🚀 Deployment Guide

## Production Deployment Checklist

### 1. Security Settings

Update `flashcard_project/settings.py`:

```python
# SECURITY WARNING: keep the secret key used in production secret!
import os
SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY', 'your-secret-key-here')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

# Update with your domain
ALLOWED_HOSTS = ['yourdomain.com', 'www.yourdomain.com']

# Security settings
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'
```

### 2. Database Configuration

#### PostgreSQL (Recommended)

Install psycopg2:
```bash
pip install psycopg2-binary
```

Update settings:
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get('DB_NAME', 'flashcard_db'),
        'USER': os.environ.get('DB_USER', 'postgres'),
        'PASSWORD': os.environ.get('DB_PASSWORD'),
        'HOST': os.environ.get('DB_HOST', 'localhost'),
        'PORT': os.environ.get('DB_PORT', '5432'),
    }
}
```

### 3. Static Files

```python
# settings.py
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATIC_URL = '/static/'

# Collect static files
python manage.py collectstatic
```

### 4. Environment Variables

Create a `.env` file:
```
DJANGO_SECRET_KEY=your-secret-key
DEBUG=False
DB_NAME=flashcard_db
DB_USER=your_db_user
DB_PASSWORD=your_db_password
DB_HOST=localhost
DB_PORT=5432
```

Install python-decouple:
```bash
pip install python-decouple
```

Use in settings.py:
```python
from decouple import config

SECRET_KEY = config('DJANGO_SECRET_KEY')
DEBUG = config('DEBUG', default=False, cast=bool)
```

### 5. Web Server Setup

#### Using Gunicorn + Nginx

Install Gunicorn:
```bash
pip install gunicorn
```

Create `gunicorn_config.py`:
```python
bind = "0.0.0.0:8000"
workers = 3
accesslog = "/var/log/gunicorn/access.log"
errorlog = "/var/log/gunicorn/error.log"
```

Run Gunicorn:
```bash
gunicorn flashcard_project.wsgi:application -c gunicorn_config.py
```

#### Nginx Configuration

Create `/etc/nginx/sites-available/flashcard`:
```nginx
server {
    listen 80;
    server_name yourdomain.com;

    location = /favicon.ico { access_log off; log_not_found off; }
    
    location /static/ {
        root /path/to/flashcard_app;
    }

    location /media/ {
        root /path/to/flashcard_app;
    }

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

Enable site:
```bash
sudo ln -s /etc/nginx/sites-available/flashcard /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

### 6. Systemd Service

Create `/etc/systemd/system/flashcard.service`:
```ini
[Unit]
Description=Flashcard Django Application
After=network.target

[Service]
User=www-data
Group=www-data
WorkingDirectory=/path/to/flashcard_app
Environment="PATH=/path/to/venv/bin"
ExecStart=/path/to/venv/bin/gunicorn flashcard_project.wsgi:application -c gunicorn_config.py

[Install]
WantedBy=multi-user.target
```

Enable and start:
```bash
sudo systemctl enable flashcard
sudo systemctl start flashcard
sudo systemctl status flashcard
```

### 7. SSL Certificate (HTTPS)

Using Let's Encrypt:
```bash
sudo apt install certbot python3-certbot-nginx
sudo certbot --nginx -d yourdomain.com -d www.yourdomain.com
```

### 8. Database Migrations

```bash
python manage.py migrate
python manage.py createsuperuser
```

## Deployment Platforms

### Heroku

1. Create `Procfile`:
```
web: gunicorn flashcard_project.wsgi
```

2. Create `runtime.txt`:
```
python-3.11.0
```

3. Update requirements.txt:
```
pip freeze > requirements.txt
```

4. Deploy:
```bash
heroku create your-app-name
git push heroku main
heroku run python manage.py migrate
heroku run python manage.py createsuperuser
```

### AWS Elastic Beanstalk

1. Install EB CLI:
```bash
pip install awsebcli
```

2. Initialize:
```bash
eb init -p python-3.11 flashcard-app
```

3. Create environment:
```bash
eb create flashcard-env
```

4. Deploy:
```bash
eb deploy
```

### DigitalOcean App Platform

1. Connect your GitHub repository
2. Select Python as the runtime
3. Set build command: `pip install -r requirements.txt`
4. Set run command: `gunicorn flashcard_project.wsgi:application`
5. Add environment variables
6. Deploy

### Docker Deployment

Create `Dockerfile`:
```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN python manage.py collectstatic --noinput

CMD ["gunicorn", "flashcard_project.wsgi:application", "--bind", "0.0.0.0:8000"]
```

Create `docker-compose.yml`:
```yaml
version: '3.8'

services:
  web:
    build: .
    command: gunicorn flashcard_project.wsgi:application --bind 0.0.0.0:8000
    volumes:
      - .:/app
      - static_volume:/app/staticfiles
    ports:
      - "8000:8000"
    env_file:
      - .env
    depends_on:
      - db

  db:
    image: postgres:15
    volumes:
      - postgres_data:/var/lib/postgresql/data
    environment:
      - POSTGRES_DB=flashcard_db
      - POSTGRES_USER=postgres
      - POSTGRES_PASSWORD=postgres

  nginx:
    image: nginx:latest
    volumes:
      - ./nginx.conf:/etc/nginx/conf.d/default.conf
      - static_volume:/app/staticfiles
    ports:
      - "80:80"
    depends_on:
      - web

volumes:
  postgres_data:
  static_volume:
```

Run:
```bash
docker-compose up -d
docker-compose exec web python manage.py migrate
docker-compose exec web python manage.py createsuperuser
```

## Post-Deployment

1. **Test all features**
2. **Set up backups** for database
3. **Monitor logs** for errors
4. **Set up monitoring** (e.g., Sentry)
5. **Configure email** (for password resets, etc.)
6. **Set up CDN** for static files (optional)
7. **Enable caching** (Redis/Memcached)

## Monitoring & Maintenance

### Log Management
```bash
# View Django logs
tail -f /var/log/gunicorn/error.log

# View Nginx logs
tail -f /var/log/nginx/error.log
```

### Database Backup
```bash
# PostgreSQL backup
pg_dump flashcard_db > backup_$(date +%Y%m%d).sql

# Restore
psql flashcard_db < backup_20260101.sql
```

### Updates
```bash
# Pull latest code
git pull origin main

# Install new dependencies
pip install -r requirements.txt

# Run migrations
python manage.py migrate

# Collect static files
python manage.py collectstatic --noinput

# Restart service
sudo systemctl restart flashcard
```

---

**Your flashcard app is now ready for production! 🚀**
