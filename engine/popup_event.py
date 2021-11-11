# Handles events like achieving milestones, earning medals and unlocking things

from os import getcwd
from time import time
from engine.popup_list import find_blob_unlock
from engine.unlocks import unlock_blob

pop_up_events = []

# PopUp Types
# Blob Unlocks
# Milestones
# Aesthetic Unlocks
# Medals

def find_pop_up_list(pop_up_type):
    if(pop_up_type == 0):
        return find_blob_unlock

# Start by loading in dictionaries for each unlock type
# Compare each dictionary to something hardcoded - if it's missing a flag add it in

class PopUpEvent():
    def __init__(self, name = None, pop_up_type = None):
        # Valid pop_up_types:
        # 0 is blob unlock
        self.name = name
        self.pop_up_type = pop_up_type
        self.is_valid_pop_up = False
        self.time_notified = time()
        self.info = find_pop_up_list(self.pop_up_type)(self.name)
        self.unlock()
        self.info.append(self.pop_up_type)

    def unlock(self):
        if(self.pop_up_type == 0):
            try:
                unlock_blob(self.name, getcwd())
            except ValueError:
                raise ValueError("Already Unlocked!")

    def __str__(self):
        return f"Name: {self.name}, Type: {self.pop_up_type}, Info: {self.info}"

def createPopUpEvent(name, pop_up_type):
    global pop_up_events
    try:
        pop_up_events.append(PopUpEvent(name = name, pop_up_type = pop_up_type))
    except ValueError:
        pass
    except Exception as ex:
        print(Exception)

def clear_pop_up_events():
    global pop_up_events
    pop_up_events = []

def get_pop_up_events():
    global pop_up_events
    return pop_up_events