FROM python:3.11-slim

# Setze das Arbeitsverzeichnis
WORKDIR /workspace

# Kopiere alle Dateien ins Image
COPY . /workspace

# Installiere pyserial
RUN pip install pyserial
RUN pip install mpremote

# Mache das Entrypoint-Skript ausführbar
RUN chmod +x /workspace/entrypoint.sh

ENTRYPOINT ["/workspace/entrypoint.sh"]