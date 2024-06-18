import subprocess
import threading
import time

def callback(id):
    print("[Execute] python", '3-seller-center.py', id)
    process = subprocess.run(['python', '3-seller-center.py', id])

threads = []
threads_sleep_time = []

account_count = 2

for temp in range(account_count):
    threads.append([])
    threads_sleep_time.append(2)

while True:
    for i in range(account_count):
        if threads[i] == []:
            time.sleep(threads_sleep_time[i])
            threads[i] = threading.Thread(target=callback, args=[str(i)])
            threads[i].start()
            #print('[xxx]', type(threads[i]))

            threads_sleep_time[i] = threads_sleep_time[i] * 2
            if(threads_sleep_time[i] > 900):
                threads_sleep_time[i] = 900

        elif type(threads[i]) == threading.Thread:
            if not threads[i].is_alive():
                threads[i] = []
    time.sleep(2)
    #process = subprocess.run(['python', 'tiktok-client.py', account[0], account[1]])

