import os
from concurrent.futures import ProcessPoolExecutor
from concurrent import futures
import threading
def run(i):
    print("Executing on {} ".format(threading.current_thread().name))

def task():
        ex = futures.ThreadPoolExecutor(max_workers=2)
        f = ex.submit(run)
        print("{}".format(f))       
        print("Executing on Process with PID: {}".format(os.getpid()))

def main():
    executor = ProcessPoolExecutor(max_workers=2)
    task1 = executor.submit(task)
    task2 = executor.submit(task)

if __name__ == '__main__':
    main()
