player_ready = False

def handle_tutorial_menu():
    
    if(not player_ready):
        game_state = "tutorial_complete"
    else:
        game_state = "main_menu"
        player_ready = False
    return game_state, []
