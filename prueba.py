from crawler import CrawlerThread
from consulta import MiHilocons
import threading

def prueba():
    cond = threading.Condition()
    CrawlerThread("http://www.um.edu.ar/es/",cond).start()
    MiHilocons("um",cond).start()

prueba()