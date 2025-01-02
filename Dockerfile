FROM ubuntu:20.04

# Instalar dependencias
RUN apt-get update && apt-get install -y \
    quagga \
    iproute2 \
    python3 \
    python3-pip

# Copiar archivos de configuración
COPY requirements.txt /tmp/
RUN pip3 install -r /tmp/requirements.txt

COPY prueba_bgp.py /usr/local/bin/
RUN chmod +x /usr/local/bin/prueba_bgp.py

CMD ["prueba_bgp.py"]
