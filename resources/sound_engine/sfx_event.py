from os import getcwd
cwd = getcwd()
sound_events = []
name_to_file = {

}

def convert_name_to_file(name):
    file = ""
    if name in name_to_file:
        file = name_to_file[name]
    return file

class SFXEvent():
    def __init__(self, name = None):
        self.name = name
        self._sound_file = convert_name_to_file(name)

    def return_file(self):
        return self._sound_file

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