import sys
print(sys.argv[1])

text = sys.argv[1]

from gtts import gTTS
from io import BytesIO
    # Initialize gTTS with the text to convert

mp3_fp = BytesIO()
tts = gTTS(text, lang='th')
tts.save('speech.mp3')

import time
import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
from pygame import mixer

mixer.init()
mixer.music.load("speech.mp3")
mixer.music.play()
while mixer.music.get_busy():  # wait for music to finish playing
    time.sleep(0.5)