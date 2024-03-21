import sys
from threading import Thread

def readinput():
    for line in sys.stdin:
        print(line.rstrip())

Thread(target=readinput).start()
while True:
    pass