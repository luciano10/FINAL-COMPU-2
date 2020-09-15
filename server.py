from http.server import HTTPServer,BaseHTTPRequestHandler
from os import curdir, sep
from crawler import crawler
import cgi
from consulta import consulta
import threading
import multiprocessing
from imagen import imagen
import os, signal
import time
import socket
from socketserver import ThreadingMixIn
from concurrent.futures import ProcessPoolExecutor
from configparser import ConfigParser

crawler_pipe, imagen_pipe = multiprocessing.Pipe()

class myHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        print(" Peticion GET" + " <" + format(threading.current_thread().name) + "> ")
        try:
            sendReply = False
            if self.path.endswith(".html"):
                mimetype = 'text/html'
                sendReply = True
            if self.path.endswith(".jpg"):
                mimetype = 'image/jpg'
                sendReply = True
            if self.path.endswith(".gif"):
                mimetype = 'image/gif'
                sendReply = True
            if self.path.endswith(".png"):
                mimetype = 'image/png'
                sendReply = True
            if self.path.endswith(".js"):
                mimetype = 'application/javascript'
                sendReply = True
            if self.path.endswith(".css"):
                mimetype = 'text/css'
                sendReply = True

            if sendReply == True:
                f = open(curdir + sep + self.path, 'rb')
                self.send_response(200)
                self.send_header('Content-type', mimetype)
                self.end_headers()
                self.wfile.write(f.read())
                f.close()
            return

        except IOError:
            self.send_error(404, 'File Not Found: %s' % self.path)

    def do_POST(self):
        print(" Peticion POST"+" <"+format(threading.current_thread().name)+"> ")
        if self.path == "/sendurl":
            form = cgi.FieldStorage(
                fp=self.rfile,
                headers=self.headers,
                environ={'REQUEST_METHOD': 'POST',
                         'CONTENT_TYPE': self.headers['Content-Type'],
                         })
            ing_url = form["url"].value
            urls = ing_url.split()
            q = multiprocessing.Queue()
            u = multiprocessing.Queue()
            p = multiprocessing.Process(target=crawler, args=(urls,q,u))
            i = multiprocessing.Process(target=imagen, args=(q, u))
            p.start()
            i.start()
            i.join()
            p.join()

            print ("URl: %s" % ing_url)
            archivoleer = open("resultado.html", 'r')
            html = archivoleer.read()
            self.send_response(200)
            self.end_headers()
            self.wfile.write(("%s " % html).encode(encoding='utf_8'))
            if not u.empty():
                while not u.empty():
                    urls = u.get()
                    print(urls)
                    self.wfile.write(("<a href= %s" % urls + ">%s" % urls + "</a>").encode(encoding='utf_8'))
                    self.wfile.write(("<br><br>").encode(encoding='utf_8'))
            else:
                print("No hay Resultado")
                self.wfile.write(("<h2> No hay Resultado </h2>").encode(encoding='utf_8'))
                self.wfile.write(("<br><br>").encode(encoding='utf_8'))

            return

        if self.path == "/sendconsulta":
            form = cgi.FieldStorage(
                fp=self.rfile,
                headers=self.headers,
                environ={'REQUEST_METHOD': 'POST',
                         'CONTENT_TYPE': self.headers['Content-Type'],
                         })
            consul = form["consulta"].value
            consultas = consul.split()
            r = multiprocessing.Queue()
            c = multiprocessing.Process(target=consulta, args=(consultas,r))
            c.start()
            c.join()
            archivoleer = open("resultado.html", 'r')
            html = archivoleer.read()
            self.send_response(200)
            self.end_headers()
            self.wfile.write(("%s " % html).encode(encoding='utf_8'))
            print("Resultado Busquedad: ")
            if not r.empty():
                while not r.empty():
                    busquedad = r.get()
                    print(busquedad)
                    self.wfile.write(("<a href= %s" % busquedad + ">%s" % busquedad + "</a>").encode(encoding='utf_8'))
                    self.wfile.write(("<br><br>").encode(encoding='utf_8'))
            else:
                print("No hay Resultado")
                self.wfile.write(("<h2> No hay Resultado </h2>").encode(encoding='utf_8'))
                self.wfile.write(("<br><br>").encode(encoding='utf_8'))

            print ("Buscado: %s" % consul)
            return

class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
    address_family = socket.AF_INET
    """Handle requests in a separate thread."""
