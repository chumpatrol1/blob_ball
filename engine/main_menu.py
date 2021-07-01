import pygame as pg
import sys
import engine.handle_input

pg.init()
clock = pg.time.Clock()
#clock.tick(60)

selector_position = 0
p1_selector_position = [4, 2, 0] #0 is unselected, 1 is selected, 2 is confirmed
p2_selector_position = [4, 2, 0] #0 is unselected, 1 is selected, 2 is confirmed
p1_blob = "quirkless"
p2_blob = "quirkless"

def menu_navigation():
    game_state = "main_menu"
    pressed = engine.handle_input.menu_input()
    global selector_position
    if('p1_up' in pressed or 'p2_up' in pressed):
        if selector_position == 0:
            selector_position = 6
            button_timer = 1
        else:
            selector_position -= 1
            button_timer = 1
    elif('p1_down' in pressed or 'p2_down' in pressed):
        if selector_position == 6:
            selector_position = 0
            button_timer = 1
        else:
            selector_position += 1
            button_timer = 1
    if('p1_ability' in pressed or 'p2_ability' in pressed):
        if(selector_position == 0): #Casual
            game_state = "casual_css"
            print(game_state)
        elif(selector_position == 1):
            game_state = "competitive_css"
        elif(selector_position == 2):
            selector_position = 0
        elif(selector_position == 3):
            game_state = "almanac"
        elif(selector_position == 4):
            game_state = "rules"
        elif(selector_position == 5):
            game_state = "settings"
        elif(selector_position == 6): #Quits the game
            print("QUIT")
            pg.quit()
            sys.exit()
            
        print("Selected position {}!".format(selector_position))
    return selector_position, game_state

def casual_css_navigation():
    pressed = engine.handle_input.css_input()
    global p1_selector_position
    global p2_selector_position
    global p1_blob
    global p2_blob
    game_state = "casual_css"
    if(p1_selector_position[2] == 0):
        if('p1_up' in pressed):
            if p1_selector_position[1] == 0:
                p1_selector_position[1] = 4
                
            else:
                p1_selector_position[1] -= 1
        elif('p1_down' in pressed):
            if p1_selector_position[1] == 4:
                p1_selector_position[1] = 0
            else:
                p1_selector_position[1] += 1
        if('p1_left' in pressed):
            if p1_selector_position[0] == 0:
                p1_selector_position[0] = 7
            else:
                p1_selector_position[0] -= 1
        elif('p1_right' in pressed):
            if p1_selector_position[0] == 7:
                p1_selector_position[0] = 0
            else:
                p1_selector_position[0] += 1
    if(p2_selector_position[2] == 0):
        if('p2_up' in pressed):
            if p2_selector_position[1] == 0:
                p2_selector_position[1] = 4
            else:
                p2_selector_position[1] -= 1
        elif('p2_down' in pressed):
            if p2_selector_position[1] == 4:
                p2_selector_position[1] = 0
            else:
                p2_selector_position[1] += 1
        if('p2_left' in pressed):
            if p2_selector_position[0] == 0:
                p2_selector_position[0] = 7
            else:
                p2_selector_position[0] -= 1
        elif('p2_right' in pressed):
            if p2_selector_position[0] == 7:
                p2_selector_position[0] = 0
            else:
                p2_selector_position[0] += 1

    if('p1_ability' in pressed):
        if(p1_selector_position[0] == 0):
            if(p1_selector_position[1] == 0):
                game_state = "main_menu"
                p1_selector_position = [4, 2, 0]
                p2_selector_position = [4, 2, 0]
            elif(p1_selector_position[1] == 1):
                game_state = "main_menu"
                p1_selector_position = [4, 2, 0]
                p2_selector_position = [4, 2, 0]
            elif(p1_selector_position[1] == 2):
                game_state = "main_menu"
                p1_selector_position = [4, 2, 0]
                p2_selector_position = [4, 2, 0]
            elif(p1_selector_position[1] == 3):
                game_state = "main_menu"
                p1_selector_position = [4, 2, 0]
                p2_selector_position = [4, 2, 0]
            elif(p1_selector_position[1] == 4):
                game_state = "main_menu"
                p1_selector_position = [4, 2, 0]
                p2_selector_position = [4, 2, 0]
                print("?")
        else:
            #TODO: Fix this spaghetti
            p1_blob = "quirkless"
            p1_selector_position[2] = 1
    elif('p1_kick' in pressed):
        p1_selector_position[2] = 0
    
    if('p2_ability' in pressed):
        if(p2_selector_position[0] == 0):
            if(p2_selector_position[1] == 0):
                game_state = "main_menu"
                p1_selector_position = [4, 2, 0]
                p2_selector_position = [4, 2, 0]
            elif(p2_selector_position[1] == 1):
                game_state = "main_menu"
                p1_selector_position = [4, 2, 0]
                p2_selector_position = [4, 2, 0]
            elif(p2_selector_position[1] == 2):
                game_state = "main_menu"
                p1_selector_position = [4, 2, 0]
                p2_selector_position = [4, 2, 0]
            elif(p2_selector_position[1] == 3):
                game_state = "main_menu"
                p1_selector_position = [4, 2, 0]
                p2_selector_position = [4, 2, 0]
            elif(p2_selector_position[1] == 4):
                game_state = "main_menu"
                p1_selector_position = [4, 2, 0]
                p2_selector_position = [4, 2, 0]
                print("?")
        else:
            #TODO: Fix this spaghetti
            p2_blob = "quirkless"
            p2_selector_position[2] = 1
    elif('p2_kick' in pressed):
        p2_selector_position[2] = 0

    if(p1_selector_position[2] >= 1 and p2_selector_position[2] >= 1):
        if('p1_ability' in pressed):
            p1_selector_position[2] = 2
        if('p2_ability' in pressed):
            p2_selector_position[2] = 2
    if(p1_selector_position[2] == 2 and p2_selector_position[2] == 2):
        print("Casual Match Started!")
        game_state = "casual_match"
    
    if(game_state == "casual_match"):
        p1_selector_position = [4, 2, 0] #0 is unselected, 1 is selected, 2 is confirmed
        p2_selector_position = [4, 2, 0] #0 is unselected, 1 is selected, 2 is confirmed
        p1_blob = "quirkless"
        p2_blob = "quirkless"

    return p1_selector_position, p2_selector_position, game_state, p1_blob, p2_blob
