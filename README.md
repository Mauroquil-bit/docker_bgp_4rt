# Proyecto: Simulación de Configuración BGP con Docker

## ¿De qué se trata este proyecto?

Este proyecto tiene como objetivo simular una configuración de **BGP (Border Gateway Protocol)** entre cuatro routers virtuales utilizando **Docker**. Los contenedores Docker representan routers, cada uno configurado para establecer sesiones BGP con sus vecinos. Al finalizar, los usuarios podrán observar la conectividad y configuración del protocolo mediante el comando `show ip bgp summary`.

Esta simulación está diseñada para:

- Entusiastas de redes que desean practicar configuraciones de BGP sin hardware físico.
- Profesionales que buscan entender mejor la integración entre redes y tecnologías de virtualización.
- Principiantes interesados en aprender sobre automatización de redes con Docker.

## ¿Qué es Docker?

Docker es una plataforma de contenedores que permite empaquetar aplicaciones y sus dependencias en un entorno aislado, conocido como contenedor. Esto garantiza que una aplicación funcione de manera consistente en cualquier sistema operativo que soporte Docker.

En términos simples, un contenedor es como una "mini-computadora virtual" que solo incluye los recursos necesarios para ejecutar una aplicación específica.

### Ventajas de Docker:

- **Portabilidad:** Los contenedores funcionan igual en cualquier sistema que tenga Docker instalado.
- **Eficiencia:** Usa menos recursos que las máquinas virtuales.
- **Aislamiento:** Cada contenedor está separado del sistema anfitrión y otros contenedores.

## ¿Dónde descargar Docker?

Puedes descargar Docker desde su página oficial: [Docker](https://www.docker.com/products/docker-desktop).

Recomendamos trabajar con **Docker Desktop**, ya que proporciona una interfaz gráfica amigable y herramientas útiles para desarrolladores y administradores de sistemas.

### Requisitos:

- **Windows:** Windows 10/11 con soporte para WSL2.
- **Mac:** macOS 10.15 o superior.
- **Linux:** Docker CLI y Docker Engine.

## Estructura del proyecto

El proyecto se organiza en el directorio `docker_bgp_4rt` con los siguientes archivos y carpetas:

```plaintext
docker_bgp_4rt/
├── docker-compose.yml
├── Dockerfile
├── prueba_bgp.py
├── quagga_rt1.config
├── quagga_rt2.config
├── quagga_rt3.config
├── quagga_rt4.config
├── README.md
└── requirements.txt
```

### Descripción de cada archivo

1. **`docker-compose.yml`****:**
   Este archivo define y coordina los cuatro contenedores que representan los routers virtuales. También configura las redes virtuales (WAN, LAN, BGP) y asigna direcciones IP y puertos SSH para cada contenedor.

2. **`Dockerfile`****:**
   Describe cómo construir la imagen base para los routers. Incluye:

   - Instalación de Quagga (un software de ruteo).
   - Configuración de SSH para acceso remoto.
   - Instalación de dependencias como Python y Netmiko.

3. **`prueba_bgp.py`****:**
   Un script Python que automatiza la configuración de BGP en los routers usando la biblioteca **Netmiko**.

   - **Netmiko:** Herramienta para gestionar dispositivos de red a través de SSH.
   - Este script se conecta a cada router, ejecuta comandos en el protocolo BGP y valida la configuración.

4. **`quagga_rt1.config`**** a ****`quagga_rt4.config`****:**
   Archivos de configuración específicos para cada router, utilizados por Quagga.

   - Cada archivo define el Autonomous System (AS) de un router, los vecinos BGP y las redes que anuncia.

5. **`requirements.txt`****:**
   Lista de bibliotecas Python necesarias para ejecutar el proyecto, como Netmiko y Flask.

6. **`README.md`****:**
   Este archivo, que proporciona una guía completa para configurar y ejecutar el proyecto.

---

## Explicación detallada del proyecto

### Redes virtuales configuradas

Se crean tres redes virtuales para conectar los routers:

- **WAN (****`10.0.0.0/24`****):** Red que conecta todos los routers como si fueran enlaces de proveedores de servicios.
- **LAN (****`172.16.0.0/24`****):** Red interna para simular la comunicación local.
- **BGP (****`192.168.10.0/24`****):** Red para establecer sesiones BGP entre routers.

### Flujo de trabajo:

1. **Construcción de la imagen Docker:**
   Usando el archivo `Dockerfile`, cada contenedor se prepara con las herramientas necesarias (Quagga, SSH, Python).

2. **Definición de contenedores:**
   En `docker-compose.yml`, se especifica:

   - Asignación de redes.
   - Direcciones IP para cada contenedor.
   - Montaje de configuraciones individuales (`quagga_rt*.config`).

3. **Configuración de BGP:**
   El script `prueba_bgp.py` automatiza la configuración del protocolo BGP:

   - Se conecta a cada router mediante SSH.
   - Ejecuta comandos para configurar vecinos, AS y redes anunciadas.

4. **Pruebas de conectividad:**
   Los usuarios pueden conectarse a cada contenedor por SSH y verificar la configuración de BGP:

   ```bash
   ssh root@localhost -p 2221
   vtysh
   show ip bgp summary
   ```

---

## Explicación general del proyecto

Este proyecto es una forma accesible y práctica de aprender sobre BGP y virtualización con Docker. ¡No necesitas hardware costoso ni conocimientos avanzados para empezar! Además, está diseñado para ser comprensible tanto para principiantes como para colegas avanzados.

### Beneficios de este proyecto:

- Experimentar con configuraciones reales de BGP.
- Comprender la integración de redes con tecnologías modernas como Docker.
- Practicar automatización usando Python y Netmiko.

---

## Instrucciones para ejecutar el proyecto

1. **Clonar el repositorio:**

   ```bash
   git clone <URL-del-repositorio>
   cd docker_bgp_4rt
   ```

2. **Construir las imágenes Docker:**

   ```bash
   docker-compose build
   ```

3. **Levantar los contenedores:**

   ```bash
   docker-compose up -d
   ```

4. **Verificar conectividad:**
   Conéctate a un router por SSH:

   ```bash
   ssh root@localhost -p 2221
   vtysh
   show ip bgp summary
   ```

---

¡Espero que disfrutes este proyecto tanto como yo al desarrollarlo! Si tienes dudas o sugerencias, no dudes en contactarme. 🚀

