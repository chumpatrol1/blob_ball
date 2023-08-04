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
    "perfect_parry": ["perfect_parry.wav"],
    "clank": ["clank.wav"],
    "hit": ["hit.wav"],
    "ball_grass_bounce": ['ball_grass_bounce_1.wav', 'ball_grass_bounce_2.wav', 'ball_grass_bounce_3.wav'],
    "ball_blob_bounce": ['ball_blob_bounce_1.wav', 'ball_blob_bounce_2.wav'],
    "ball_metal_bounce": ['ball_metal_bounce_1.wav', 'ball_metal_bounce_2.wav', 'ball_metal_bounce_3.wav'],
    "chime_progress": ['chime_progress.wav'],
    "chime_completion": ['chime_completion.wav'],
    "chime_error": ['chime_error.wav'],
    "chime_milestone": ['chime_milestone.wav'],
    'fire': ['fire_1.wav', 'fire_2.wav', 'fire_3.wav'],
    'ice': ['ice_1.wav', 'ice_2.wav'],
    'water': ['water_1.wav', 'water_2.wav', 'water_3.wav'],
    'glyph': ['glyph_1.wav'],
    'spire': ['spire_1.wav'],
    'electricity': ['spark_1.wav', 'spark_2.wav'],
    'crunch': ['crunch.wav'],
    'gale': ['gale.wav'],
    'c&d': [],
    'tax': [],
    'whistle': ['whistle_1.wav'],
    'boxing_bell': ['boxing_bell.wav'],
	'goal': ['goal.wav'],
    'ball_spire_hit': ['ball_spire_hit.wav'],
    'wavebounce': ['wavebounce.wav'],
    'wavedash': ['wavedash.wav'],
    'camera': ['camera.wav'],
    'teleport': ['teleport.wav'],
    'bubble': ['bubble.wav'],
    'pop': ['pop.wav'],
}

suppression_list = { # First number is the supression timer, second is the increment amount, third is max (before we supress)
    'boost': [0, 30, 90],
    'crunch': [0, 15, 90],
    'whistle': [0, 30, 60],
    'boxing_bell': [0, 30, 90],
    'wavebounce': [0, 15, 90],
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
    '''
    Name: String of the sound to play. May result in a randomized sound
    Volume Modifier: Default volume is 1.
    '''
    global sound_events
    if(name in suppression_list and suppression_list[name][0] >= suppression_list[name][2]):
        return
    sound_events.append(SFXEvent(name = name, volume_modifier = volume_modifier))
    if(name in suppression_list and suppression_list[name][0] < suppression_list[name][2]):
        suppression_list[name][0] += suppression_list[name][1] # Only increment if the sound is actually played

def clear_sound_events():
    global sound_events
    sound_events = []

def get_sound_events():
    global sound_events
    return sound_events

def decrement_supression():
    global suppression_list
    # This is for you, Quackus
    for annoying_sound in  suppression_list:
        suppression_list[annoying_sound][0] -= 1 if suppression_list[annoying_sound][0] > 0 else 0