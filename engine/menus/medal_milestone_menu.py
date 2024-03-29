from pygame.display import Info
import engine.handle_input
from engine.unlocks import load_medal_unlocks, return_medal_unlocks, return_mam_selector_medals, update_mam_medals
from engine.unlock_event import clear_unlock_events, get_unlock_events
from engine.game_handler import set_timer
from resources.graphics_engine.display_almanac import load_almanac_static_text, unload_almanac_static_text
from resources.graphics_engine.display_medals_and_milestones import force_load_medals
from resources.sound_engine.sfx_event import createSFXEvent
from engine.button import Button

medal_menu_buttons = [
]
for i in range(8): # 8 columns
    for j in range(5): # 5 rows
        medal_menu_buttons.append(Button(50+100*j, 150+100*j, 136 + i*136, 204 + i*136)) # Left half of slot is for P1
        



# X position, Y position, Confirmation, CPU/Human
medal_selector = [4, 2, 0] #0 is unselected, 1 is selected, 2 is confirmed... 0 is human, 1 is cpu
ghost_position = None
medal = "goal"

medal_list = return_mam_selector_medals()

def medal_navigation(timer):
    global medal_selector
    global ghost_selector
    ghost_selector = None
    pressed_conversions = engine.handle_input.merge_inputs(engine.handle_input.get_keypress())
    pressed_buttons = engine.handle_input.css_input()
    
    mouse = engine.handle_input.handle_mouse()
    game_state = "medals"

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
    
    
    if(medal_selector[2] == 0):
        if('up' in pressed):
            if medal_selector[1] == 0:
                medal_selector[1] = 4
                
            else:
                medal_selector[1] -= 1
        elif('down' in pressed):
            if medal_selector[1] == 4:
                medal_selector[1] = 0
            else:
                medal_selector[1] += 1
        if('left' in pressed):
            if medal_selector[0] == 0:
                medal_selector[0] = 7
            else:
                medal_selector[0] -= 1
        elif('right' in pressed):
            if medal_selector[0] == 7:
                medal_selector[0] = 0
            else:
                medal_selector[0] += 1

    mam_menu_buttons = medal_menu_buttons

    for i in range(len(mam_menu_buttons)):
        if(mam_menu_buttons[i].check_hover(mouse)):
            if(mouse[2] or mouse[1][0] or mouse[1][2]) and medal_selector[2] == 0: # Did we move the mouse? 
                ghost_selector = [i//5, i%5] # Change the selector position

            if(mouse[1][0]):
                # Functionality:
                # both unselected: set to select
                # me select, other unselect: nothing
                # me unselect, other select: set to select
                # both select: both confirm
                if(medal_selector[2] >= 1):
                    medal_selector[2] = 2
                    ghost_selector = None
                elif(not medal_selector[2]):
                    medal_selector[0] = i//5
                    medal_selector[1] = i%5
                    medal_selector[2] = 1
                    ghost_selector = None
                
            elif(mouse[1][2]):
                medal_selector[2] = 0
                ghost_selector = None
                
    return game_state, [medal_selector, ghost_selector]
    
timer = 0
def mam_handler():
    global medal_selector
    global ghost_position
    global medal
    global timer
    game_state = "medals"
    medal_selector, timer, ghost_position = medal_navigation(1, medal_selector, timer, ghost_position)
    
    if(medal_selector[2] == 1):
        if(medal_selector[0] == 0):
            unload_almanac_static_text()
            if(medal_selector[1] == 0):
                game_state = "main_menu"
                medal_selector = [4, 2, 0]
                ghost_position = None
            elif(medal_selector[1] == 1):
                game_state = "almanac"
                medal_selector[2] = 0
            elif(medal_selector[1] == 2):
                game_state = "modifier"
                medal_selector[2] = 0
            elif(medal_selector[1] == 3):
                game_state = "almanac"
                load_almanac_static_text()
                medal_selector[2] = 0
        else:
            #TODO: Fix this spaghetti
            medal = medal_list[medal_selector[1]][medal_selector[0]]

    if(timer > 0):
        timer -= 1

    return game_state, [medal_selector, medal, ghost_position]

pop_up_counter = 0
def popup_handler(timer):
    global pop_up_counter
    global medal_list
    game_state = "pop_up"
    if(pop_up_counter >= len(get_unlock_events())):
        pop_up_counter = 0
        last_info = get_unlock_events()[-1].info
        clear_unlock_events()
        medal_list = return_mam_selector_medals()
        return "mam", last_info
    
    pop_up = get_unlock_events()[pop_up_counter].info
    
    pressed = engine.handle_input.get_keypress()
    mouse = engine.handle_input.handle_mouse()

    if("p1_ability" in pressed or "p2_ability" in pressed or "return" in pressed or mouse[1][0] or mouse[1][2]) and timer <= 0:
        pop_up_counter += 1
        set_timer(60)
        if(pop_up_counter < len(get_unlock_events())):
            createSFXEvent("chime_milestone")

    return game_state, pop_up