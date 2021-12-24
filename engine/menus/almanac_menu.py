import engine.handle_input
from resources.sound_engine.sfx_event import createSFXEvent
selector_position = 0
def almanac_navigation(timer, previous_screen):
    game_state = "almanac"
    pressed = engine.handle_input.menu_input()
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
    if(not timer) and ('p1_ability' in pressed or 'p2_ability' in pressed or 'return' in pressed):
        createSFXEvent('select')
        if(selector_position == 0): #Blobs and Info
            game_state = "almanac"
        elif(selector_position == 1):
            game_state = "medals"
            #selector_position = 0
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
            
        #print("Selected position {}!".format(selector_position))
    return selector_position, game_state

def almanac_stats_navigation(timer):
    pressed = engine.handle_input.menu_input()
    game_state = "almanac_stats"
    if(not timer) and ('p1_ability' in pressed or 'p2_ability' in pressed or 'return' in pressed):
        createSFXEvent('select')
        game_state = "almanac_stats_page_2"
    return [game_state]

def almanac_stats_navigation_2(timer):
    pressed = engine.handle_input.menu_input()
    game_state = "almanac_stats_page_2"
    if(not timer) and ('p1_ability' in pressed or 'p2_ability' in pressed or 'return' in pressed):
        createSFXEvent('select')
        game_state = "almanac_stats_page_3"
        global p1_selector_position
        p1_selector_position = [3, 2, 0, 0]
    return [game_state]

almanac_mu_chart_selector = [3, 2, 0]

def almanac_stats_navigation_3():
    global almanac_mu_chart_selector
    game_state = "almanac_stats_page_3"
    pressed = engine.handle_input.css_input()
    pressed = engine.handle_input.merge_inputs(pressed)
    global almanac_mu_chart_selector

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

    return game_state, almanac_mu_chart_selector


def almanac_art_navigation(timer):
    game_state = "almanac_art"
    pressed = engine.handle_input.menu_input()
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
    if(not timer) and ('p1_ability' in pressed or 'p2_ability' in pressed or 'return' in pressed):
        createSFXEvent('select')
        if(selector_position == 5): #Casual
            game_state = "almanac"
            selector_position = 3
        elif(selector_position == 0):
            game_state = "almanac_art_backgrounds"
        elif(selector_position == 1):
            selector_position = 0
            game_state = "almanac_art_blobs"
            
        #print("Selected position {}!".format(selector_position))
    return selector_position, game_state

def almanac_art_backgrounds_navigation(timer):
    game_state = "almanac_art_backgrounds"
    pressed = engine.handle_input.menu_input()
    global selector_position
    if('p1_left' in pressed or 'p2_left' in pressed):
        if selector_position == 0:
            selector_position = 6
        else:
            selector_position -= 1
    elif('p1_right' in pressed or 'p2_right' in pressed):
        if selector_position == 6:
            selector_position = 0
        else:
            selector_position += 1
    if(not timer) and ('p1_ability' in pressed or 'p2_ability' in pressed or 'return' in pressed):
        selector_position = 0
        game_state = "almanac_art"

    return selector_position, game_state

def almanac_art_blobs_navigation(timer):
    game_state = "almanac_art_blobs"
    pressed = engine.handle_input.menu_input()
    global selector_position
    if('p1_left' in pressed or 'p2_left' in pressed):
        if selector_position == 0:
            selector_position = 39
        else:
            selector_position -= 1
    elif('p1_right' in pressed or 'p2_right' in pressed):
        if selector_position == 39:
            selector_position = 0
        else:
            selector_position += 1
    if(not timer) and ('p1_ability' in pressed or 'p2_ability' in pressed or 'return' in pressed):
        selector_position = 0
        game_state = "almanac_art"

    return selector_position, game_state

def credits_navigation(timer):
    pressed = engine.handle_input.menu_input()
    game_state = "credits"
    if(not timer) and ('p1_ability' in pressed or 'p2_ability' in pressed or 'return' in pressed):
        createSFXEvent('select')
        game_state = "almanac"
    return [game_state]
