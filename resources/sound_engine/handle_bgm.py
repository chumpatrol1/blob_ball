from os import getcwd
from random import randint
cwd = getcwd() + '/resources/sounds/bgm/'
# TODO: Add more songs for tests
# TODO: Make documentation

class bgm:
    def __init__(self, track_file = "Blob_Ball_Main_Theme.wav", track_name = "Blob Ball Main Theme", track_number = 1, track_duration = 133.5, restart_point = 10, volume_modifier = 1):
        self.track_file = cwd + track_file
        self.track_name = track_name
        self.track_number = track_number
        self.track_duration = track_duration
        self.restart_point = restart_point
        self.volume_modifier = volume_modifier

    def __str__(self):
        return "Track Name (Number): ({}) {}, Track Duration: {}, Restart Point: {}".format(self.track_number, self.track_name, self.track_duration, self.restart_point)

bgm_list = {
    "bb_main_theme": [bgm(track_file="Blob_Ball_Main_Theme.wav", track_name = "Blob Ball Main Theme", track_number=1, track_duration=133.5, restart_point=10, volume_modifier=1)],
    "bb_win_theme": [bgm(track_file="Blob_Ball_Win_Theme.wav", track_name = "Blob Ball Win Theme", track_number=2, track_duration=4, restart_point=None, volume_modifier=0.5)]
}

def load_bgm(song_playing):
    track_array = bgm_list[song_playing]
    random_track = randint(0, len(track_array) - 1)
    return track_array[random_track]
