# Simulación de BGP con Docker — Tutorial completo

Laboratorio de 4 routers BGP virtuales usando **Docker** y **Quagga**. Sirve para entender el funcionamiento de BGP en un entorno controlado y reproducible.

---

## Topología

```
          AS 65000          AS 65001
          router1 --------- router2
         /       \         /       \
        /         \       /         \
   router4       red BGP            router3
  AS 65003      192.168.10.0/24    AS 65002

  Red WAN: 10.0.0.0/24
  Red LAN: 172.16.0.0/24
  Red BGP: 192.168.10.0/24
```

| Router  | AS    | IP WAN      | IP LAN       | IP BGP        | Puerto SSH |
|---------|-------|-------------|--------------|---------------|-----------|
| router1 | 65000 | 10.0.0.2    | 172.16.0.2   | 192.168.10.2  | 2221      |
| router2 | 65001 | 10.0.0.3    | 172.16.0.3   | 192.168.10.3  | 2225      |
| router3 | 65002 | 10.0.0.4    | 172.16.0.4   | 192.168.10.4  | 2223      |
| router4 | 65003 | 10.0.0.5    | 172.16.0.5   | 192.168.10.5  | 2224      |

---

## Requisitos previos

- **Docker** y **Docker Compose** instalados
- Git instalado

Verificá que estén disponibles:

```bash
docker --version
docker compose version
git --version
```

---

## Paso 1 — Clonar el repositorio

```bash
git clone https://github.com/Mauroquil-bit/docker_bgp_4rt.git
cd docker_bgp_4rt
```

---

## Paso 2 — Construir las imágenes

```bash
docker compose build
```

Deberías ver al final:

```
✔ docker_bgp_4rt-router1  Built
✔ docker_bgp_4rt-router2  Built
✔ docker_bgp_4rt-router3  Built
✔ docker_bgp_4rt-router4  Built
```

---

## Paso 3 — Levantar los routers

```bash
docker compose up -d
```

Verificá que estén corriendo:

```bash
docker compose ps
```

Deberías ver los 4 routers en estado `Up`:

```
NAME      STATUS          PORTS
router1   Up              0.0.0.0:2221->22/tcp
router2   Up              0.0.0.0:2225->22/tcp
router3   Up              0.0.0.0:2223->22/tcp
router4   Up              0.0.0.0:2224->22/tcp
```

> **Nota:** el puerto 2222 está reservado por el sistema. Por eso router2 usa el 2225.

---

## Paso 4 — Conectarse a un router por SSH

```bash
ssh root@localhost -p 2221   # router1
ssh root@localhost -p 2225   # router2
ssh root@localhost -p 2223   # router3
ssh root@localhost -p 2224   # router4
```

**Contraseña:** `password`

---

## Paso 5 — Verificar BGP con vtysh

Una vez dentro del router, los comandos de red **no son comandos de bash**. Hay que entrar a `vtysh`:

```bash
vtysh
```

Verás el prompt cambiar a:

```
Hello, this is Quagga (version 0.99.XX).
router1#
```

### Comandos útiles dentro de vtysh

```
show ip bgp summary          # Estado de las sesiones BGP
show ip bgp neighbors        # Detalle de cada vecino BGP
show ip route                # Tabla de rutas completa
show ip route bgp            # Solo rutas aprendidas por BGP
show running-config          # Configuración activa
```

Para salir:

```
exit
```

---

## Resultado esperado — `show ip bgp summary`

```
BGP router identifier 192.168.10.2, local AS number 65000
Peers 3, using 27 KiB of memory

Neighbor        V    AS   State/PfxRcd
192.168.10.3    4  65001  Established
192.168.10.4    4  65002  Established
192.168.10.5    4  65003  Established
```

Si el estado es `Established` en todos los vecinos, el laboratorio está funcionando correctamente.

---

## Comandos de gestión

```bash
# Ver logs de un router
docker compose logs router1

# Detener todo
docker compose down

# Reiniciar todo
docker compose down && docker compose up -d

# Ejecutar un comando directo sin SSH
docker exec -it router1 vtysh -c "show ip bgp summary"
```

---

## Problemas comunes y soluciones

### Error: puerto 2222 en uso
```
failed to bind host port 0.0.0.0:2222/tcp: address already in use
```
**Causa:** el entorno (dev container, VM) ya usa ese puerto para SSH.  
**Solución:** en `docker-compose.yml`, cambiar `"2222:22"` por `"2225:22"` en router2.

---

### Los contenedores arrancan y se apagan solos
```
*** Error reading config: There is no such command.
*** Error occurred processing line 6, below:
 ip address 10.0.0.2/24  # IP de la red WAN
```
**Causa:** Quagga no soporta comentarios `#` en línea dentro de los archivos `.conf`.  
**Solución:** eliminar los comentarios al final de cada línea en los archivos `zebra_rt*.conf`.

---

### `show ip bgp` no funciona en bash
```
-bash: show: command not found
```
**Causa:** los comandos de routing son de Quagga, no de bash.  
**Solución:** primero ejecutar `vtysh` y luego lanzar los comandos.

---

### Sesiones BGP en estado `Active` (no `Established`)
**Causa:** los daemons `zebra` o `bgpd` no levantaron correctamente.  
**Solución:**
```bash
docker compose logs router1   # revisar errores
docker compose down && docker compose up -d
```

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
