import engine.handle_input
from resources.sound_engine.sfx_event import createSFXEvent
from json import dumps

selector_position = 0
def rules_navigation(timer, ruleset, previous_screen, cwd):
    game_state = "rules"
    pressed = engine.handle_input.menu_input()
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
        if(selector_position == 0):
            if(ruleset['goal_limit'] > 1):
                ruleset['goal_limit'] -= 1
            else:
                ruleset['goal_limit'] = 25
        elif(selector_position == 1):
            if(ruleset['time_limit'] > 0):
                ruleset['time_limit'] -= 600
            else:
                ruleset['time_limit'] = 36000
        elif(selector_position == 2):
            if(ruleset['time_bonus'] > 0):
                ruleset['time_bonus'] -= 300
            else:
                ruleset['time_bonus'] = 3600
        elif(selector_position == 3):
            if(ruleset['special_ability_charge_base'] > 0):
                ruleset['special_ability_charge_base'] -= 1
            else:
                ruleset['special_ability_charge_base'] = 20
        with open(cwd+'/config/ruleset.txt', 'w') as rulesetdoc:
            rulesetdoc.write(dumps(ruleset))
    elif('p1_right' in pressed or 'p2_right' in pressed or 'return' in pressed):
        if(selector_position == 0):
            if(ruleset['goal_limit'] < 25):
                ruleset['goal_limit'] += 1
            else:
                ruleset['goal_limit'] = 1
        elif(selector_position == 1):
            if(ruleset['time_limit'] < 36000):
                ruleset['time_limit'] += 600
            else:
                ruleset['time_limit'] = 0
        elif(selector_position == 2):
            if(ruleset['time_bonus'] < 3600):
                ruleset['time_bonus'] += 300
            else:
                ruleset['time_bonus'] = 0
        elif(selector_position == 3):
            if(ruleset['special_ability_charge_base'] < 20):
                ruleset['special_ability_charge_base'] += 1
            else:
                ruleset['special_ability_charge_base'] = 0
        with open(cwd+'/config/ruleset.txt', 'w') as rulesetdoc:
            rulesetdoc.write(dumps(ruleset))
    if(not timer) and ('p1_ability' in pressed or 'p2_ability' in pressed or 'return' in pressed):
        createSFXEvent('select')
        if(selector_position == len(ruleset)):
            selector_position = 0
            game_state = previous_screen
        elif(selector_position == len(ruleset) - 1):
            ruleset['goal_limit'] = 5
            ruleset['time_limit'] = 3600
            ruleset['time_bonus'] = 600
            ruleset['special_ability_charge_base'] = 1
            ruleset['danger_zone_enabled'] = True
        elif(selector_position == 4):
            ruleset['danger_zone_enabled'] = not(ruleset['danger_zone_enabled'])
        with open(cwd+'/config/ruleset.txt', 'w') as rulesetdoc:
            rulesetdoc.write(dumps(ruleset))
            
    return selector_position, game_state, ruleset
