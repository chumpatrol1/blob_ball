import engine.handle_input
from engine.initializer import load_default_ruleset
from resources.sound_engine.sfx_event import createSFXEvent
from json import dumps
from engine.button import Button


selector_position = 0
rules_navigation_buttons = [
    Button(65, 130, 0, 600),
    Button(135, 200, 0, 600),
    Button(205, 275, 0, 600),
    Button(290, 360, 0, 600),
    Button(365, 430, 0, 600),
    Button(440, 505, 0, 600),
    Button(515, 580, 0, 600),
    Button(590, 670, 0, 600),
    Button(675, 740, 0, 600),
]

# Left arrow, or right clicks
def rules_navigation_selection_left(selector_position, ruleset, previous_screen, cwd, limit = None):
    game_state = "rules"

    def update_goal_limit():
        if(ruleset['goal_limit'] > 1):
            ruleset['goal_limit'] -= 1
        else:
            ruleset['goal_limit'] = 25
        createSFXEvent('chime_progress')

    def update_time_limit():
        if(ruleset['time_limit'] > 0):
            ruleset['time_limit'] -= 600
        else:
            ruleset['time_limit'] = 36000
        createSFXEvent('chime_progress')

    def update_time_bonus():
        if(ruleset['time_bonus'] > 0):
            ruleset['time_bonus'] -= 300
        else:
            ruleset['time_bonus'] = 3600
        createSFXEvent('chime_progress')
    
    def update_charge_rate():
        if(ruleset['special_ability_charge_base'] > 0):
            ruleset['special_ability_charge_base'] -= 1
        else:
            ruleset['special_ability_charge_base'] = 20
        createSFXEvent('chime_progress')
    
    def go_back():
        global selector_position
        nonlocal game_state
        selector_position = 0
        game_state = previous_screen
        createSFXEvent('select')

    def reload_ruleset():
        nonlocal ruleset
        ruleset = load_default_ruleset()
        createSFXEvent('chime_completion')
    def toggle_dz():
        ruleset['danger_zone_enabled'] = not(ruleset['danger_zone_enabled'])
        createSFXEvent('select')

    def goto_p1_mods():
        nonlocal game_state
        game_state = 'p1_mods'
        createSFXEvent('select')
    
    def goto_p2_mods():
        nonlocal game_state
        game_state = 'p2_mods'
        createSFXEvent('select')

    run_func = {
        0: update_goal_limit,
        1: update_time_limit,
        2: update_time_bonus,
        3: update_charge_rate,
        4: toggle_dz,
        5: goto_p1_mods,
        6: goto_p2_mods,
        7: reload_ruleset,
        8: go_back,
    }

    if(limit is None or selector_position <= limit):
        run_func[selector_position]()
    
    with open(cwd+'/config/ruleset.txt', 'w') as rulesetdoc:
        rulesetdoc.write(dumps(ruleset))
    return game_state, ruleset

# Right arrow, or left clicks
def rules_navigation_selection_right(selector_position, ruleset, previous_screen, cwd, limit = None):
    game_state = "rules"

    def update_goal_limit():
        if(ruleset['goal_limit'] < 25):
            ruleset['goal_limit'] += 1
        else:
            ruleset['goal_limit'] = 1
        createSFXEvent('chime_progress')

    def update_time_limit():
        if(ruleset['time_limit'] < 36000):
            ruleset['time_limit'] += 600
        else:
            ruleset['time_limit'] = 0
        createSFXEvent('chime_progress')

    def update_time_bonus():
        if(ruleset['time_bonus'] < 3600):
            ruleset['time_bonus'] += 300
        else:
            ruleset['time_bonus'] = 0
        createSFXEvent('chime_progress')
    
    def update_charge_rate():
        if(ruleset['special_ability_charge_base'] < 20):
            ruleset['special_ability_charge_base'] += 1
        else:
            ruleset['special_ability_charge_base'] = 0
        createSFXEvent('chime_progress')
    
    def go_back():
        global selector_position
        nonlocal game_state
        selector_position = 0
        game_state = previous_screen
        createSFXEvent('select')

    def reload_ruleset():
        nonlocal ruleset
        ruleset = load_default_ruleset()
        createSFXEvent('chime_completion')
    def toggle_dz():
        ruleset['danger_zone_enabled'] = not(ruleset['danger_zone_enabled'])
        createSFXEvent('select')

    def goto_p1_mods():
        nonlocal game_state
        game_state = 'p1_mods'
        createSFXEvent('select')
    
    def goto_p2_mods():
        nonlocal game_state
        game_state = 'p2_mods'
        createSFXEvent('select')

    run_func = {
        0: update_goal_limit,
        1: update_time_limit,
        2: update_time_bonus,
        3: update_charge_rate,
        4: toggle_dz,
        5: goto_p1_mods,
        6: goto_p2_mods,
        7: reload_ruleset,
        8: go_back,
    }

    if(limit is None or selector_position <= limit):
        run_func[selector_position]()

    with open(cwd+'/config/ruleset.txt', 'w') as rulesetdoc:
        rulesetdoc.write(dumps(ruleset))
    return game_state, ruleset

