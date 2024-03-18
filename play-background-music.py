import pygame
import os
import time
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"

music_path = 'music'
filename = 'kpop.ogg'
pygame.mixer.init()
pygame.mixer.music.load(os.path.join(music_path, filename))
pygame.mixer.music.set_volume(0.05)
pygame.mixer.music.play(loops=-1)
print('['+time.strftime('%H:%M')+'][Background] : playing ' + filename)

while(True):
    time.sleep(1)