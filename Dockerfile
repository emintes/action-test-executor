FROM python:3.11-slim

# Setze das Arbeitsverzeichnis
WORKDIR /workspace

# Kopiere alle Dateien ins Image
COPY . /workspace

RUN apt update

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

RUN apt install -y dos2unix

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

# Jetzt alles fuer den ST-Link:
RUN apt-get install -y git cmake make gcc libusb-1.0-0-dev gcc-arm-none-eabi
#RUN rm -rf stlink
RUN git clone https://github.com/stlink-org/stlink.git
RUN make -C stlink release
RUN make -C stlink/build/Release install
RUN export LD_LIBRARY_PATH=/usr/local/lib:$LD_LIBRARY_PATH
RUN echo "/usr/local/lib" | tee /etc/ld.so.conf.d/stlink.conf
RUN ldconfig

# Mache das Entrypoint-Skript ausführbar
RUN chmod +x /workspace/entrypoint.sh

ENTRYPOINT ["/workspace/entrypoint.sh"]