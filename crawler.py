import threading, urllib
from urllib.parse import urlparse
from urllib.parse import urljoin
from html.parser import HTMLParser
import urllib.request
import sys
from glob import glob
import fileinput
import time
from concurrent import futures
import os, signal
from configparser import ConfigParser

parser = ConfigParser()
parser.read('config_init.ini',encoding='utf-8')
max_workers = parser.get('config_init', 'cant_worker_url')

def run(url,cola,cola2):
    print(format(threading.current_thread().name))
    print("<Executing on Process with: %d >" % os.getpid())

    try:
        socket = urllib.request.urlopen(url)
    except:
        print("Error Temporary failure in name resolution")
        socket = urllib.request.urlopen(url)
    urlMarkUp = socket.read().decode("ascii", "ignore")
    print("Llega URL al crawler: %s" % url)
    global linkHTMLParser
    linkHTMLParser = LinkHTMLParser()
    linkHTMLParser.feed(urlMarkUp)
    urlsin = url.split('/')
    archivomod = open(urlsin[2] + ".txt", 'a')
    archivoleer = open(urlsin[2] + ".txt", 'r')
    contenido = archivoleer.read()
    urls = []
    if contenido == '':
        for link in linkHTMLParser.links:
            link = urljoin(url, link)
            urls.append(link)
            print("\t" + link)
            cola.put(link)
            cola2.put(link)
            archivomod.write(link + "\n")
        archivomod.close()
    else:
        input = fileinput.input(glob(urlsin[2] + ".txt"))
        for linea in input:
            cola.put(linea)
            cola2.put(linea)
        input.close()
        print("<Ya cargado Url %s >"%url)

def cmp(a, b):
    return (a > b) - (a < b)


class LinkHTMLParser(HTMLParser):
    A_TAG = "a"
    HREF_ATTRIBUTE = "href"
    A_TAG1="img"
    HREF_ATTRIBUTE1 = "src"

    def __init__(self):
        self.links = []
        HTMLParser.__init__(self)


    def handle_starttag(self, tag, attrs):
        if cmp(tag, self.A_TAG) == 0:
            for (key, value) in attrs:
                if cmp(key, self.HREF_ATTRIBUTE) == 0:
                    self.links.append(value)
        if cmp(tag, self.A_TAG1) == 0:
            for (key, value) in attrs:
                if cmp(key, self.HREF_ATTRIBUTE1) == 0:
                    self.links.append(value)
    def handle_endtag(self, tag):
        pass


def crawler(url,cola,cola2):
        print("Empezando Crawler-URL")
        print("<Executing on %d >" % os.getpid())
        global max_workers
        with futures.ThreadPoolExecutor(max_workers=int(max_workers)) as executor:
            for elem in url:
                future_to_url = executor.submit(run, elem, cola, cola2)
                print(future_to_url)

        cola.put("False")
