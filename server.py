#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""Clase (y programa principal) para un servidor de eco en UDP simple"""

import socketserver
import sys
import os


try:

    PORT = int(sys.argv[2])
    SERVER = sys.argv[1]
    FICH = sys.argv[3]
except:
    sys.exit('Usage: python client.py method receiver@IP:SIPport')


class EchoHandler(socketserver.DatagramRequestHandler):
    """
    Echo server class
    """

    def handle(self):
        """Escribe dirección y puerto del cliente (de tupla client_address)"""
        while 1:
            """Leyendo línea a línea lo que nos envía el cliente"""
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
                    print("El cliente nos manda " + linea_decod)
                elif METODO == 'ACK':
                    aEjecutar = './mp32rtp -i ' + SERVER + ' -p 23032 <' + FICH
                    os.system(aEjecutar)
                    print("El cliente nos manda " + linea_decod)
                elif METODO == 'BYE':
                    mensaje = b'SIP/2.0 200 OK \r\n\r\n'
                    self.wfile.write(mensaje)
                    print("El cliente nos manda " + linea_decod)
                elif METODO not in METODOS:
                    mensaje = b'SIP/2.0 405 Method Not Allowed \r\n\r\n'
                    self.wfile.write(mensaje)
                    print("El cliente nos manda " + linea_decod)
                else:
                    self.wfile.write('b"SIP/2.0 400 Bad Request\r\n\r\n')
                    print("El cliente nos manda " + linea_decod)
            else:
                print(" ")

            """Si no hay más líneas salimos del bucle infinito"""
            if not line:
                break


if __name__ == "__main__":

    if PORT < 1024:
        sys.exit('PORT INCORRET, please enter a port bigger than 1024')
    if len(sys.argv) != 4:
        sys.exit('Usage: python client.py method receiver@IP:SIPport')

    """Creamos servidor de eco y escuchamos"""
    serv = socketserver.UDPServer((SERVER, PORT), EchoHandler)
    print("Listening...")
    try:
        serv.serve_forever()
    except KeyboardInterrupt:
        print("Finalizado servidor")
