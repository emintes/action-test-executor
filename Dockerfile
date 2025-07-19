FROM python:3.11-slim

# Kopiere alle Dateien ins Image
COPY entrypoint.sh /entrypoint.sh

# Installiere ggf. weitere Abhängigkeiten hier
# RUN pip install -r requirements.txt

ENTRYPOINT ["/entrypoint.sh"]