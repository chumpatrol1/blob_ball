import pygame as pg
from resources.sound_engine.handle_bgm import load_bgm
from resources.sound_engine.sfx_event import get_sound_events, clear_sound_events
from time import time
pg.init()
pg.mixer.init()
pg.mixer.set_num_channels(10)

saved_song = ""
bgm = None
bgm_timer = 0
bgm_class = None
start_time = 0
elapsed_time = 0

# TODO: Make handle_bgm.py actually play the music? At least move this to a separate function

def play_bgm(song_playing, settings):
    global saved_song
    global bgm_timer
    global start_time
    global bgm_class
    # Play BGM
    # Play SFX
    pg.mixer.music.set_volume(settings['music_volume']/10)
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

def play_sfx(settings):
    for sound_event in get_sound_events():
        print(sound_event)
        sound = pg.mixer.Sound(sound_event.return_file())
        sound.set_volume(settings['sound_volume']/10)
        pg.mixer.Channel(sound_event.return_channel()).play(sound)
    clear_sound_events()    

def handle_sound(song_playing, settings):
    play_bgm(song_playing, settings)
    play_sfx(settings)