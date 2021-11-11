from pygame.display import Info
import engine.handle_input
from engine.unlocks import return_css_selector
from engine.popup_event import clear_pop_up_events, get_pop_up_events
from engine.game_handler import set_timer

p1_selector_position = [4, 2, 0, 0] #0 is unselected, 1 is selected, 2 is confirmed... 0 is human, 1 is cpu
p2_selector_position = [4, 2, 0, 0] #0 is unselected, 1 is selected, 2 is confirmed... 0 is human, 1 is cpu
p1_blob = "quirkless"
p2_blob = "quirkless"

blob_list = return_css_selector()

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
def css_handler():
    global p1_selector_position
    global p2_selector_position
    global p1_blob
    global p2_blob
    global p1_timer
    global p2_timer
    game_state = "css"
    p1_selector_position, p1_timer, p2_selector_position = css_navigation(1, p1_selector_position, p1_timer, p2_selector_position)
    p2_selector_position, p2_timer, p1_selector_position = css_navigation(2, p2_selector_position, p2_timer, p1_selector_position)
    
    if(p1_selector_position[2] == 1):
        if(p1_selector_position[0] == 0):
            if(p1_selector_position[1] == 0):
                game_state = "main_menu"
                p1_selector_position = [4, 2, 0, 0]
                p2_selector_position = [4, 2, 0, 0]
            elif(p1_selector_position[1] == 1):
                game_state = "rules"
                p1_selector_position[2] = 0
                p2_selector_position[2] = 0
            elif(p1_selector_position[1] == 2):
                game_state = "settings"
                p1_selector_position[2] = 0
                p2_selector_position[2] = 0
            elif(p1_selector_position[1] == 3):
                game_state = "almanac"
                p1_selector_position[2] = 0
                p2_selector_position[2] = 0
            elif(p1_selector_position[1] == 4):
                p1_selector_position[2] = 0
                p1_selector_position[3] = not p1_selector_position[3]

        else:
            #TODO: Fix this spaghetti
            p1_blob = blob_list[p1_selector_position[1]][p1_selector_position[0]]
    
    if(p2_selector_position[2] == 1):
        if(p2_selector_position[0] == 0):
            if(p2_selector_position[1] == 0):
                game_state = "main_menu"
                p1_selector_position = [4, 2, 0, 0]
                p2_selector_position = [4, 2, 0, 0]
            elif(p2_selector_position[1] == 1):
                game_state = "rules"
                p1_selector_position[2] = 0
                p2_selector_position[2] = 0
            elif(p2_selector_position[1] == 2):
                game_state = "settings"
                p1_selector_position[2] = 0
                p2_selector_position[2] = 0
            elif(p2_selector_position[1] == 3):
                game_state = "almanac"
                p1_selector_position[2] = 0
                p2_selector_position[2] = 0
            elif(p2_selector_position[1] == 4):
                p2_selector_position[2] = 0
                p2_selector_position[3] = not p2_selector_position[3]
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

pop_up_counter = 0
def popup_handler(timer):
    global pop_up_counter
    game_state = "pop_up"
    if(pop_up_counter >= len(get_pop_up_events())):
        pop_up_counter = 0
        last_info = get_pop_up_events()[-1].info
        clear_pop_up_events()
        return "css", last_info
    
    pop_up = get_pop_up_events()[pop_up_counter].info
    
    pressed = engine.handle_input.get_keypress()

    if("p1_ability" in pressed or "p2_ability" in pressed or "return" in pressed) and timer <= 0:
        pop_up_counter += 1
        set_timer(30)

    return game_state, pop_up