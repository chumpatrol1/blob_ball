from engine.handle_input import bind_input as bind_input
from engine.handle_input import unbind_inputs as unbind_inputs

# God forbid I made spaghetti

rebind_array = ['p1_up', 'p1_down', 'p1_left', 'p1_right', 'p1_ability', 'p1_kick', 'p1_block', 'p1_boost',
'p2_up', 'p2_down', 'p2_left', 'p2_right', 'p2_ability', 'p2_kick', 'p2_block', 'p2_boost',
    ]
rebind_number = -1

def handle_rebinding():
    global rebind_number
    game_state = "rebind"

    if(rebind_number == -1):
        unbind_inputs()
        rebind_number = 0

    if(bind_input(rebind_array[rebind_number])):
        rebind_number += 1
        if(rebind_number == 16):
            game_state = "settings"
            rebind_number = -1
    
    rebind_key = rebind_array[rebind_number]

    return game_state, rebind_key