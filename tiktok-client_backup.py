import sys
import os
import schedule
#unique_id = sys.argv[1]
#token = sys.argv[2]
#unique_id = '@perfumexlab'
#token = 'QRmlgL6hLf5oBBWxHrEJ9RtndZQMpOcppePlzWF069H'

# TiktokLiveClient
from TikTokLive import TikTokLiveClient
from TikTokLive.types.events import CommentEvent, ConnectEvent, DisconnectEvent, LiveEndEvent, UnknownEvent

#GTTS Speech
from gtts import gTTS
import time
import datetime
#Line Notify
import requests
url = 'https://notify-api.line.me/api/notify'
#token = 'NIcr2QFJ1eJCfuELDLZQzJpYF5E3mdt8x3Baho2qRGu' Test
#headers = {'content-type':'application/x-www-form-urlencoded','Authorization':'Bearer '+token}


room_create_time = -1
#Tiktok Account
unique_id = "@perfumexlab"

client: TikTokLiveClient = TikTokLiveClient(unique_id)

def notify():
    print('')


@client.on("connect")
async def on_connect(_: ConnectEvent):
    #print(client.room_info['create_time'])
    create_time_epoch = client.room_info['create_time']
    
    t = time.ctime(create_time_epoch)

    room_create_time = time.strftime('%H:%M:%S', t)
    print("room_create_time", room_create_time)
    print('['+time.strftime('%H:%M')+']['+unique_id+'] '+ "is on live")#, room_create_time)
    #message = unique_id + 'is on live'# + room_create_time
    message = unique_id + ' on air | started at ' + room_create_time
    print(message)

    #r = requests.post(url, headers=headers, data = {'message':message})
    #tts = gTTS("สวัสดีค่า", lang='th')
    #filename = str(int(time.time()))
    #tts.save('comment\\'+filename+'.mp3')

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
    #r = requests.post(url, headers=headers, data = {'message': unique_id + ' disconnected'})

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

