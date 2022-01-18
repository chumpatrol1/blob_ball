import pygame as pg

current_events = []
def update_events(): # DO NOT USE THIS. EVER. EXCEPT FOR MAIN LOOP
    global current_events
    current_events = pg.event.get()
    return current_events

def get_events():
    global current_events
    return current_events