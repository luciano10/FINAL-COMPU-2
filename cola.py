from multiprocessing import Process, Queue
class Cola():
    def __init__(self, funtion,element):
        self.funtion=funcion
        self.element=element

    def cola(self):
        cola = Queue()
        cola.put(self.element)
