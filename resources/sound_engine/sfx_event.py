from os import getcwd
from random import randint
cwd = getcwd()
cwd = cwd + "/resources/sounds/sfx/"
sound_events = []
name_to_file = {
    "select": ["select.wav"],
    "kick": ["kick.wav"],
    "block": ["block.wav"],
    "boost": ["boost.wav"],
    "parry": ["parry.wav"],
    "clank": ["clank.wav"],
    "hit": ["hit.wav"],
    "ball_grass_bounce": ['ball_grass_bounce_1.wav', 'ball_grass_bounce_2.wav', 'ball_grass_bounce_3.wav'],
    "ball_blob_bounce": ['ball_blob_bounce_1.wav', 'ball_blob_bounce_2.wav'],
    "ball_metal_bounce": ['ball_metal_bounce_1.wav', 'ball_metal_bounce_2.wav', 'ball_metal_bounce_3.wav'],
    "chime_progress": ['chime_progress.wav'],
    "chime_completion": ['chime_completion.wav'],
    "chime_error": ['chime_error.wav'],
    'fire': ['fire_1.wav', 'fire_2.wav', 'fire_3.wav'],
    'ice': ['ice_1.wav', 'ice_2.wav'],
    'water': ['water_1.wav', 'water_2.wav', 'water_3.wav'],
    'gale': ['gale.wav'],
	'goal': ['goal.wav'],
    'ball_spire_hit': ['ball_spire_hit.wav'],
    'wavebounce': ['wavebounce.wav'],	
}

def convert_name_to_file(name):
    file = ""
    if name in name_to_file:
        sfx_array = name_to_file[name]
        random_track = randint(0, len(sfx_array) - 1)
        file = sfx_array[random_track]
    
    file = cwd + file
    return file

class SFXEvent():
    def __init__(self, name = None, volume_modifier = 1):
        self.name = name
        self._sound_file = convert_name_to_file(name)
        self._volume_modifier = volume_modifier

    def return_file(self):
        return self._sound_file

    def return_volume_modifier(self):
        return self._volume_modifier

    def __str__(self):
        return f"SFX Name: {self.name}\nSFX File: {self.return_file()}"

def createSFXEvent(name, volume_modifier = 1):
    global sound_events
    sound_events.append(SFXEvent(name = name, volume_modifier = volume_modifier))

def clear_sound_events():
    global sound_events
    sound_events = []

def get_sound_events():
    global sound_events
    return sound_events