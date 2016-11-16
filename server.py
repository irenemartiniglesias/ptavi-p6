#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Clase (y programa principal) para un servidor de eco en UDP simple
"""

import socketserver
import sys
import os

PORT = int(sys.argv[2])
SERVER = sys.argv[1]
FICHERO = sys.argv[3]

class EchoHandler(socketserver.DatagramRequestHandler):
    """
    Echo server class
    """

    def handle(self):
        # Escribe dirección y puerto del cliente (de tupla client_address)
        while 1:
            # Leyendo línea a línea lo que nos envía el cliente
            line = self.rfile.read()
            linea_decod = line.decode('utf-8')
            METODO = linea_decod.split(' ')[0]
            METODOS = ['INVITE', 'BYE', 'ACK']
            if len(linea_decod) >= 2:
                if METODO == 'INVITE':
                    mensaje = b'SIP/2.0 100 Trying \r\n\r\n'
                    mensaje += b'SIP/2.0 180 Ring \r\n\r\n'
                    mensaje += b'SIP/2.0 200 OK \r\n\r\n'
                    self.wfile.write(mensaje)
                elif METODO == 'ACK':
                    aEjecutar = 'mp32rtp -i 127.0.0.1 -p 23032 < ' + FICHERO
                    os.system(aEjecutar)
                elif METODO == 'BYE':
                    mensaje = b'SIP/2.0 200 OK \r\n\r\n'
                    self.wfile.write(mensaje)
            else:
                print("El cliente nos manda " + linea_decod)
                
            # Si no hay más líneas salimos del bucle infinito
            if not line:
                break

if __name__ == "__main__":
    # Creamos servidor de eco y escuchamos
    serv = socketserver.UDPServer((SERVER, PORT), EchoHandler)
    print("Listening...")
    serv.serve_forever()
