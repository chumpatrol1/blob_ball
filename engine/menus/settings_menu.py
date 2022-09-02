'''
engine/menus/settings_menu.py

Handles the settings menu which focuses more on appearance, sound and controls rather than how to win the game

> settings_selection_right(): Updates the settings when pressing right
> settings_selection_left(): Updates the settings when pressing left
> settings_navigation(): Handles navigating through the settings menu
'''

import engine.handle_input
from resources.sound_engine.sfx_event import createSFXEvent
from json import dumps

from updatechecker_dist import check_for_game_updates

selector_position = 0

from engine.button import Button
settings_buttons = [
    Button(65, 125, 0, 600),
    Button(125, 185, 0, 600),
    Button(185, 245, 0, 600),
    Button(245, 305, 0, 600),
    Button(305, 365, 0, 600),
    Button(365, 425, 0, 600),
    Button(425, 485, 0, 600),
    Button(485, 545, 0, 600),
    Button(545, 605, 0, 600),
    Button(605, 665, 0, 600),
    Button(665, 725, 0, 600),
]

def settings_selection_right(selector_position, settings, previous_screen, cwd, limit = None):
    '''
    Updates the settings when pressing right

    Inputs
        - selector_position [int]: Integer representing the location of the selector, ranging from 0 to len(settings) + 4 (aka 9)
        - settings [dict]: Dictionary containing all the settings that we have updated
        - previous_screen [string]: The place we navigated from - will either be "main_menu" or "css"
        - cwd [string]: Current working directory, so we can open the settings.txt file
        - limit [int]: Used with left/right navigation. Unused if we click or press ability to toggle/update

    Outputs
        - game_state [string]: Defaults to "settings"
        - selector_position [int]: Integer representing the location of the selector, ranging from 0 to len(settings) + 4 (aka 9)
    '''
    game_state = "settings"
    # TODO: Force Toggle Fullscreen
    def adjust_music():
        '''
        Adjusts the music volume
        '''
        if(settings['music_volume'] < 10):
                settings['music_volume'] += 1
        else:
            settings['music_volume'] = 0

    def adjust_sound():
        '''
        Adjusts the sound volume
        '''
        if(settings['sound_volume'] < 10):
            settings['sound_volume'] += 1
        else: 
            settings['sound_volume'] = 0
        createSFXEvent('chime_progress')

    def go_back():
        '''
        Sends us back to the previous screen
        '''
        nonlocal selector_position
        nonlocal game_state
        selector_position = 0
        game_state = previous_screen
        createSFXEvent('select')

    def reset_settings():
        '''
        Resets some of the settings to their default values
        '''
        settings['hd_backgrounds'] = True   
        settings['hd_blobs'] = True
        settings['smooth_scaling'] = True
        createSFXEvent('chime_completion')

    def reset_inputs():
        '''
        Resets keyboard inputs
        '''
        engine.handle_input.reset_inputs()
        createSFXEvent('chime_completion')

    def enter_rebind():
        '''
        Takes us to the keyboard rebind screen
        '''
        nonlocal game_state
        game_state = "rebind"
        createSFXEvent('select')

    def enter_joystick():
        '''
        Takes us to the controller rebind screen
        '''
        nonlocal game_state
        game_state = "controller_config"
        createSFXEvent('select')

    def toggle_background():
        '''
        Toggles backgrounds between HD and LD modes
        '''
        settings['hd_backgrounds'] = not(settings['hd_backgrounds'])
        createSFXEvent('select')

    def toggle_hd_blobs():
        '''
        Unused, slated for deletion. Toggles between HD and LD blobs.
        '''
        settings['hd_blobs'] = not(settings['hd_blobs'])
        createSFXEvent('select')

    def toggle_scaling():
        '''
        Toggles smooth scaling mode (used primarily in non 1366x768 modes)
        '''
        settings['smooth_scaling'] = not(settings['smooth_scaling'])
        createSFXEvent('select')

    def toggle_ui_mode():
        '''
        Toggles UI from top to bottom
        '''
        settings['ui_mode'] = not settings['ui_mode']
        createSFXEvent('select')

    def toggle_gversion():
        '''
        Unused
        '''
        if(settings['graphics'] == 1): # 0 = Legacy, 1 = Normal - I didn't make it a true or false statement in case we add more.
            settings['graphics'] = 0
        else:
            settings['graphics'] += 1
        createSFXEvent('select')
    
    def check_game_update():
        '''
        Checks for updates to Blob Ball
        '''
        check_for_game_updates()
        

    run_func = {
        0: toggle_background,
        1: toggle_ui_mode,
        2: toggle_scaling,
        3: adjust_music,
        4: adjust_sound,
        5: enter_rebind,
        #6: toggle_gversion,
        len(settings) + 4: go_back,
        len(settings) + 3: check_game_update,
        len(settings) + 2: reset_settings,
        len(settings) + 1: reset_inputs,
        len(settings): enter_joystick,
    }        
    if(limit is None or selector_position <= limit):
        run_func[selector_position]()

    with open(cwd+'/config/settings.txt', 'w') as settingsdoc:
        settingsdoc.write(dumps(settings))

    return game_state, selector_position
    
