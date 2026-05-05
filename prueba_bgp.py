#!/usr/bin/env python3
"""
Script de prueba BGP para el laboratorio de 4 routers.
Conecta via SSH a cada router usando netmiko y recopila
el estado de las sesiones BGP. Expone los resultados via Flask.
"""

from flask import Flask, jsonify
from netmiko import ConnectHandler
import threading

app = Flask(__name__)

ROUTERS = [
    {"name": "router1", "host": "192.168.10.2", "as": 65000, "port": 22},
    {"name": "router2", "host": "192.168.10.3", "as": 65001, "port": 22},
    {"name": "router3", "host": "192.168.10.4", "as": 65002, "port": 22},
    {"name": "router4", "host": "192.168.10.5", "as": 65003, "port": 22},
]

SSH_CREDENTIALS = {
    "device_type": "quagga",
    "username": "root",
    "password": "password",
}

BGP_COMMANDS = [
    "show ip bgp summary",
    "show ip bgp neighbors",
    "show ip route bgp",
]


def get_bgp_info(router):
    """Conecta al router y ejecuta comandos BGP."""
    device = {
        **SSH_CREDENTIALS,
        "host": router["host"],
        "port": router["port"],
    }
    result = {"router": router["name"], "as": router["as"], "output": {}, "error": None}
    try:
        with ConnectHandler(**device) as conn:
            for cmd in BGP_COMMANDS:
                result["output"][cmd] = conn.send_command(cmd)
    except Exception as e:
        result["error"] = str(e)
    return result


@app.route("/bgp/status", methods=["GET"])
def bgp_status():
    """Devuelve el estado BGP de todos los routers."""
    results = []
    threads = []
    lock = threading.Lock()

    def fetch(router):
        info = get_bgp_info(router)
        with lock:
            results.append(info)

    for router in ROUTERS:
        t = threading.Thread(target=fetch, args=(router,))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

    return jsonify(results)


@app.route("/bgp/status/<router_name>", methods=["GET"])
def bgp_status_single(router_name):
    """Devuelve el estado BGP de un router específico."""
    router = next((r for r in ROUTERS if r["name"] == router_name), None)
    if not router:
        return jsonify({"error": f"Router '{router_name}' no encontrado"}), 404
    return jsonify(get_bgp_info(router))


@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok"})


if __name__ == "__main__":
    print("Iniciando servidor Flask para pruebas BGP...")
    print("Endpoints disponibles:")
    print("  GET /bgp/status          - Estado BGP de todos los routers")
    print("  GET /bgp/status/<nombre> - Estado BGP de un router específico")
    print("  GET /health              - Health check")
    app.run(host="0.0.0.0", port=5000, debug=False)
