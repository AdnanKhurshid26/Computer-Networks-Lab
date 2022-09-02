import threading
import time

e = threading.Event()
e.clear()


def fun1():
    time.sleep(5)
    e.set()
    print("fun1")

def fun2():
    e.wait()
    print("fun2")

thread1 = threading.Thread(target=fun1)
thread2 = threading.Thread(target=fun2)

def start():
    thread1.start()
    thread2.start()

start()