import sys
import os
import threading

unique_id = sys.argv[1]
token = sys.argv[2]

#test id & token
#unique_id = '@perfumexlab'
#token = 'NIcr2QFJ1eJCfuELDLZQzJpYF5E3mdt8x3Baho2qRGu'

# TiktokLiveClient
from TikTokLive import TikTokLiveClient
from TikTokLive.types.events import CommentEvent, ConnectEvent, DisconnectEvent, LiveEndEvent, UnknownEvent

#GTTS Speech
from gtts import gTTS
import time

#Line Notify
import requests
url = 'https://notify-api.line.me/api/notify'
headers = {'content-type':'application/x-www-form-urlencoded','Authorization':'Bearer '+token}

client: TikTokLiveClient = TikTokLiveClient(unique_id)

def notify(message):
    r = requests.post(url, headers=headers, data = {'message':message})

def notify_before_end(time_diff):
    #number of second to be waited until end - 300 (before 5 mins)
    waiting_seconds = 14400 - (time_diff % 14400) - 300
    if waiting_seconds > 0:
        # sleep exactly the right amount of time
        m, s = divmod(waiting_seconds, 60)
        h, m = divmod(m, 60)
        print('['+time.strftime('%H:%M')+']['+unique_id+'] set notification in', f'{h:02d}:{m:02d}', 'hours')
        time.sleep(waiting_seconds)
        message = unique_id + ' is ending in 5 mins'
        notify(message)

@client.on("connect")
async def on_connect(_: ConnectEvent):
    time_now = int(time.time())
    create_time_epoch = client.room_info['create_time']
    create_time_str = time.strftime('%H:%M', time.localtime(create_time_epoch))

    #check how many seconds have been passed since room created
    time_diff = time_now - create_time_epoch

    #check how many round for each 4hours passes
    round_count = int(time_diff / 14400)

    #find ending time (each 4 hours since created)
    ending_time_epoch = create_time_epoch + 14400*(round_count+1)
    ending_time_str = time.strftime('%H:%M', time.localtime(ending_time_epoch))

    print('['+time.strftime('%H:%M')+']['+unique_id+'] [Start] ' + create_time_str + ' [End] ' + ending_time_str)#, room_create_time)
    message = unique_id + ' ' + create_time_str + ' - ' + ending_time_str
    notify(message)

    #############################################
    #print('Now               :', time_now )
    #print('Create Time       :', create_time_epoch)
    #print('Ending Time       :', ending_time_epoch)
    #m, s = divmod(time_diff, 60)
    #h, m = divmod(m, 60)
    #print('Time Diff         :', time_diff,f'{h:02d}:{m:02d}')
    #print('Round count       :', round_count)
    ##############################################

    # Set time to notify
    thread = threading.Thread(target=notify_before_end, args={time_diff:time_diff})
    thread.start()

# Notice no decorator?
async def on_comment(event: CommentEvent):
    print('['+time.strftime('%H:%M')+']['+unique_id+'] '+ event.user.nickname + ' : ' + event.comment)
    message = event.user.nickname + ' : ' + event.comment
    #r = requests.post(url, headers=headers, data = {'message':message})
    tts = gTTS(event.comment, lang='th')

    filename = str(int(time.time())) + '_' + event.comment
    #filename = ''.join(e for e in filename if e.isalnum())
    tts.save(os.path.join('comment', filename +'.ogg'))

@client.on("disconnect")
async def on_disconnect(event: DisconnectEvent):
    print('['+time.strftime('%H:%M')+']['+unique_id+'] Disconnected')
    message = unique_id + ' disconnected'
    notify(message)

    #print("Disconnected")

@client.on("live_end")
async def on_connect(event: LiveEndEvent):
    print('['+time.strftime('%H:%M')+']['+unique_id+'] Livestream ended')
    #r = requests.post(url, headers=headers, data = {'message': unique_id + ' livestream ended'})

    #print(f"Livestream ended :(")

#@client.on("unknown")
#async def on_connect(event: UnknownEvent):
#    if event.type == 'WebcastGiftBroadcastMessage':
#        print('['+time.strftime('%H:%M')+']['+unique_id+'] UnknownEvent', event.type)
#    elif event.type == 'WebcastMsgDetectMessage':
#        print('['+time.strftime('%H:%M')+']['+unique_id+'] UnknownEvent', event.type)
#    elif event.type == 'WebcastHotRoomMessage':
#        print('['+time.strftime('%H:%M')+']['+unique_id+'] UnknownEvent', event.type)
        #r = requests.post(url, headers=headers, data = {'message': unique_id + ' ห้องกำลังฮอต'})
#    elif event.type == 'WebcastControlMessage':
#        print('['+time.strftime('%H:%M')+']['+unique_id+'] UnknownEvent', event.type)
#    elif event.type == 'WebcastLinkLayerMessage':
#        print('['+time.strftime('%H:%M')+']['+unique_id+'] UnknownEvent', event.type)
#    else:
#        print('['+time.strftime('%H:%M')+']['+unique_id+'] UnknownEvent', event.type)
        #r = requests.post(url, headers=headers, data = {'message': unique_id + ' unknown event'})

    #print(f"Event Type: {event.type}")
    #print(f"Event Base64: {event.base64}")

@client.on("error")
async def on_connect(error: Exception):
    # Otherwise, log the error
    # You can use the internal method, but ideally your own
    print('['+time.strftime('%H:%M')+']['+unique_id+'] UnknownError: ', error)
    #r = requests.post(url, headers=headers, data = {'message': unique_id + ' UnknownError'})
    #client._log_error(error)




# Define handling an event via a "callback"
client.add_listener("comment", on_comment)

if __name__ == '__main__':
    # Run the client and block the main thread
    # await client.start() to run non-blocking
    try:
        client.run()

    except Exception as e:
        print('['+time.strftime('%H:%M')+']['+unique_id+'] ERROR:', e)

        if hasattr(e, 'retry_after'):
            wait = e.retry_after
            print('Sleep for', wait, 'seconds')
            time.sleep(int(wait))

