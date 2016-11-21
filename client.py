#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""Programa cliente que abre un socket a un servidor"""

import socket
import sys

"""Cliente UDP simple."""

"""Dirección IP del servidor y puerto"""

try:
    METODO = sys.argv[1]
    DIRECCION = sys.argv[2]
    Linea_partes = DIRECCION.split('@')[1]
    USUARIO = DIRECCION.split('@')[0] + '@'
    SERVER = Linea_partes.split(':')[0]
    PORT = int(Linea_partes.split(':')[1])
except:
    sys.exit('Usage: python client.py method receiver@IP:SIPport')
 
if len(sys.argv) != 3:
    sys.exit('Usage: python client.py method receiver@IP:SIPport')

if PORT < 1024:
    sys.exit('PORT INCORRET')
     
"""Contenido que vamos a enviar"""
Linea_sip = ' sip:' + USUARIO + SERVER + ' SIP/2.0\r\n'
LINEA = METODO + Linea_sip


"""Creamos el socket, lo configuramos y lo atamos a un servidor/puerto"""
my_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
my_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
my_socket.connect((SERVER, PORT))

print("Enviando: " + LINEA)
my_socket.send(bytes(LINEA, 'utf-8') + b'\r\n')
data = my_socket.recv(1024)

print('Recibido -- ', data.decode('utf-8'))
print("Terminando socket...")

lista = data.decode('utf-8').split('\r\n\r\n')[0:-1]
if lista == ['SIP/2.0 100 Trying', 'SIP/2.0 180 Ring', 'SIP/2.0 200 OK']:
    LINEACK = 'ACK' + Linea_sip
    print ('Enviando: ' + LINEACK)
    my_socket.send(bytes(LINEACK, 'utf-8') + b'\r\n')
    data = my_socket.recv(1024)

   
"""Cerramos todo"""
my_socket.close()
print("Fin.")
