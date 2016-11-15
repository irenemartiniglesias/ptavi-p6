#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Programa cliente que abre un socket a un servidor
"""

import socket
import sys

# Cliente UDP simple.

# Dirección IP del servidor y puerto.
METODO = sys.argv[1]
DIRECCION = sys.argv[2]
Linea0 = DIRECCION.split('@')
Linea1 = Linea0[1]
Linea2 = Linea1.split(':')
SERVER = Linea2[0]
PORT = int(Linea2[1])

# Contenido que vamos a enviar
LINE = '¡Hola mundo!'


if len(sys.argv) != 3:
    sys.exit('Usage: python client.py method receiver@IP:SIPport')

        
# Creamos el socket, lo configuramos y lo atamos a un servidor/puerto
my_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
my_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
my_socket.connect((SERVER, PORT))

print("Enviando: " + LINE)
my_socket.send(bytes(LINE, 'utf-8') + b'\r\n')
data = my_socket.recv(1024)

print('Recibido -- ', data.decode('utf-8'))
print("Terminando socket...")

# Cerramos todo
my_socket.close()
print("Fin.")
