import engine.handle_input
selector_position = [0, 0]
def medal_navigation(timer):
    pressed = engine.handle_input.css_input()
    pressed = engine.handle_input.merge_inputs(pressed)
    global selector_position
    game_state = "medals"
    if('ability' in pressed):
        game_state = "almanac"
        selector_position = [0, 0]
    return game_state, selector_position