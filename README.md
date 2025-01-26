# Simulación de BGP con Docker

Este proyecto es una simulación de configuración de BGP entre múltiples routers virtuales utilizando **Docker** y **Quagga**. El objetivo principal es entender el funcionamiento de BGP en un entorno controlado, resolviendo problemas reales relacionados con redes y automatización.

---

## Características principales

- **4 Routers simulados** configurados como contenedores Docker.
- **Daemons de Quagga** (`zebra` y `bgpd`) configurados para gestionar las rutas y las sesiones BGP.
- Conectividad entre routers a través de tres redes: `WAN`, `LAN`, y `BGP`.
- Pruebas exitosas de conectividad y anuncios de rutas mediante `show ip bgp`.

---

## Requisitos previos

- **Docker** y **Docker Compose** instalados.
- Conocimientos básicos de redes y BGP.

---

## Estructura del proyecto

```plaintext
routers_bgp_4/
|— docker_bgp_4rt/
   |— bgpd_rt1.conf
   |— bgpd_rt2.conf
   |— bgpd_rt3.conf
   |— bgpd_rt4.conf
   |— zebra_rt1.conf
   |— zebra_rt2.conf
   |— zebra_rt3.conf
   |— zebra_rt4.conf
   |— docker-compose.yml
   |— Dockerfile
   |— README.md
```

---

## Configuración

### **Archivo `bgpd.conf` (ejemplo para router1)**

```plaintext
hostname bgpd
password zebra
enable password zebra
router bgp 65000
  neighbor 192.168.10.3 remote-as 65001
  neighbor 192.168.10.4 remote-as 65002
  neighbor 192.168.10.5 remote-as 65003
  network 10.0.0.0/24
  network 172.16.0.0/24
log file /var/log/quagga/bgpd_router1.log
```

### **Archivo `zebra.conf` (ejemplo para router1)**

```plaintext
hostname zebra
password zebra
enable password zebra

interface eth0
  ip address 10.0.0.2/24
interface eth1
  ip address 172.16.0.2/24
interface eth2
  ip address 192.168.10.2/24

log file /var/log/quagga/zebra_router1.log
```

---

## Ejecución del proyecto

### 1. Clonar el repositorio

```bash
git clone https://github.com/tu_usuario/routers_bgp_4.git
cd routers_bgp_4/docker_bgp_4rt
```

### 2. Construir y levantar los contenedores

```bash
docker-compose up -d
```

### 3. Verificar los logs

Asegúrate de que los daemons estén corriendo correctamente:

```bash
docker logs router1
```

### 4. Conectarte a un router

```bash
docker exec -it router1 bash
```

Dentro del contenedor:

```bash
vtysh
show ip bgp summary
```

---

## Resultados esperados

### **`show ip bgp summary`**

```plaintext
BGP router identifier 192.168.10.2, local AS number 65000
RIB entries 3, using 336 bytes of memory
Peers 3, using 27 KiB of memory

Neighbor        V         AS MsgRcvd MsgSent   TblVer  InQ OutQ Up/Down  State/PfxRcd
192.168.10.3    4 65001       0       0        0    0    0 00:05:22   Established
192.168.10.4    4 65002       0       0        0    0    0 00:05:22   Established
192.168.10.5    4 65003       0       0        0    0    0 00:05:22   Established

Total number of neighbors 3
```

### **`show ip bgp`**

```plaintext
   Network          Next Hop            Metric LocPrf Weight Path
*> 10.0.0.0/24      0.0.0.0                  0         32768 i
*> 172.16.0.0/24    0.0.0.0                  0         32768 i
```

---

## Problemas comunes

1. **Error: `privs_init: initial cap_set_proc failed`**
   - Solución: Agrega `privileged: true` y `cap_add: [NET_ADMIN, NET_RAW]` en el archivo `docker-compose.yml`.

2. **Sesiones BGP en estado `Active`**
   - Solución: Verifica la conectividad entre los routers usando `ping`.

---

## Aprendizajes clave

- Configuración detallada de BGP usando Quagga.
- Resolución de problemas de permisos y conectividad en entornos Docker.
- Comprensión del funcionamiento de `zebra` y `bgpd` en redes simuladas.

---

## Contribuciones

Si deseas mejorar este proyecto, por favor envía un PR o abre un issue en el repositorio. ¡Todas las contribuciones son bienvenidas!

---

## Licencia

Este proyecto está bajo la licencia MIT. Consulta el archivo `LICENSE` para más información.
