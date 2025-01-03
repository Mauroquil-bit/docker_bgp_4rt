#!/usr/bin/env python3

import netmiko

# El resto de tu script...
print("Simulación de BGP activa")


def configure_router(router_ip, username, password):
    connection = netmiko.ConnectHandler(
        device_type='linux',
        ip=router_ip,
        username=username,
        password=password
    )
    
    commands = [
        'vtysh',
        'configure terminal',
        'router bgp 65000',
        'neighbor 192.168.1.2 remote-as 65001',
        'network 10.0.0.0/24',
        'exit',
        'exit',
        'write memory'
    ]
    
    for command in commands:
        connection.send_command(command)
    
    connection.disconnect()

if __name__ == "__main__":
    routers = [
        {"ip": "172.19.0.2", "username": "root", "password": "password"},
        {"ip": "172.19.0.3", "username": "root", "password": "password"},
        {"ip": "172.19.0.4", "username": "root", "password": "password"},
        {"ip": "172.19.0.5", "username": "root", "password": "password"}
    ]
    
    for router in routers:
        configure_router(router["ip"], router["username"], router["password"])
