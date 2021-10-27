import engine.handle_input
from resources.sound_engine.sfx_event import createSFXEvent
from json import dumps

selector_position = 0

def settings_navigation(timer, settings, previous_screen, cwd):
    game_state = "settings"
    pressed = engine.handle_input.menu_input()
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
        if(selector_position == 3):
            if(settings['music_volume'] > 0):
                settings['music_volume'] -= 1
            else:
                settings['music_volume'] = 10
        elif(selector_position == 4):
            if(settings['sound_volume'] > 0):
                settings['sound_volume'] -= 1
            else: 
                settings['sound_volume'] = 10
            createSFXEvent('chime_progress')

        
    elif('p1_right' in pressed or 'p2_right' in pressed):
        if(selector_position == 3):
            if(settings['music_volume'] < 10):
                settings['music_volume'] += 1
            else:
                settings['music_volume'] = 0
        elif(selector_position == 4):
            if(settings['sound_volume'] < 10):
                settings['sound_volume'] += 1
            else: 
                settings['sound_volume'] = 0
            createSFXEvent('chime_progress')

    if(not timer) and ('p1_ability' in pressed or 'p2_ability' in pressed or 'return' in pressed):
        if(selector_position == len(settings) + 3):
            selector_position = 0
            game_state = previous_screen
            createSFXEvent('select')
        elif(selector_position == len(settings) + 2):
            settings['hd_backgrounds'] = True
            settings['hd_blobs'] = True
            settings['smooth_scaling'] = True
            createSFXEvent('chime_completion')
        elif(selector_position == len(settings) + 1):
            engine.handle_input.reset_inputs()
            createSFXEvent('chime_completion')
        elif(selector_position == 5):
            game_state = "rebind"
            createSFXEvent('select')
        elif(selector_position == 0):
            settings['hd_backgrounds'] = not(settings['hd_backgrounds'])
            createSFXEvent('select')
        elif(selector_position == 1):
            settings['hd_blobs'] = not(settings['hd_blobs'])
            createSFXEvent('select')
        elif(selector_position == 2):
            settings['smooth_scaling'] = not(settings['smooth_scaling'])
            createSFXEvent('select')

        with open(cwd+'/config/settings.txt', 'w') as settingsdoc:
            settingsdoc.write(dumps(settings))

    return selector_position, game_state, settings
