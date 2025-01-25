FROM ubuntu:20.04

ENV DEBIAN_FRONTEND=noninteractive
ENV TZ=Etc/UTC

# Instalar dependencias necesarias
RUN apt-get update && apt-get install -y \
    quagga \
    iproute2 \
    python3 \
    python3-pip \
    openssh-server \
    iputils-ping \
    net-tools \
    traceroute

# Configurar el servidor SSH
RUN mkdir /var/run/sshd && \
    echo 'root:password' | chpasswd && \
    sed -i 's/#PermitRootLogin prohibit-password/PermitRootLogin yes/' /etc/ssh/sshd_config && \
    echo "GatewayPorts yes" >> /etc/ssh/sshd_config

# Crear archivo para inicialización de Quagga
RUN echo 'zebra=yes\nbgpd=yes' > /etc/quagga/daemons && \
    touch /var/log/quagga.log && \
    chown quagga:quagga /var/log/quagga.log

# Exponer el puerto SSH
EXPOSE 22

# Copiar y configurar los requisitos de Python
COPY requirements.txt /tmp/
RUN pip3 install -r /tmp/requirements.txt

# Copiar el script Python
COPY prueba_bgp.py /usr/local/bin/
RUN chmod +x /usr/local/bin/prueba_bgp.py

# Iniciar servicios al inicio del contenedor
CMD service ssh start && \
    service zebra start && \
    service bgpd start && \
    tail -f /var/log/quagga.log
