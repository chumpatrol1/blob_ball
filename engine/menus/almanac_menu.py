import engine.handle_input
from resources.sound_engine.sfx_event import createSFXEvent
from engine.button import Button
selector_position = 0
almanac_main_buttons = [
    Button(50, 110, 400, 950),
    Button(125, 185, 400, 950),
    Button(200, 260, 400, 950),
    Button(275, 335, 400, 950),
    Button(350, 410, 400, 950),
    Button(425, 500, 400, 950),
]
def almanac_navigation(timer, previous_screen):
    game_state = "almanac"
    pressed = engine.handle_input.menu_input()
    mouse = engine.handle_input.handle_mouse()
    global selector_position
    if('p1_up' in pressed or 'p2_up' in pressed):
        if selector_position == 0:
            selector_position = 5
        else:
            selector_position -= 1
    elif('p1_down' in pressed or 'p2_down' in pressed):
        if selector_position == 5:
            selector_position = 0
        else:
            selector_position += 1

    def update_gamestate():
        global selector_position
        createSFXEvent('select')
        if(selector_position == 0): #Blobs and Info
            game_state = "almanac"
        elif(selector_position == 1):
            #game_state = "medals"
            game_state = "almanac"
            selector_position = 1
            # Will be temporarily disabled
        elif(selector_position == 2):
            game_state = "almanac_stats"
        elif(selector_position == 3):
            selector_position = 0
            game_state = "almanac_art"
        elif(selector_position == 4):
            game_state = "credits"
        elif(selector_position == 5): #Go back
            game_state = previous_screen
            selector_position = 0
        return game_state

    if(not timer) and ('p1_ability' in pressed or 'p2_ability' in pressed or 'return' in pressed):
        game_state = update_gamestate()
            
    for i in range(len(almanac_main_buttons)):
        if(almanac_main_buttons[i].check_hover(mouse)):
            if(mouse[2] or mouse[1][0] or mouse[1][2]): # Did we move the mouse?
                selector_position = i # Change the selector position

            if(mouse[1][0] or mouse[1][2]):
                createSFXEvent('select')
                game_state = update_gamestate()
                
    return selector_position, game_state

def almanac_stats_navigation(timer):
    pressed = engine.handle_input.menu_input()
    mouse = engine.handle_input.handle_mouse()
    game_state = "almanac_stats"
    if(not timer) and ('p1_ability' in pressed or 'p2_ability' in pressed or 'return' in pressed or mouse[1][0] or mouse[1][2]):
        createSFXEvent('select')
        game_state = "almanac_stats_page_2"
    return [game_state]

def almanac_stats_navigation_2(timer):
    pressed = engine.handle_input.menu_input()
    mouse = engine.handle_input.handle_mouse()
    game_state = "almanac_stats_page_2"
    if(not timer) and ('p1_ability' in pressed or 'p2_ability' in pressed or 'return' in pressed or mouse[1][0] or mouse[1][2]):
        createSFXEvent('select')
        game_state = "almanac_stats_page_3"
        global p1_selector_position
        p1_selector_position = [3, 2, 0, 0]
    return [game_state]

almanac_mu_chart_selector = [3, 2, 0]
almanac_mu_chart_ghost = None
almanac_mu_chart_buttons = []
for i in range(7): # 7 columns
    for j in range(5): # 5 rows
        almanac_mu_chart_buttons.append(Button(25+100*j, 125+100*j, 75 + i*175, 250 + i*175)) # Left half of slot is for P1
        

