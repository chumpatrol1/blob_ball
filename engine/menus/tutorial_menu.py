'''
engine/menus/tutorial_menu.py

An unused file slated for deletion.

> handle_tutorial_menu(): Looks like it was meant to be a menu to access the tutorial
'''
player_ready = False

def handle_tutorial_menu():
    '''
    Does nothing

    Outputs:
        - game_state [str]: Defaults to 'tutorial_complete'
        - info_getter [array]
    '''    
    if(not player_ready):
        game_state = "tutorial_complete"
    else:
        game_state = "main_menu"
        player_ready = False
    return game_state, []
