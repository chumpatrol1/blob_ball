from pygame.display import Info
import engine.handle_input
from engine.unlocks import load_blob_unlocks, return_blob_unlocks, return_css_selector_blobs, update_css_blobs, return_available_costumes
from engine.popup_event import clear_pop_up_events, get_pop_up_events
from engine.game_handler import set_timer
from resources.graphics_engine.display_almanac import load_almanac_static_text, unload_almanac_static_text
from resources.graphics_engine.display_css import force_load_blobs
from resources.sound_engine.sfx_event import createSFXEvent
from engine.button import Button

p1_css_menu_buttons = [
]
p2_css_menu_buttons = [
]
for i in range(8): # 8 columns
    for j in range(5): # 5 rows
        p1_css_menu_buttons.append(Button(50+100*j, 150+100*j, 136 + i*136, 204 + i*136)) # Left half of slot is for P1
        p2_css_menu_buttons.append(Button(50+100*j, 150+100*j, 204 + i*136, 272 + i*136)) # Right half of slot is for P2
        


# X position, Y position, Confirmation, CPU/Human
p1_selector_position = [4, 2, 0, 0, 0] #x... y... 0 is unselected, 1 is selected, 2 is confirmed... 0 is human, 1 is cpu... 0 is default, 1 is grayscale, 2+ are custom
p2_selector_position = [4, 2, 0, 0, 0] #x... y... 0 is unselected, 1 is selected, 2 is confirmed... 0 is human, 1 is cpu... 0 is default, 1 is grayscale, 2+ are custom
p1_ghost_position = None
p2_ghost_position = None
p1_blob = "quirkless"
p2_blob = "quirkless"

blob_list = return_css_selector_blobs()

