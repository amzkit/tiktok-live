import os

os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame
import time
import random

music_path = 'music'
pygame.mixer.init()
musics = os.listdir(music_path)
random.shuffle(musics)

while(True):
    for music in musics:
        pygame.mixer.music.load(os.path.join(music_path, music))
        pygame.mixer.music.set_volume(0.04)
        pygame.mixer.music.play(loops=1)
        print('['+time.strftime('%H:%M')+'][Background] : playing ' + music)

        while pygame.mixer.music.get_busy():
            time.sleep(1)

    time.sleep(1)