def rules_navigation(timer, ruleset, previous_screen, cwd):
    game_state = "rules"
    pressed = engine.handle_input.menu_input()
    mouse = engine.handle_input.handle_mouse()
    global selector_position
    if('p1_up' in pressed or 'p2_up' in pressed):
        if selector_position == 0:
            selector_position = len(ruleset)
        else:
            selector_position -= 1
    elif('p1_down' in pressed or 'p2_down' in pressed):
        if selector_position == len(ruleset):
            selector_position = 0
        else:
            selector_position += 1
    if('p1_left' in pressed or 'p2_left' in pressed):
        game_state, ruleset = rules_navigation_selection_left(selector_position, ruleset, previous_screen, cwd, limit = 4)
    if('p1_right' in pressed or 'p2_right' in pressed or 'return' in pressed):
        game_state, ruleset = rules_navigation_selection_right(selector_position, ruleset, previous_screen, cwd, limit = 4)
    if(not timer) and ('p1_ability' in pressed or 'p2_ability' in pressed or 'return' in pressed):
        game_state, ruleset = rules_navigation_selection_right(selector_position, ruleset, previous_screen, cwd)
            
    for i in range(len(rules_navigation_buttons)):
        if(rules_navigation_buttons[i].check_hover(mouse)):
            if(mouse[2] or mouse[1][0] or mouse[1][2]): # Did we move the mouse?
                selector_position = i # Change the selector position

            if(mouse[1][0]):
                game_state, ruleset = rules_navigation_selection_right(selector_position, ruleset, previous_screen, cwd)
            elif(mouse[1][2]):
                game_state, ruleset = rules_navigation_selection_left(selector_position, ruleset, previous_screen, cwd)
            

    return selector_position, game_state, ruleset

p_selector_position = 0
page = 1

def player_mods_page_1_left(p_selector_position, ruleset, player, limit = None):
    def adjust_max_hp():
        pmod = ruleset[player]['max_hp']
        if(pmod is None):
            pmod = 20
        elif(pmod > 2):
            pmod -= 2
        elif(pmod == 2):
            pmod = 1
        else:
            pmod = None
        ruleset[player]['max_hp'] = pmod
    
    def adjust_top_speed():
        pmod = ruleset[player]['top_speed']
        if(pmod is None):
            pmod = 5
        elif(pmod == 1):
            pmod = None
        else:
            pmod -= 1
        ruleset[player]['top_speed'] = pmod

    def adjust_traction():
        pmod = ruleset[player]['traction']
        if(pmod is None):
            pmod = 5
        elif(pmod == 1):
            pmod = None
        else:
            pmod -= 1
        ruleset[player]['traction'] = pmod

    def adjust_friction():
        pmod = ruleset[player]['friction']
        if(pmod is None):
            pmod = 5
        elif(pmod == 1):
            pmod = None
        else:
            pmod -= 1
        ruleset[player]['friction'] = pmod

    def adjust_gravity():
        pmod = ruleset[player]['gravity']
        if(pmod is None):
            pmod = 5
        elif(pmod == 1):
            pmod = None
        else:
            pmod -= 1
        ruleset[player]['gravity'] = pmod

    def adjust_boost_cost():
        pmod = ruleset[player]['boost_cost']
        if(pmod is None):
            pmod = 1200
        elif(pmod == 0):
            pmod = None
        else:
            pmod -= 120
        ruleset[player]['boost_cost'] = pmod

    def adjust_boost_cooldown():
        pmod = ruleset[player]['boost_cooldown_max']
        if(pmod is None):
            pmod = 5
        elif(pmod == 1):
            pmod = None
        else:
            pmod -= 1
        ruleset[player]['boost_cooldown_max'] = pmod

    def adjust_boost_duration():
        pmod = ruleset[player]['boost_duration']
        if(pmod is None):
            pmod = 5
        elif(pmod == 1):
            pmod = None
        else:
            pmod -= 1
        ruleset[player]['boost_duration'] = pmod

    run_func = {
        0: adjust_max_hp,
        1: adjust_top_speed,
        2: adjust_traction,
        3: adjust_friction,
        4: adjust_gravity,
        5: adjust_boost_cost,
        6: adjust_boost_cooldown,
        7: adjust_boost_duration,
    }        

    if(limit is None or p_selector_position <= limit):
        run_func[p_selector_position]()

    if(p_selector_position < 8):
        createSFXEvent('chime_progress')

