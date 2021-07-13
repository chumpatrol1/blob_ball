import pygame as pg
import sys
import engine.handle_input

pg.init()
clock = pg.time.Clock()
clock.tick(60)

selector_position = 0
p1_selector_position = [4, 2, 0] #0 is unselected, 1 is selected, 2 is confirmed
p2_selector_position = [4, 2, 0] #0 is unselected, 1 is selected, 2 is confirmed
p1_blob = "quirkless"
p2_blob = "quirkless"

def menu_navigation(timer):
    game_state = "main_menu"
    pressed = engine.handle_input.menu_input()
    global selector_position
    if('p1_up' in pressed or 'p2_up' in pressed):
        if selector_position == 0:
            selector_position = 6
        else:
            selector_position -= 1
    elif('p1_down' in pressed or 'p2_down' in pressed):
        if selector_position == 6:
            selector_position = 0
        else:
            selector_position += 1
    if(not timer) and('p1_ability' in pressed or 'p2_ability' in pressed):
        if(selector_position == 0): #Casual
            game_state = "casual_css"
            print(game_state)
        elif(selector_position == 1):
            #game_state = "competitive_css"
            game_state = "casual_css"
        elif(selector_position == 2):
            selector_position = 0
        elif(selector_position == 3):
            #game_state = "almanac"
            game_state = "casual_css"
        elif(selector_position == 4):
            selector_position = 0
            game_state = "rules"
        elif(selector_position == 5):
            #game_state = "settings"
            game_state = "casual_css"
        elif(selector_position == 6): #Quits the game
            print("QUIT")
            pg.quit()
            sys.exit()
            
        print("Selected position {}!".format(selector_position))
    return selector_position, game_state

blob_list = [
    ["back", "quirkless", "fire", "ice", "quirkless", "quirkless", "quirkless", "quirkless",],
    ["back", "quirkless", "quirkless", "quirkless", "quirkless", "quirkless", "quirkless", "quirkless",],
    ["back", "quirkless", "quirkless", "quirkless", "quirkless", "quirkless", "quirkless", "quirkless",],
    ["back", "quirkless", "quirkless", "quirkless", "quirkless", "quirkless", "quirkless", "quirkless",],
    ["back", "quirkless", "quirkless", "quirkless", "quirkless", "quirkless", "quirkless", "quirkless",],
]

def css_navigation(player, selector, timer, other_selector):
    pressed_conversions = engine.handle_input.player_to_controls(player)
    pressed_buttons = engine.handle_input.css_input()
    pressed = []
    for button in pressed_buttons:
        if(button in pressed_conversions):
            pressed.append(pressed_conversions[button])
        
    if pressed == []:
        timer = 0

    if not timer == 0:
        pressed = []
        
    if not (pressed == []):
        if('ability' in pressed):
            timer = 15
        else:
            timer = 30
    
    
    if(selector[2] == 0):
        if('up' in pressed):
            if selector[1] == 0:
                selector[1] = 4
                
            else:
                selector[1] -= 1
        elif('down' in pressed):
            if selector[1] == 4:
                selector[1] = 0
            else:
                selector[1] += 1
        if('left' in pressed):
            if selector[0] == 0:
                selector[0] = 7
            else:
                selector[0] -= 1
        elif('right' in pressed):
            if selector[0] == 7:
                selector[0] = 0
            else:
                selector[0] += 1
    
    if(selector[2] == 0):
        if('ability' in pressed):
            selector[2] = 1
    elif('kick' in pressed):
        selector[2] = 0
        if(other_selector[2] == 2):
            #Deconfirms the other player's selection if the other player has confirmed
            other_selector[2] = 1
    elif(selector[2] >= 1 and other_selector[2] >= 1):
        if('ability' in pressed):
            selector[2] = 2

    return selector, timer, other_selector
    
p1_timer = 0
p2_timer = 0
def casual_css_navigation():
    global p1_selector_position
    global p2_selector_position
    global p1_blob
    global p2_blob
    global p1_timer
    global p2_timer
    game_state = "casual_css"
    p1_selector_position, p1_timer, p2_selector_position = css_navigation(1, p1_selector_position, p1_timer, p2_selector_position)
    p2_selector_position, p2_timer, p1_selector_position = css_navigation(2, p2_selector_position, p2_timer, p1_selector_position)
    
    if(p1_selector_position[2] == 1):
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
        else:
            #TODO: Fix this spaghetti
            p1_blob = blob_list[p1_selector_position[1]][p1_selector_position[0]]
    
    if(p2_selector_position[2] == 1):
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
        else:
            #TODO: Fix this spaghetti
            p2_blob = blob_list[p2_selector_position[1]][p2_selector_position[0]]

    if(p1_selector_position[2] == 2 and p2_selector_position[2] == 2):
        print("Casual Match Started!")
        game_state = "casual_match"
    
    if(game_state == "casual_match"):
        p1_selector_position[2] = 0 #0 is unselected, 1 is selected, 2 is confirmed
        p2_selector_position[2] = 0 #0 is unselected, 1 is selected, 2 is confirmed

    if(p1_timer > 0):
        p1_timer -= 1
    if(p2_timer > 0):
        p2_timer -= 1
    return p1_selector_position, p2_selector_position, game_state, p1_blob, p2_blob

def rules_navigation(timer, ruleset):
    game_state = "rules"
    pressed = engine.handle_input.menu_input()
    global selector_position
    if('p1_up' in pressed or 'p2_up' in pressed):
        if selector_position == 0:
            selector_position = 3
        else:
            selector_position -= 1
    elif('p1_down' in pressed or 'p2_down' in pressed):
        if selector_position == 3:
            selector_position = 0
        else:
            selector_position += 1
    if('p1_left' in pressed or 'p2_left' in pressed):
        if(selector_position == 0):
            if(ruleset['goal_limit'] > 1):
                ruleset['goal_limit'] -= 1
            else:
                ruleset['goal_limit'] = 25
        elif(selector_position == 1):
            if(ruleset['time_limit'] > 0):
                ruleset['time_limit'] -= 600
            else:
                ruleset['time_limit'] = 36000
        elif(selector_position == 2):
            if(ruleset['time_bonus'] > 0):
                ruleset['time_bonus'] -= 300
            else:
                ruleset['time_bonus'] = 3600
    elif('p1_right' in pressed or 'p2_right' in pressed):
        if(selector_position == 0):
            if(ruleset['goal_limit'] < 25):
                ruleset['goal_limit'] += 1
            else:
                ruleset['goal_limit'] = 1
        elif(selector_position == 1):
            if(ruleset['time_limit'] < 36000):
                ruleset['time_limit'] += 600
            else:
                ruleset['time_limit'] = 0
        elif(selector_position == 2):
            if(ruleset['time_bonus'] < 3600):
                ruleset['time_bonus'] += 300
            else:
                ruleset['time_bonus'] = 0

    if(not timer) and('p1_ability' in pressed or 'p2_ability' in pressed):
        if(selector_position == 3): #Casual
            selector_position = 4
            game_state = "main_menu"
            
        print("Selected position {}!".format(selector_position))
    return selector_position, game_state
