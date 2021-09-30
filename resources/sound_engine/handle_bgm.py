from os import getcwd
cwd = getcwd()

bgm_list = {
    "bb_main_theme": cwd + "/resources/sounds/bgm/Blob_Ball_Main_Theme.wav"
}

bgm_duration = { # How many frames does this song last before looping?
    "bb_main_theme": 7500
}

def load_bgm(song_playing):
    return bgm_list[song_playing]

def get_bgm_duration(song_playing):
    return bgm_duration[song_playing]