def player_mods_page_2_left(p_selector_position, ruleset, player, limit = None):
    def adjust_kick_cooldown():
        pmod = ruleset[player]['kick_cooldown_rate']
        if(pmod is None):
            pmod = 5
        elif(pmod == 1):
            pmod = None
        else:
            pmod -= 1
        ruleset[player]['kick_cooldown_rate'] = pmod
    
    def adjust_block_cooldown():
        pmod = ruleset[player]['block_cooldown_rate']
        if(pmod is None):
            pmod = 5
        elif(pmod == 1):
            pmod = None
        else:
            pmod -= 1
        ruleset[player]['block_cooldown_rate'] = pmod

    def adjust_ability_cost():
        pmod = ruleset[player]['special_ability_cost']
        if(pmod is None):
            pmod = 1200
        elif(pmod == 30):
            pmod = None
        else:
            pmod -= 30
        ruleset[player]['special_ability_cost'] = pmod

    def adjust_ability_maintenance():
        pmod = ruleset[player]['special_ability_maintenance']
        if(pmod is None):
            pmod = 30
        elif(pmod == 0):
            pmod = None
        else:
            pmod -= 1
        ruleset[player]['special_ability_maintenance'] = pmod

    def adjust_ability_max():
        pmod = ruleset[player]['special_ability_max']
        if(pmod is None):
            pmod = 2400
        elif(pmod == 1200):
            pmod = None
        else:
            pmod -= 120
        ruleset[player]['special_ability_max'] = pmod

    def adjust_ability_cooldown():
        pmod = ruleset[player]['special_ability_cooldown']
        if(pmod is None):
            pmod = 900
        elif(pmod == 30):
            pmod = 2
        elif(pmod == 2):
            pmod = None
        else:
            pmod -= 30
        ruleset[player]['special_ability_cooldown'] = pmod

    def adjust_ability_delay():
        pmod = ruleset[player]['special_ability_delay']
        if(pmod is None):
            pmod = 60
        elif(pmod == 5):
            pmod = None
        else:
            pmod -= 5
        ruleset[player]['special_ability_delay'] = pmod

    def adjust_ability_duration():
        pmod = ruleset[player]['special_ability_duration']
        if(pmod is None):
            pmod = 300
        elif(pmod == 30):
            pmod = None
        else:
            pmod -= 30
        ruleset[player]['special_ability_duration'] = pmod

    run_func = {
        0: adjust_kick_cooldown,
        1: adjust_block_cooldown,
        2: adjust_ability_cost,
        3: adjust_ability_maintenance,
        4: adjust_ability_max,
        5: adjust_ability_cooldown,
        6: adjust_ability_delay,
        7: adjust_ability_duration,
    }        

    if(limit is None or p_selector_position <= limit):
        run_func[p_selector_position]()

    if(p_selector_position < 8):
        createSFXEvent('chime_progress')

