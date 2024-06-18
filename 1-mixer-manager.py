import subprocess
import threading
import time

def callback():
    process = subprocess.run(['python', '1-mixer.py'])

thread = []
thread_sleep_time = 2

while True:
    if thread == []:
        time.sleep(thread_sleep_time)
        thread = threading.Thread(target=callback)
        thread.start()
        print('['+time.strftime('%H:%M')+'][===== Mixer Started =====]')


    elif type(thread) == threading.Thread:
        if not thread.is_alive():
            print('['+time.strftime('%H:%M')+'][===== Mixer Ended =====]')
            thread = []
    time.sleep(2)
    #process = subprocess.run(['python', 'tiktok-client.py', account[0], account[1]])