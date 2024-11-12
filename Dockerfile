# Basis-Image
FROM python:3.8-slim-buster

# Arbeitsverzeichnis setzen
WORKDIR /app

# Abhängigkeiten kopieren
COPY requirements.txt requirements.txt

# Abhängigkeiten installieren
RUN pip install --no-cache-dir -r requirements.txt

# Anwendungscode kopieren
COPY . .

# Port definieren, auf dem die App läuft
EXPOSE 5000

# Umgebungsvariable für Flask setzen
ENV FLASK_APP=app.py

# Startbefehl für die Anwendung
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"]