def player_mods_page_1_right(p_selector_position, ruleset, player, limit = None):
    def adjust_max_hp():
        pmod = ruleset[player]['max_hp']
        if(pmod is None):
            pmod = 1
        elif(pmod == 1):
            pmod = 2
        elif(pmod < 20):
            pmod += 2
        else:
            pmod = None
        ruleset[player]['max_hp'] = pmod

    def adjust_top_speed():
        pmod = ruleset[player]['top_speed']
        if(pmod is None):
            pmod = 1
        elif(pmod == 5):
            pmod = None
        else:
            pmod += 1
        ruleset[player]['top_speed'] = pmod

    def adjust_traction():
        pmod = ruleset[player]['traction']
        if(pmod is None):
            pmod = 1
        elif(pmod == 5):
            pmod = None
        else:
            pmod += 1
        ruleset[player]['traction'] = pmod

    def adjust_friction():
        pmod = ruleset[player]['friction']
        if(pmod is None):
            pmod = 1
        elif(pmod == 5):
            pmod = None
        else:
            pmod += 1
        ruleset[player]['friction'] = pmod

    def adjust_gravity():
        pmod = ruleset[player]['gravity']
        if(pmod is None):
            pmod = 1
        elif(pmod == 5):
            pmod = None
        else:
            pmod += 1
        ruleset[player]['gravity'] = pmod

    def adjust_boost_cost():
        pmod = ruleset[player]['boost_cost']
        if(pmod is None):
            pmod = 120
        elif(pmod == 1200):
            pmod = None
        else:
            pmod += 120
        ruleset[player]['boost_cost'] = pmod

    def adjust_boost_cooldown():
        pmod = ruleset[player]['boost_cooldown_max']
        if(pmod is None):
            pmod = 1
        elif(pmod == 5):
            pmod = None
        else:
            pmod += 1
        ruleset[player]['boost_cooldown_max'] = pmod

    def adjust_boost_duration():
        pmod = ruleset[player]['boost_duration']
        if(pmod is None):
            pmod = 1
        elif(pmod == 5):
            pmod = None
        else:
            pmod += 1
        ruleset[player]['boost_duration'] = pmod

    run_func = {
        0: adjust_max_hp,
        1: adjust_top_speed,
        2: adjust_traction,
        3: adjust_friction,
        4: adjust_gravity,
        5: adjust_boost_cost,
        6: adjust_boost_cooldown,
        7: adjust_boost_duration,
    }        

    if(limit is None or p_selector_position <= limit):
        run_func[p_selector_position]()

    if(p_selector_position < 8):
        createSFXEvent('chime_progress')

def player_mods_page_2_right(p_selector_position, ruleset, player, limit = None):
    def adjust_kick_cooldown():
        pmod = ruleset[player]['kick_cooldown_rate']
        if(pmod is None):
            pmod = 1
        elif(pmod == 5):
            pmod = None
        else:
            pmod += 1
        ruleset[player]['kick_cooldown_rate'] = pmod
    def adjust_block_cooldown():
        pmod = ruleset[player]['block_cooldown_rate']
        if(pmod is None):
            pmod = 1
        elif(pmod == 5):
            pmod = None
        else:
            pmod += 1
        ruleset[player]['block_cooldown_rate'] = pmod

    def adjust_ability_cost():
        pmod = ruleset[player]['special_ability_cost']
        if(pmod is None):
            pmod = 30
        elif(pmod == 1200):
            pmod = None
        else:
            pmod += 30
        ruleset[player]['special_ability_cost'] = pmod

    def adjust_ability_maintenance():
        pmod = ruleset[player]['special_ability_maintenance']
        if(pmod is None):
            pmod = 0
        elif(pmod == 30):
            pmod = None
        else:
            pmod += 1
        ruleset[player]['special_ability_maintenance'] = pmod

    def adjust_ability_max():
        pmod = ruleset[player]['special_ability_max']
        if(pmod is None):
            pmod = 1200
        elif(pmod == 2400):
            pmod = None
        else:
            pmod += 120
        ruleset[player]['special_ability_max'] = pmod

    def adjust_ability_cooldown():
        pmod = ruleset[player]['special_ability_cooldown']
        if(pmod is None):
            pmod = 2
        elif(pmod == 2):
            pmod = 30
        elif(pmod == 900):
            pmod = None
        else:
            pmod += 30
        ruleset[player]['special_ability_cooldown'] = pmod

    def adjust_ability_delay():
        pmod = ruleset[player]['special_ability_delay']
        if(pmod is None):
            pmod = 5
        elif(pmod == 60):
            pmod = None
        else:
            pmod += 5
        ruleset[player]['special_ability_delay'] = pmod

    def adjust_ability_duration():
        pmod = ruleset[player]['special_ability_duration']
        if(pmod is None):
            pmod = 30
        elif(pmod == 300):
            pmod = None
        else:
            pmod += 30
        ruleset[player]['special_ability_duration'] = pmod
    
    run_func = {
        0: adjust_kick_cooldown,
        1: adjust_block_cooldown,
        2: adjust_ability_cost,
        3: adjust_ability_maintenance,
        4: adjust_ability_max,
        5: adjust_ability_cooldown,
        6: adjust_ability_delay,
        7: adjust_ability_duration,
    }        

    if(limit is None or p_selector_position <= limit):
        run_func[p_selector_position]()

    if(p_selector_position < 8):
        createSFXEvent('chime_progress')

    if(p_selector_position < 8):
        createSFXEvent('chime_progress')

