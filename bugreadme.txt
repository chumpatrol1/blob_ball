How My Code Works!
Open main.py
main.py handles the "game_state" every frame by calling on the function get_game_state (Line 60 of main.py)
engine/game_handler.py accepts the game_state in the update_game_state function (Line 20)
game_state begins out as "control_splash" which shows the splash screen of Blob Ball. update_game_state takes the game_state and then takes the output of splash_navigator(). (Line 36 of game_handler.py)
If the game_state is instead "main_menu", it will handle that on Line 40.

Once we return game_state and info_getter from update_game_state to main.py, we then pass this information along to display_graphics (Line 77). display_graphics.py (under the resources folder) passes this information into draw_splash_screen or draw_main_menu (Lines 57 and 59 respectively). This information is then used to draw onto the screen.

DRAW MAIN MENU IS WHERE WE ARE DOING EXPERIMENTS. THE FILE IS UNDER RESOURCES/GRAPHICS_ENGINE/DISPLAY_MAIN_MENU.PY

Other stuff: Press ESC to quit, the menu has been disabled probably. LCTRL and RCTRL toggles fullscreen.