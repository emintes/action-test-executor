FROM python:3.11-slim

# Build-Args für optionale Anpassungen
ARG EXTRA_COMMANDS=""

# Setze das Arbeitsverzeichnis
WORKDIR /workspace

# Kopiere alle Dateien ins Image
COPY . /workspace

RUN apt update

# Führe zusätzliche Shell-Commands aus, wenn gesetzt
RUN if [ -n "${EXTRA_COMMANDS}" ]; then \
        echo "Running extra commands:" && \
        printf '%b' "$EXTRA_COMMANDS" > /tmp/extra_commands.sh && \
        chmod +x /tmp/extra_commands.sh && \
        bash /tmp/extra_commands.sh; \
    fi

RUN apt install -y libopenjp2-7

RUN apt install -y \
    libtiff-dev \
    libjpeg-dev \
    zlib1g-dev \
    libfreetype6-dev \
    liblcms2-dev \
    libwebp-dev \
    libharfbuzz-dev \
    libfribidi-dev \
    libxcb1 \
    libpng-dev

RUN pip install --upgrade pip

RUN mkdir -p /root/.config/pip && \
    echo "[global]\nextra-index-url=https://www.piwheels.org/simple" > /root/.config/pip/pip.conf

# Installiere notwendige python bibliotheken
RUN apt install libopenblas0-pthread libgfortran5
RUN pip3 install --prefer-binary numpy==2.2.4
#RUN pip3 install numpy
RUN pip3 install --prefer-binary matplotlib==3.10.1
#RUN pip3 install matplotlib
#RUN apt-get install -y python3-matplotlib
RUN pip3 install pyserial
RUN pip3 install mpremote

# Mache das Entrypoint-Skript ausführbar
RUN chmod +x /workspace/entrypoint.sh

ENTRYPOINT ["/workspace/entrypoint.sh"]