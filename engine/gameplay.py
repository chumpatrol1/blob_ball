import pygame as pg
import sys
import engine.handle_input
import engine.blobs

def initialize_players(p1_selected, p2_selected):
    p1_blob = engine.blobs.blob(p1_selected, player = 1)
    p2_blob = engine.blobs.blob(p2_selected, player = 2)
    return p1_blob, p2_blob

initialized = False
p1_blob = None
p2_blob = None

def handle_gameplay(p1_selected, p2_selected):
    pressed = engine.handle_input.gameplay_input()
    global initialized
    global p1_blob
    global p2_blob
    if not initialized:
        blobs = initialize_players(p1_selected, p2_selected)
        p1_blob = blobs[0]
        p2_blob = blobs[1]
        initialized = True
    else:
        p1_blob.move(pressed)

    game_state = "casual_match"
    return p1_blob, p2_blob, game_state