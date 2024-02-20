import sys
import os
import threading
import requests
import time

unique_id = '@perfumexlab'
token = 'NIcr2QFJ1eJCfuELDLZQzJpYF5E3mdt8x3Baho2qRGu'

url = 'https://notify-api.line.me/api/notify'
headers = {'content-type':'application/x-www-form-urlencoded','Authorization':'Bearer '+token}

def notify(message):
    r = requests.post(url, headers=headers, data = {'message':message})

def notify_before_end(time_diff):
    print("NOTIFY", time_diff)
    #waiting_seconds = int(waiting_seconds)
    #number of second to be waited until end - 300 (before 5 mins)
    waiting_seconds = 14400 - (time_diff % 14400) - 300
    if waiting_seconds > 0:
        # sleep exactly the right amount of time
        m, s = divmod(waiting_seconds, 60)
        h, m = divmod(m, 60)
        print('['+time.strftime('%H:%M')+']['+unique_id+'] set notification in', f'{h:02d}:{m:02d}', 'hours')
        #time.sleep(int(waiting_seconds))
        message = unique_id + ' is ending in 5 mins'
        notify(message)

time_now = int(time.time())
create_time_epoch = 1708419600
create_time_str = time.strftime('%H:%M', time.localtime(create_time_epoch))

time_diff = time_now - create_time_epoch
round_count = int(time_diff / 14400)

ending_time_epoch = create_time_epoch + 14400*round_count

ending_time_str = time.strftime('%H:%M', time.localtime(ending_time_epoch))

waiting_seconds = 14400 - (time_diff % 14400)

print('Now               :', time_now )
print('Create Time       :', create_time_epoch)
print('Ending Time       :', ending_time_epoch)
m, s = divmod(time_diff, 60)
h, m = divmod(m, 60)
print('Time Diff         :', time_diff,f'{h:02d}:{m:02d}')
m, s = divmod(waiting_seconds, 60)
h, m = divmod(m, 60)
print('Round count       :', round_count)
print('Waiting Seconds   :',waiting_seconds,f'{h:02d}:{m:02d}')

print('['+time.strftime('%H:%M')+']['+unique_id+'] [Start] ' + create_time_str + ' [End] ' + ending_time_str)#, room_create_time)
#message = unique_id + 'is on live'# + room_create_time
message = unique_id + ' ' + create_time_str + ' - ' + ending_time_str
notify(message)

thread = threading.Thread(target=notify_before_end, args={time_diff:time_diff})
thread.start()