def almanac_stats_navigation_3():
    global almanac_mu_chart_selector
    game_state = "almanac_stats_page_3"
    pressed = engine.handle_input.css_input()
    pressed = engine.handle_input.merge_inputs(pressed)
    mouse = engine.handle_input.handle_mouse()
    global almanac_mu_chart_ghost

    if('up' in pressed):
            if almanac_mu_chart_selector[1] == 0:
                almanac_mu_chart_selector[1] = 4
                
            else:
                almanac_mu_chart_selector[1] -= 1
    elif('down' in pressed):
            if almanac_mu_chart_selector[1] == 4:
                almanac_mu_chart_selector[1] = 0
            else:
                almanac_mu_chart_selector[1] += 1
    if('left' in pressed):
        if almanac_mu_chart_selector[0] == 0:
            almanac_mu_chart_selector[0] = 6
        else:
            almanac_mu_chart_selector[0] -= 1
    elif('right' in pressed):
        if almanac_mu_chart_selector[0] == 6:
            almanac_mu_chart_selector[0] = 0
        else:
            almanac_mu_chart_selector[0] += 1
    
    if(almanac_mu_chart_selector[2] == 0):
        if('ability' in pressed):
            if(almanac_mu_chart_selector == [3, 2, 0]):
                createSFXEvent('select')
                game_state = "almanac"
            else:
                almanac_mu_chart_selector[2] = 1
    if(almanac_mu_chart_selector[2] == 1 and 
    ('up' in pressed or 'down' in pressed or 'left' in pressed or 'right' in pressed)):
        almanac_mu_chart_selector[2] = 0
    if('kick' in pressed):
        almanac_mu_chart_selector[2] = 0

    for i in range(len(almanac_mu_chart_buttons)):
        if(almanac_mu_chart_buttons[i].check_hover(mouse)):
            if(mouse[2] or mouse[1][0] or mouse[1][2]): # Did we move the mouse?
                
                almanac_mu_chart_ghost = [i//5, i%5] # Change the selector position

            if(mouse[1][0]):
                # Functionality:
                # both unselected: set to select
                # me select, other unselect: nothing
                # me unselect, other select: set to select
                # both select: both confirm
                createSFXEvent('select')
                almanac_mu_chart_selector = [i//5, i%5, 1]
                if(almanac_mu_chart_selector[:2] == [3, 2]):
                    game_state = "almanac"
                    almanac_mu_chart_ghost = None
                    almanac_mu_chart_selector[2] = 0
                
            elif(mouse[1][2]):
                almanac_mu_chart_selector[2] = 0

    return game_state, [almanac_mu_chart_selector, almanac_mu_chart_ghost]

almanac_art_buttons = list(almanac_main_buttons)

def almanac_art_navigation(timer):
    game_state = "almanac_art"
    pressed = engine.handle_input.menu_input()
    mouse = engine.handle_input.handle_mouse()
    global selector_position
    if('p1_up' in pressed or 'p2_up' in pressed):
        if selector_position == 0:
            selector_position = 5
        else:
            selector_position -= 1
    elif('p1_down' in pressed or 'p2_down' in pressed):
        if selector_position == 5:
            selector_position = 0
        else:
            selector_position += 1

    def update_gamestate():
        global selector_position
        if(selector_position == 5): #Casual
            game_state = "almanac"
            selector_position = 3
        elif(selector_position == 0):
            game_state = "almanac_art_backgrounds"
        elif(selector_position == 1):
            selector_position = 0
            game_state = "almanac_art_blobs"
        else:
            game_state = "almanac_art"
        return game_state

    if(not timer) and ('p1_ability' in pressed or 'p2_ability' in pressed or 'return' in pressed):
        createSFXEvent('select')
        game_state = update_gamestate()
            
    for i in range(len(almanac_main_buttons)):
        if(almanac_main_buttons[i].check_hover(mouse)):
            if(mouse[2] or mouse[1][0] or mouse[1][2]): # Did we move the mouse?
                selector_position = i # Change the selector position

            if(mouse[1][0] or mouse[1][2]):
                createSFXEvent('select')
                game_state = update_gamestate()

    return selector_position, game_state

def almanac_art_backgrounds_navigation(timer):
    game_state = "almanac_art_backgrounds"
    pressed = engine.handle_input.menu_input()
    mouse = engine.handle_input.handle_mouse()
    global selector_position
    if('p1_left' in pressed or 'p2_left' in pressed):
        if selector_position == 0:
            selector_position = 6
        else:
            selector_position -= 1
    elif('p1_right' in pressed or 'p2_right' in pressed or mouse[1][0]):
        if selector_position == 6:
            selector_position = 0
        else:
            selector_position += 1
    if(not timer) and ('p1_ability' in pressed or 'p1_kick' in pressed or 'p2_ability' in pressed or 'p2_kick' in pressed or 'return' in pressed or mouse[1][2]):
        selector_position = 0
        game_state = "almanac_art"

    return selector_position, game_state

def almanac_art_blobs_navigation(timer):
    game_state = "almanac_art_blobs"
    pressed = engine.handle_input.menu_input()
    mouse = engine.handle_input.handle_mouse()
    global selector_position
    if('p1_left' in pressed or 'p2_left' in pressed):
        if selector_position == 0:
            selector_position = 39
        else:
            selector_position -= 1
    elif('p1_right' in pressed or 'p2_right' in pressed or mouse[1][0]):
        if selector_position == 39:
            selector_position = 0
        else:
            selector_position += 1
    if(not timer) and ('p1_ability' in pressed or 'p1_kick' in pressed or 'p2_ability' in pressed or 'p2_kick' in pressed or 'return' in pressed or mouse[1][2]):
        selector_position = 0
        game_state = "almanac_art"

    return selector_position, game_state

def credits_navigation(timer):
    pressed = engine.handle_input.menu_input()
    mouse = engine.handle_input.handle_mouse()
    game_state = "credits"
    if(not timer) and ('p1_ability' in pressed or 'p1_kick' in pressed or 'p2_ability' in pressed or 'p2_kick' in pressed or 'return' in pressed or mouse[1][0] or mouse[1][2]):
        createSFXEvent('select')
        game_state = "almanac"
    return [game_state]
