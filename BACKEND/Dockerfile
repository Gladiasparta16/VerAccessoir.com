FROM python:3.11-slim

WORKDIR /app

# Installer les dépendances
COPY BACKEND/requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

# Copier tout le projet
COPY . /app

WORKDIR /app/BACKEND
ENV PYTHONUNBUFFERED=1

EXPOSE 5000

# Démarrer l'application via Gunicorn
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "app:app"]