def css_navigation(player, selector, timer, other_selector, ghost_selector, other_ghost):
    pressed_conversions = engine.handle_input.player_to_controls(player)
    detect_new_controllers = True
    if(player == 2):
        detect_new_controllers = False
    pressed_buttons = engine.handle_input.css_input(detect_new_controllers = detect_new_controllers)
    if(player == 1):
        mouse = engine.handle_input.handle_mouse(False)
        cur_blob = p1_blob
    else:
        mouse = engine.handle_input.handle_mouse()
        cur_blob = p2_blob

    pressed = []
    override = {'return', 'escape'}
    for button in pressed_buttons:
        if(button in pressed_conversions):
            pressed.append(pressed_conversions[button])
        elif(button in override):
            pressed.append(button)
    if pressed == []:
        timer = 0

    if not timer == 0:
        pressed = []
        
    if not (pressed == []):
        if('ability' in pressed or 'escape' in pressed):
            timer = 15
        else:
            timer = 30
    
    
    if(selector[2] == 0):
        if('up' in pressed):
            selector[4] = 0
            if selector[1] == 0:
                selector[1] = 4
            else:
                selector[1] -= 1
            
        elif('down' in pressed):
            selector[4] = 0
            if selector[1] == 4:
                selector[1] = 0
            else:
                selector[1] += 1
        if('left' in pressed):
            selector[4] = 0
            if selector[0] == 0:
                selector[0] = 7
            else:
                selector[0] -= 1
        elif('right' in pressed):
            selector[4] = 0
            if selector[0] == 7:
                selector[0] = 0
            else:
                selector[0] += 1

    if('block' in pressed and selector[0] > 0 and not (cur_blob == 'quirkless' and selector[0] != 0 and selector[1] != 0)):
        selector[4] += 1
        costumes = return_available_costumes()
        if(selector[4] >= len(costumes[cur_blob])):
            selector[4] = 0
    
    if('return' in pressed):
        print("return pressed")

    if(selector[2] == 0):
        if('ability' in pressed):
            selector[2] = 1
            ghost_selector = None
        elif('escape' in pressed):
            if(other_selector[2] == 0 and selector[3] == 0):
                other_selector[2] = 2
                other_selector[3] = 1

    elif('kick' in pressed):
        selector[2] = 0
        if(other_selector[2] == 2):
            #Deconfirms the other player's selection if the other player has confirmed
            other_selector[2] = 1
    elif(selector[2] >= 1 and other_selector[2] >= 1):
        if('ability' in pressed):
            selector[2] = 2
            ghost_selector = None
        elif('return' in pressed or 'escape' in pressed):
            selector[2] = 2
            other_selector[2] = 2
            ghost_selector = None
    elif(selector[2] >= 1 and other_selector[2] == 0):
        if('escape' in pressed and selector[3] == 0):
            selector[2] = 2
            other_selector[2] = 2
            other_selector[3] = 1
            ghost_selector = None


    if(player == 1):
        css_menu_buttons = p1_css_menu_buttons
    else:
        css_menu_buttons = p2_css_menu_buttons

    for i in range(len(css_menu_buttons)):
        if(css_menu_buttons[i].check_hover(mouse)):
            if(mouse[2] or mouse[1][0] or mouse[1][2]) and selector[2] == 0: # Did we move the mouse? 
                ghost_selector = [i//5, i%5] # Change the selector position

            if(mouse[1][0]):
                # Functionality:
                # both unselected: set to select
                # me select, other unselect: nothing
                # me unselect, other select: set to select
                # both select: both confirm
                if(selector[2] >= 1 and other_selector[2] >= 1):
                    selector[2] = 2
                    other_selector[2] = 2
                    ghost_selector = None
                    other_ghost = None
                elif(not selector[2]):
                    selector[0] = i//5
                    selector[1] = i%5
                    selector[2] = 1
                    ghost_selector = None
                
            elif(mouse[1][2]):
                selector[2] = 0
                other_selector[2] = 0
                ghost_selector = None
                other_ghost = None
                
    return selector, timer, other_selector, ghost_selector, other_ghost
    
p1_timer = 0
p2_timer = 0
def css_handler():
    global p1_selector_position
    global p2_selector_position
    global p1_ghost_position
    global p2_ghost_position
    global p1_blob
    global p2_blob
    global p1_timer
    global p2_timer
    game_state = "css"
    # Controller failure - cannot swap players here
    p1_selector_position, p1_timer, p2_selector_position, p1_ghost_position, p2_ghost_position = css_navigation(1, p1_selector_position, p1_timer, p2_selector_position, p1_ghost_position, p2_ghost_position)
    p2_selector_position, p2_timer, p1_selector_position, p2_ghost_position, p1_ghost_position = css_navigation(2, p2_selector_position, p2_timer, p1_selector_position, p2_ghost_position, p1_ghost_position)
    
    if(p1_selector_position[2] == 1):
        if(p1_selector_position[0] == 0):
            unload_almanac_static_text()
            if(p1_selector_position[1] == 0):
                game_state = "main_menu"
                p1_selector_position = [4, 2, 0, 0, 0]
                p2_selector_position = [4, 2, 0, 0, 0]
                p1_ghost_position = None
                p2_ghost_position = None
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
                load_almanac_static_text()
                p1_selector_position[2] = 0
                p2_selector_position[2] = 0
            elif(p1_selector_position[1] == 4):
                p1_selector_position[2] = 0
                p1_selector_position[3] = not p1_selector_position[3]
    
    if(p1_selector_position[0] > 0):
        p1_blob = blob_list[p1_selector_position[1]][p1_selector_position[0]]
    
    if(p2_selector_position[2] == 1):
        if(p2_selector_position[0] == 0):
            if(p2_selector_position[1] == 0):
                game_state = "main_menu"
                p1_selector_position = [4, 2, 0, 0, 0]
                p2_selector_position = [4, 2, 0, 0, 0]
                p1_ghost_position = None
                p2_ghost_position = None
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
                load_almanac_static_text()
                p1_selector_position[2] = 0
                p2_selector_position[2] = 0
            elif(p2_selector_position[1] == 4):
                p2_selector_position[2] = 0
                p2_selector_position[3] = not p2_selector_position[3]

            #TODO: Fix this spaghetti
    
    if(p2_selector_position[0] > 0):
        p2_blob = blob_list[p2_selector_position[1]][p2_selector_position[0]]

    if(p1_selector_position[2] == 2 and p2_selector_position[2] == 2):
        game_state = "casual_match"
        p1_selector_position[2] = 0 #0 is unselected, 1 is selected, 2 is confirmed
        p2_selector_position[2] = 0 #0 is unselected, 1 is selected, 2 is confirmed
        p1_ghost_position = None
        p2_ghost_position = None

    if(p1_timer > 0):
        p1_timer -= 1
    if(p2_timer > 0):
        p2_timer -= 1

    return game_state, [p1_selector_position, p2_selector_position, p1_blob, p2_blob, p1_ghost_position, p2_ghost_position]

pop_up_counter = 0
def popup_handler(timer):
    global pop_up_counter
    global blob_list
    game_state = "pop_up"
    if(pop_up_counter >= len(get_pop_up_events())):
        pop_up_counter = 0
        last_info = get_pop_up_events()[-1].info
        clear_pop_up_events()
        blob_list = return_css_selector_blobs()
        return "css", last_info
    
    pop_up = get_pop_up_events()[pop_up_counter].info
    
    pressed = engine.handle_input.get_keypress()
    mouse = engine.handle_input.handle_mouse()

    if("p1_ability" in pressed or "p2_ability" in pressed or "return" in pressed or mouse[1][0] or mouse[1][2]) and timer <= 0:
        pop_up_counter += 1
        set_timer(60)
        if(pop_up_counter < len(get_pop_up_events())):
            createSFXEvent("chime_milestone")

    return game_state, pop_up