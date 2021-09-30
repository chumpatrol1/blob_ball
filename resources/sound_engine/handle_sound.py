import pygame as pg
from resources.sound_engine.handle_bgm import load_bgm
from time import time
pg.init()
pg.mixer.init()
print("PYGAME SOUND:", pg.mixer.get_init())

saved_song = ""
bgm = None
bgm_timer = 0
bgm_class = None
start_time = 0
elapsed_time = 0

# TODO: Make handle_bgm.py actually play the music? At least move this to a separate function

def handle_sound(song_playing):
    global saved_song
    global bgm_timer
    global start_time
    global bgm_class

    # Play BGM
    # Play SFX
    if(song_playing != saved_song) or not bgm_timer:
        saved_song = song_playing
        bgm_class = load_bgm(song_playing)
        bgm_timer = bgm_class.track_duration
        start_time = time()
        pg.mixer.music.load(bgm_class.track_file)
        pg.mixer.music.play(-1)
    elapsed_time = time() - start_time

    if elapsed_time >= bgm_timer:
        start_time = time()
        try:
            pg.mixer.music.play(-1, start = bgm_class.restart_point)
        except pg.error as message:
            print("handle_sound.py error:", message)
            pg.mixer.music.play(-1)