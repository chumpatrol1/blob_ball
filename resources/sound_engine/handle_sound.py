import pygame as pg
from pygame.constants import BLEND_RGBA_MULT
from resources.sound_engine.handle_bgm import load_bgm, get_bgm_duration
pg.init()
pg.mixer.init()
print("PYGAME SOUND:", pg.mixer.get_init())

saved_song = ""
bgm = None
bgm_timer = 0

def handle_sound(song_playing):
    global saved_song
    global bgm_timer
    # Play BGM
    # Play SFX
    if(song_playing != saved_song) or not bgm_timer:
        saved_song = song_playing
        pg.mixer.music.load(load_bgm(song_playing))
    if not bgm_timer:
        pg.mixer.music.play(-1)
        bgm_timer = get_bgm_duration(song_playing)
    else:
        bgm_timer -= 1