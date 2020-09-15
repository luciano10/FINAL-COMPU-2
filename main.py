from server import myHandler
from http.server import HTTPServer
from threading import Thread
import multiprocessing
import socket
from server import ThreadedHTTPServer
from socketserver import ThreadingMixIn
import argparse
import os
from configparser import ConfigParser
parser = ConfigParser()
parser.read('config_init.ini',encoding='utf-8')
port = parser.get('config_init', 'port')

if int(port):
        PORT_NUMBER=int(port)
        try:
            server_ipv4 = ThreadedHTTPServer(('', PORT_NUMBER), myHandler)
            print('Started httpserver on port ', PORT_NUMBER)
            print('Starting server, use <Ctrl-C> to stop')
            th4 = multiprocessing.Process(target=server_ipv4.serve_forever)
            th4.start()
            print("Process IPV4 --> %s"%th4)
            th4.join()

        except KeyboardInterrupt:
            pass
            th4.terminate()
            print("\nTermino Servidor")


