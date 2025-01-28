import pygame as pg
from os import getcwd
cwd = getcwd()
pg.font.init()
tip_font = pg.font.Font(cwd + "/resources/fonts/neuropol-x-free.regular.ttf", 30) # Load in the font
text_color = (0, 0, 255) # Set the text color to blue

# Should I put these into loops? -sunken

def return_selected_blob_tips(selected_blob):
    global tip_font
    with open(f"blobs\\{selected_blob}\\blob_tips_eng.txt", "r") as f:
        init_file = f.readlines()

    rendered_tips = []

    for line in init_file:
        rendered_tips.append(tip_font.render(line, False, text_color))

    try:
        return rendered_tips
    except:
        return []
    
