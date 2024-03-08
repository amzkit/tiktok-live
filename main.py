import os
import time
import subprocess
import threading

def wait_for_event(e, index, file, opt=[]):
    process = subprocess.run(['python', file])

e = threading.Event()
thread = threading.Thread(target=wait_for_event, args=[e, 0, 'play-background-music.py'])
#thread = threading.Thread(target=run, args=[1, 'siri.py'])

thread.start()

while True:
    command = input()
    if command == "w":
        e.set()
    elif command == "r":
        thread.notify()