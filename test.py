import datetime
import time
epoch_time = 1706955190
room_create_time = datetime.datetime.fromtimestamp(epoch_time).strftime('%H:%M:%S')
ending_time = epoch_time + 14400
ending_time_str = datetime.datetime.fromtimestamp(ending_time).strftime('%H:%M:%S')
now = datetime.datetime.now()


remain = datetime.timedelta(seconds=ending_time-ending_time)
print(room_create_time, ending_time_str, now)
print(remain)


create_time_epoch = 1706955190
t = time.ctime(create_time_epoch)

create_time_epoch = 1706955190
create_time_str = time.strftime('%H:%M:%S', time.localtime(create_time_epoch))
ending_time_epoch = create_time_epoch + 14400
ending_time_str = time.strftime('%H:%M:%S', time.localtime(ending_time_epoch))

notification_time_epoch = ending_time_epoch - 300
notification_time_str = time.strftime('%H:%M', time.localtime(notification_time_epoch))

sleep_time = notification_time_epoch - create_time_epoch
sleep_time_str = time.strftime("%H:%M:%S", time.gmtime(sleep_time))

print('=======================')
#print("room_create_time", create_time_str)
#print("room_end_time", ending_time_str)
#print("sleep_time", sleep_time_str)
#print("noti_time", notification_time_str)
print('=======================')


import schedule
import threading

unique_id = "@perfumexlab"
def notify(message):
    print("XXX")
    #r = requests.post(url, headers=headers, data = {'message':message})

def notify_at_specific_time(message, waiting_seconds):
    print('['+time.strftime('%H:%M')+']['+unique_id+'] Set notification at ' + notification_time_str)
    while True:
        n = schedule.idle_seconds()
        if n is None:
            # no more jobs
            break
        elif n > 0:
            # sleep exactly the right amount of time
            print('['+time.strftime('%H:%M')+']['+unique_id+'] waiting for ' + str(n))
            time.sleep(n)
            notify(message)

create_time_epoch = 1708357225
create_time_str = time.strftime('%H:%M', time.localtime(create_time_epoch))
ending_time_epoch = create_time_epoch + 14400
ending_time_str = time.strftime('%H:%M', time.localtime(ending_time_epoch))
notification_time_epoch = ending_time_epoch - 300
notification_time_str = time.strftime('%H:%M', time.localtime(notification_time_epoch))

time_now = int(time.time())
waiting_seconds = 14400 - 300 - (time_now - create_time_epoch)
print('Now               :', time_now )
print('Create Time       :', create_time_epoch )
print('Notification Time :', notification_time_epoch)
m, s = divmod(waiting_seconds, 60)
h, m = divmod(m, 60)
print('Waiting Seconds   :',waiting_seconds,f'{h:02d}:{m:02d}')



notify_message = unique_id + ' is ending at ' + ending_time_str
notification_time_str = "23:30"
thread = threading.Thread(target=notify_at_specific_time, args={notify_message, waiting_seconds})
thread.start()


