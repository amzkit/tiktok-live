import datetime

epoch_time = 1706955190
room_create_time = datetime.datetime.fromtimestamp(epoch_time).strftime('%H:%M:%S')
ending_time = epoch_time + 14400
ending_time_str = datetime.datetime.fromtimestamp(ending_time).strftime('%H:%M:%S')
now = datetime.datetime.now()


remain = datetime.timedelta(seconds=ending_time-ending_time)
print(room_create_time, ending_time_str, now)
print(remain)