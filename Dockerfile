FROM python:3.11-slim

# Kopiere alle Dateien ins Image
COPY . /action

WORKDIR /action

# Installiere ggf. weitere Abhängigkeiten hier
# RUN pip install -r requirements.txt

ENTRYPOINT ["python", "findTestbox.py"]