def settings_selection_left(selector_position, settings, previous_screen, cwd, limit = None): # Handles left arrow, right clicks
    '''
    Updates the settings when pressing right

    Inputs
        - selector_position [int]: Integer representing the location of the selector, ranging from 0 to len(settings) + 4 (aka 9)
        - settings [dict]: Dictionary containing all the settings that we have updated
        - previous_screen [string]: The place we navigated from - will either be "main_menu" or "css"
        - cwd [string]: Current working directory, so we can open the settings.txt file
        - limit [int]: Used with left/right navigation. Unused if we click or press ability to toggle/update

    Outputs
        - game_state [string]: Defaults to "settings"
        - selector_position [int]: Integer representing the location of the selector, ranging from 0 to len(settings) + 4 (aka 9)
    '''
    game_state = "settings"
    # TODO: Force Toggle Fullscreen
    def adjust_music():
        '''
        Adjusts the music volume
        '''
        if(settings['music_volume'] > 0):
            settings['music_volume'] -= 1
        else:
            settings['music_volume'] = 10

    def adjust_sound():
        '''
        Adjusts the sound volume
        '''
        if(settings['sound_volume'] > 0):
            settings['sound_volume'] -= 1
        else: 
            settings['sound_volume'] = 10
        createSFXEvent('chime_progress')

    def go_back():
        '''
        Takes us back to the previous screen
        '''
        nonlocal selector_position
        nonlocal game_state
        selector_position = 0
        game_state = previous_screen
        createSFXEvent('select')

    def reset_settings():
        '''
        Resets some settings to the default
        '''
        settings['hd_backgrounds'] = True   
        settings['hd_blobs'] = True
        settings['smooth_scaling'] = True
        createSFXEvent('chime_completion')

    def reset_inputs():
        '''
        Resets the keyboard inputs
        '''
        engine.handle_input.reset_inputs()
        createSFXEvent('chime_completion')

    def enter_rebind():
        '''
        Takes us to the keyboard rebind screen
        '''
        nonlocal game_state
        game_state = "rebind"
        createSFXEvent('select')

    def enter_joystick():
        '''
        Takes us to the controller rebind screen
        '''
        nonlocal game_state
        game_state = "controller_config"
        createSFXEvent('select')

    def toggle_background():
        '''
        Toggles backgrounds between HD and LD modes
        '''
        settings['hd_backgrounds'] = not(settings['hd_backgrounds'])
        createSFXEvent('select')

    def toggle_hd_blobs():
        '''
        Unused, slated for deletion. Toggles between HD and LD blobs.
        '''
        settings['hd_blobs'] = not(settings['hd_blobs'])
        createSFXEvent('select')

    def toggle_scaling():
        '''
        Toggles smooth scaling mode (used primarily in non 1366x768 modes)
        '''
        settings['smooth_scaling'] = not(settings['smooth_scaling'])
        createSFXEvent('select')

    def toggle_ui_mode():
        '''
        Toggles the game UI from top to bottom
        '''
        settings['ui_mode'] = not settings['ui_mode']
        createSFXEvent('select')

    def check_game_update():
        '''
        Checks for updates to Blob Ball
        '''
        check_for_game_updates()

    run_func = {
        0: toggle_background,
        1: toggle_ui_mode,
        2: toggle_scaling,
        3: adjust_music,
        4: adjust_sound,
        5: enter_rebind,
        #6: toggle_gversion,
        len(settings) + 4: go_back,
        len(settings) + 3: check_game_update,
        len(settings) + 2: reset_settings,
        len(settings) + 1: reset_inputs,
        len(settings): enter_joystick,
    }    

    if(limit is None or selector_position <= limit):
        run_func[selector_position]()
    
    with open(cwd+'/config/settings.txt', 'w') as settingsdoc:
        settingsdoc.write(dumps(settings))

    return game_state, selector_position

def settings_navigation(timer, settings, previous_screen, cwd):
    '''
    TODO: Standardize return!
    Handles navigating through the settings menu

    Inputs:
        - timer [int]: The timer, which prevents the player from navigating too quickly
        - settings [dict]: Dictionary containing all the settings that we will update
        - previous_screen [string]: The place we navigated from - will either be "main_menu" or "css"
        - cwd [string]: Current working directory, so we can open the settings.txt file
        - selector_position [int] (global): Integer representing the location of the selector, ranging from 0 to len(settings) + 4 (aka 9)

    Outputs:
        - selector_position [int]: Integer representing the location of the selector, ranging from 0 to len(settings) + 4 (aka 9) 
        - game_state [string]: String representing the updated game state, which is pulled from the dictionary. Defaults to "almanac", otherwise is previous_screen
        - settings [dict]: Dictionary containing all the settings that we have updated
    '''
    pressed = engine.handle_input.menu_input()
    mouse = engine.handle_input.handle_mouse()
    game_state = "settings"
    global selector_position
    if('p1_up' in pressed or 'p2_up' in pressed):
        if selector_position == 0:
            selector_position = len(settings) + 4
        else:
            selector_position -= 1
    elif('p1_down' in pressed or 'p2_down' in pressed):
        if selector_position == len(settings) + 4:
            selector_position = 0
        else:
            selector_position += 1

    if('p1_left' in pressed or 'p2_left' in pressed):
        game_state, selector_position = settings_selection_left(selector_position, settings, previous_screen, cwd, limit = 4)

        
    elif('p1_right' in pressed or 'p2_right' in pressed):
        game_state, selector_position = settings_selection_right(selector_position, settings, previous_screen, cwd, limit = 4)

    if(not timer) and ('p1_ability' in pressed or 'p2_ability' in pressed or 'return' in pressed):
        game_state, selector_position = settings_selection_right(selector_position, settings, previous_screen, cwd)

    for i in range(len(settings_buttons)):
        if(settings_buttons[i].check_hover(mouse)):
            if(mouse[2] or mouse[1][0] or mouse[1][2]): # Did we move the mouse?
                selector_position = i # Change the selector position

            if(mouse[1][0]):
                game_state, selector_position = settings_selection_right(selector_position, settings, previous_screen, cwd)
            elif(mouse[1][2]):
                game_state, selector_position = settings_selection_left(selector_position, settings, previous_screen, cwd)

    return selector_position, game_state, settings
