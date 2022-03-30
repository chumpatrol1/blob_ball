import engine.handle_input
from json import dumps
from engine.menus.main_menu import game_state_navigation
from resources.sound_engine.sfx_event import createSFXEvent
from os import getcwd
from engine.button import Button
selector_position = 0
cwd = getcwd()

pause_buttons = [
    Button(125, 200, 525, 825),
    Button(200, 275, 525, 825),
    Button(275, 350, 525, 825),
    Button(350, 425, 525, 825),
    Button(425, 500, 525, 825),
]


def pause_menu_selection(selector_position, game_state, settings, left_mode = False, unpause_mode = False):

    def go_back():
        nonlocal game_state
        nonlocal unpause_mode
        if(unpause_mode):
            game_state = 'casual_match'
            createSFXEvent('select')

    def take_screenshot():
        from resources.graphics_engine.display_pause import take_screenshot
        take_screenshot()
        createSFXEvent('camera')

    def raise_music_volume():
        if not left_mode:
            if(settings['music_volume'] < 10):
                settings['music_volume'] += 1
            else: 
                settings['music_volume'] = 0
        else:
            if(settings['music_volume'] > 0):
                settings['music_volume'] -= 1
            else:
                settings['music_volume'] = 10
            
        with open(cwd+'/config/settings.txt', 'w') as settingsdoc:
            settingsdoc.write(dumps(settings))

    def raise_sound_volume():
        if not left_mode:
            if(settings['sound_volume'] < 10):
                settings['sound_volume'] += 1
            else: 
                settings['sound_volume'] = 0
        else:
            if(settings['sound_volume'] > 0):
                settings['sound_volume'] -= 1
            else: 
                settings['sound_volume'] = 10
        createSFXEvent('chime_progress')

        with open(cwd+'/config/settings.txt', 'w') as settingsdoc:
            settingsdoc.write(dumps(settings))

    def quit_game():
        nonlocal game_state
        nonlocal unpause_mode
        if(unpause_mode):
            createSFXEvent('select')
            game_state = 'css'

    run_func = {
        0: go_back,
        1: take_screenshot,
        2: raise_music_volume,
        3: raise_sound_volume,
        4: quit_game,
    }

    run_func[selector_position]()

    return game_state

def handle_pause_menu(timer, settings):
    global selector_position
    game_state = 'pause'
    pressed = engine.handle_input.menu_input(pause_screen=True)
    mouse = engine.handle_input.handle_mouse()
    if('p1_up' in pressed or 'p2_up' in pressed):
        if(selector_position == 0):
            selector_position = 4
        else:
            selector_position -= 1
    elif('p1_down' in pressed or 'p2_down' in pressed):
        if(selector_position == 4):
            selector_position = 0
        else:
            selector_position += 1

    if(not timer and 'escape' in pressed):
        game_state = 'casual_match'
    elif('p1_ability' in pressed or 'p2_ability' in pressed or 'p1_right' in pressed or 'p2_right' in pressed):
        game_state = pause_menu_selection(selector_position, game_state, settings,)
    elif('return' in pressed):
        game_state = pause_menu_selection(selector_position, game_state, settings, unpause_mode=True)
    elif('p1_kick' in pressed or 'p2_kick' in pressed or 'p1_left' in pressed or 'p2_left' in pressed):
        game_state = pause_menu_selection(selector_position, game_state, settings, left_mode=True)

    if(game_state != 'pause'):
        selector_position = 0

    for i in range(len(pause_buttons)):
        if(pause_buttons[i].check_hover(mouse)):
            if(mouse[2] or mouse[1][0] or mouse[1][2]): # Did we move the mouse?
                selector_position = i # Change the selector position

            if(mouse[1][0]):
                game_state = pause_menu_selection(selector_position, game_state, settings, unpause_mode = True)
            elif(mouse[1][2]):
                game_state = pause_menu_selection(selector_position, game_state, settings,left_mode=True, unpause_mode = True)

    return game_state, [selector_position]