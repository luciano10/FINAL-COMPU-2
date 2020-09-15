import mmap
import threading
from os import listdir
from glob import glob
import fileinput
import sys
import time
import os, signal
from concurrent import futures

def buscarUrl(palabra):
    print(format(threading.current_thread().name))
    link = glob('*.txt')
    result= []
    if(link):
        input = fileinput.input(link)
        for linea in input:
            if palabra in linea:
                result.append(linea)
                #print(linea)
            if not linea:
                break
        input.close()
    else:
        print("No esta Cargado Nada")
    return result

def buscarImg(palabra):
    print(format(threading.current_thread().name))
    img = glob('*/*')
    result = []
    if(img):
        for elem in img:
            try:
                ext=(elem.split("/")[1]).split(".")[1]
                if(ext=="png" or ext=="jpg" or ext=="gif" or ext=="jpeg" or ext=="eps"):
                    if palabra in elem.split("/")[1]:
                        #print(elem.split("/")[1])
                        #result.append(elem.split("/")[1])
                        result.append(elem)
                    if not linea:
                        break
            except:
                pass
    else:
        print("No esta Cargado Nada")
    return result
def consulta(palabra,r):
            print("Empezando Consulta-URL-Imagen")
            print("<Executing on %d >" % os.getpid())
            with futures.ThreadPoolExecutor(max_workers=2) as executor:
                for elem in palabra:
                    print("<Buscando: %s >" % elem)
                    future_to_url = executor.submit(buscarUrl,elem)
                    print("Url: %s" % future_to_url)
                    future_to_url2 = executor.submit(buscarImg, elem)
                    print("Imagen: %s" % future_to_url2)
            for elem in future_to_url.result():
                r.put(elem)
            for elem in future_to_url2.result():
                r.put(elem)