def player_mods_navigation(timer, ruleset, game_state, cwd):
    pressed = engine.handle_input.menu_input()
    mouse = engine.handle_input.handle_mouse()
    global p_selector_position
    global page

    if("p1" in game_state):
        player = "p1_modifiers"
    else:
        player = "p2_modifiers"

    if('p1_up' in pressed or 'p2_up' in pressed):
        if p_selector_position == 0:
            p_selector_position = 8
        else:
            p_selector_position -= 1
    elif('p1_down' in pressed or 'p2_down' in pressed):
        if p_selector_position == 8:
            p_selector_position = 0
        else:
            p_selector_position += 1
    if('p1_left' in pressed or 'p2_left' in pressed):
        if(page == 1):
            player_mods_page_1_left(p_selector_position, ruleset, player, limit = 7)
        elif(page == 2):
            player_mods_page_2_left(p_selector_position, ruleset, player, limit = 7)

        with open(cwd+'/config/ruleset.txt', 'w') as rulesetdoc:
            rulesetdoc.write(dumps(ruleset))

    elif('p1_right' in pressed or 'p2_right' in pressed or 'return' in pressed):
        if(page == 1):
            player_mods_page_1_right(p_selector_position, ruleset, player, limit = 7)
        elif(page == 2):
            player_mods_page_2_right(p_selector_position, ruleset, player, limit = 7)
        
        with open(cwd+'/config/ruleset.txt', 'w') as rulesetdoc:
            rulesetdoc.write(dumps(ruleset))

    if(not timer) and ('p1_ability' in pressed or 'p2_ability' in pressed or 'return' in pressed):
        if(p_selector_position == 8):
            p_selector_position = 0
            if(page == 1):
                page = 2
            else:
                page = 1
                game_state = "rules"
            createSFXEvent('select')
        else:
            if(page == 1):
                player_mods_page_1_right(p_selector_position, ruleset, player, limit = 7)
            elif(page == 2):
                player_mods_page_2_right(p_selector_position, ruleset, player, limit = 7)

    for i in range(len(rules_navigation_buttons)):
        if(rules_navigation_buttons[i].check_hover(mouse)):
            if(mouse[2] or mouse[1][0] or mouse[1][2]): # Did we move the mouse?
                p_selector_position = i # Change the selector position

            if(mouse[1][0]):
                if(p_selector_position == 8):
                    page = (not (page - 1)) + 1
                    if(page == 1):
                        game_state = "rules"
                    createSFXEvent('select')
                else:
                    if(page == 1):
                        player_mods_page_1_right(p_selector_position, ruleset, player, limit = 7)
                    elif(page == 2):
                        player_mods_page_2_right(p_selector_position, ruleset, player, limit = 7)
            elif(mouse[1][2]):
                if(p_selector_position == 8):
                    page = (not (page - 1)) + 1
                    if(page == 1):
                        game_state = "rules"
                    createSFXEvent('select')
                else:
                    if(p_selector_position == 8):
                        page = (not (page - 1)) + 1
                    else:
                        if(page == 1):
                            player_mods_page_1_left(p_selector_position, ruleset, player, limit = 7)
                        elif(page == 2):
                            player_mods_page_2_left(p_selector_position, ruleset, player, limit = 7)
    return game_state, [p_selector_position, ruleset, player, page]
