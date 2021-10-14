from os import getcwd
cwd = getcwd()
cwd = cwd + "/resources/sounds/sfx/"
sound_events = []
name_to_file = {
    "select": "select.wav",
}

name_to_channel = {
    "select": 1,
}

def convert_name_to_file(name):
    file = ""
    if name in name_to_file:
        file = cwd + name_to_file[name]
    return file

def convert_name_to_channel(name):
    return name_to_channel[name]

class SFXEvent():
    def __init__(self, name = None):
        self.name = name
        self._sound_file = convert_name_to_file(name)
        self._channel = convert_name_to_channel(name)

    def return_file(self):
        return self._sound_file

    def return_channel(self):
        return self._channel

    def __str__(self):
        return f"SFX Name: {self.name}\nSFX File: {self.return_file()}"

def createSFXEvent(name):
    global sound_events
    sound_events.append(SFXEvent(name = name))

def clear_sound_events():
    global sound_events
    sound_events = []

def get_sound_events():
    global sound_events
    return sound_events