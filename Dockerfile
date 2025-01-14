FROM ubuntu:20.04

# Instalar dependencias necesarias
RUN apt-get update && apt-get install -y \
    quagga \
    iproute2 \
    python3 \
    python3-pip \
    openssh-server

# Configurar el servidor SSH
RUN mkdir /var/run/sshd && \
    echo 'root:password' | chpasswd && \
    sed -i 's/#PermitRootLogin prohibit-password/PermitRootLogin yes/' /etc/ssh/sshd_config && \
    echo "GatewayPorts yes" >> /etc/ssh/sshd_config

# Exponer el puerto SSH
EXPOSE 22

# Copiar y configurar los requisitos de Python
COPY requirements.txt /tmp/
RUN pip3 install -r /tmp/requirements.txt

# Copiar el script Python
COPY prueba_bgp.py /usr/local/bin/
RUN chmod +x /usr/local/bin/prueba_bgp.py

# Iniciar el servidor SSH
CMD ["/usr/sbin/sshd", "-D"]
