# Handles events like achieving milestones, earning medals and unlocking things

from os import getenv
from time import time
from engine.milestones import add_milestone
from engine.popup_list import find_blob_unlock, find_medal_unlock, find_costume_unlock
from engine.unlocks import unlock_blob, unlock_medal, unlock_costume

unlock_events = []

# PopUp Types
# Blob Unlocks
# Milestones
# Aesthetic Unlocks
# Medals

def find_unlock_list(unlock_type):
    if(unlock_type == 0):
        return find_blob_unlock
    elif(unlock_type == 1):
        return find_medal_unlock
    elif(unlock_type == 2):
        return find_costume_unlock

# Start by loading in dictionaries for each unlock type
# Compare each dictionary to something hardcoded - if it's missing a flag add it in

class UnlockEvent():
    def __init__(self, name = None, unlock_type = None):
        # Valid unlock_types:
        # 0 is blob unlock
        # 1 is medal unlock
        # 2 is costume unlock
        self.name = name
        self.unlock_type = unlock_type
        self.is_valid_unlock = False
        self.time_notified = time()
        self.info = find_unlock_list(self.unlock_type)(self.name)
        self.unlock()
        self.info.append(self.unlock_type)

    def unlock(self):
        if(self.unlock_type == 0):
            try:
                unlock_blob(self.name, getenv('APPDATA')+"/BlobBall")
            except ValueError:
                raise ValueError("Already Unlocked!")
        elif(self.unlock_type == 1):
            try:
                unlock_medal(self.name, getenv('APPDATA')+"/BlobBall")
            except ValueError:
                raise ValueError("Already Unlocked!")
        elif(self.unlock_type == 2):
            #print(self.name)
            try:
                unlock_costume(self.name.split("/")[0], self.name.split("/")[1], getenv('APPDATA')+"/BlobBall")
            except ValueError:
                raise ValueError("Already Unlocked!")

    def __str__(self):
        return f"Name: {self.name}, Type: {self.unlock_type}, Info: {self.info}"

def createUnlockEvent(name, unlock_type):
    global unlock_events
    try:
        unlock_events.append(UnlockEvent(name = name, unlock_type = unlock_type))
        add_milestone(getenv('APPDATA') + '/BlobBall', unlock_events[-1])
        return True
    except ValueError as ex:
        pass
    except Exception as ex:
        print(ex)

def clear_unlock_events():
    global unlock_events
    unlock_events = []

def get_unlock_events():
    global unlock_events
    return unlock_events