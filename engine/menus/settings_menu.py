import engine.handle_input
from resources.sound_engine.sfx_event import createSFXEvent
from json import dumps

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
]

def settings_selection_right(selector_position, settings, previous_screen, cwd, limit = None):
    game_state = "settings"
    # TODO: Force Toggle Fullscreen
    def adjust_music():
        if(settings['music_volume'] < 10):
                settings['music_volume'] += 1
        else:
            settings['music_volume'] = 0

    def adjust_sound():
        if(settings['sound_volume'] < 10):
            settings['sound_volume'] += 1
        else: 
            settings['sound_volume'] = 0
        createSFXEvent('chime_progress')

    def go_back():
        nonlocal selector_position
        nonlocal game_state
        selector_position = 0
        game_state = previous_screen
        createSFXEvent('select')

    def reset_settings():
        settings['hd_backgrounds'] = True   
        settings['hd_blobs'] = True
        settings['smooth_scaling'] = True
        createSFXEvent('chime_completion')

    def reset_inputs():
        engine.handle_input.reset_inputs()
        createSFXEvent('chime_completion')

    def enter_rebind():
        nonlocal game_state
        game_state = "rebind"
        createSFXEvent('select')

    def enter_joystick():
        nonlocal game_state
        game_state = "controller_config"
        createSFXEvent('select')

    def toggle_background():
        settings['hd_backgrounds'] = not(settings['hd_backgrounds'])
        createSFXEvent('select')

    def toggle_hd_blobs():
        settings['hd_blobs'] = not(settings['hd_blobs'])
        createSFXEvent('select')

    def toggle_scaling():
        settings['smooth_scaling'] = not(settings['smooth_scaling'])
        createSFXEvent('select')

    def toggle_ui_mode():
        settings['ui_mode'] = not settings['ui_mode']
        createSFXEvent('select')

    run_func = {
        0: toggle_background,
        1: toggle_ui_mode,
        2: toggle_scaling,
        3: adjust_music,
        4: adjust_sound,
        5: enter_rebind,
        len(settings) + 3: go_back,
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
    game_state = "settings"
    # TODO: Force Toggle Fullscreen
    def adjust_music():
        if(settings['music_volume'] > 0):
            settings['music_volume'] -= 1
        else:
            settings['music_volume'] = 10

    def adjust_sound():
        if(settings['sound_volume'] > 0):
            settings['sound_volume'] -= 1
        else: 
            settings['sound_volume'] = 10
        createSFXEvent('chime_progress')

    def go_back():
        nonlocal selector_position
        nonlocal game_state
        selector_position = 0
        game_state = previous_screen
        createSFXEvent('select')

    def reset_settings():
        settings['hd_backgrounds'] = True   
        settings['hd_blobs'] = True
        settings['smooth_scaling'] = True
        createSFXEvent('chime_completion')

    def reset_inputs():
        engine.handle_input.reset_inputs()
        createSFXEvent('chime_completion')

    def enter_rebind():
        nonlocal game_state
        game_state = "rebind"
        createSFXEvent('select')

    def enter_joystick():
        nonlocal game_state
        game_state = "controller_config"
        createSFXEvent('select')

    def toggle_background():
        settings['hd_backgrounds'] = not(settings['hd_backgrounds'])
        createSFXEvent('select')

    def toggle_hd_blobs():
        settings['hd_blobs'] = not(settings['hd_blobs'])
        createSFXEvent('select')

    def toggle_scaling():
        settings['smooth_scaling'] = not(settings['smooth_scaling'])
        createSFXEvent('select')

    def toggle_ui_mode():
        settings['ui_mode'] = not settings['ui_mode']
        createSFXEvent('select')

    run_func = {
        0: toggle_background,
        1: toggle_ui_mode,
        2: toggle_scaling,
        3: adjust_music,
        4: adjust_sound,
        5: enter_rebind,
        len(settings) + 3: go_back,
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
    pressed = engine.handle_input.menu_input()
    mouse = engine.handle_input.handle_mouse()
    game_state = "settings"
    global selector_position
    if('p1_up' in pressed or 'p2_up' in pressed):
        if selector_position == 0:
            selector_position = len(settings) + 3
        else:
            selector_position -= 1
    elif('p1_down' in pressed or 'p2_down' in pressed):
        if selector_position == len(settings) + 3:
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
