from engine.controller_mappings.cycle_dicts import cycle_left_dict, cycle_right_dict
def generic_left(selector_position, bind_to_joy_arr, current_mapping):
    if(selector_position == 0): # H Dead
        bind_to_joy_arr[2] = 'horizontal_deadzone'
        value = current_mapping['horizontal_deadzone']
        value = round(value - 0.1, 1)
        if(value < 0.1):
            value = 0.8
        bind_to_joy_arr[3] = value
        
        
    elif(selector_position == 1): # V Dead
        bind_to_joy_arr[2] = 'vertical_deadzone'
        value = current_mapping['vertical_deadzone']
        value = round(value - 0.1, 1)
        if(value < 0.1):
            value = 0.8
        bind_to_joy_arr[3] = value
        

    elif(selector_position == 2): # B0
        bind_to_joy_arr[2] = '0'
        value = current_mapping['0']
        value = cycle_left_dict[value]
        bind_to_joy_arr[3] = value
        
    elif(selector_position == 3): # B1
        bind_to_joy_arr[2] = '1'
        value = current_mapping['1']
        value = cycle_left_dict[value]
        bind_to_joy_arr[3] = value
        
    elif(selector_position == 4): # B2
        bind_to_joy_arr[2] = '2'
        value = current_mapping['2']
        value = cycle_left_dict[value]
        bind_to_joy_arr[3] = value
        
    elif(selector_position == 5): # B3
        bind_to_joy_arr[2] = '3'
        value = current_mapping['3']
        value = cycle_left_dict[value]
        bind_to_joy_arr[3] = value
        
    elif(selector_position == 6): # B4
        bind_to_joy_arr[2] = '4'
        value = current_mapping['4']
        value = cycle_left_dict[value]
        bind_to_joy_arr[3] = value
        
    elif(selector_position == 7): # B5
        bind_to_joy_arr[2] = '5'
        value = current_mapping['5']
        value = cycle_left_dict[value]
        bind_to_joy_arr[3] = value
        
    elif(selector_position == 8): # LT
        bind_to_joy_arr[2] = 'lt'
        value = current_mapping['lt']
        value = cycle_left_dict[value]
        bind_to_joy_arr[3] = value
        
    elif(selector_position == 9): # RT
        bind_to_joy_arr[2] = 'rt'
        value = current_mapping['rt']
        value = cycle_left_dict[value]
        bind_to_joy_arr[3] = value
        
    elif(selector_position == 10): # Rumble
        bind_to_joy_arr[2] = 'rumble'
        value = current_mapping['rumble']
        value = not value
        bind_to_joy_arr[3] = value

def generic_right(selector_position, bind_to_joy_arr, current_mapping):
    if(selector_position == 0): # H Dead
        bind_to_joy_arr[2] = 'horizontal_deadzone'
        value = current_mapping['horizontal_deadzone']
        value = round(value + 0.1, 1)
        if(value > 0.8):
            value = 0.1
        bind_to_joy_arr[3] = value
        
        
    elif(selector_position == 1): # V Dead
        bind_to_joy_arr[2] = 'vertical_deadzone'
        value = current_mapping['vertical_deadzone']
        value = round(value + 0.1, 1)
        if(value > 0.8):
            value = 0.1
        bind_to_joy_arr[3] = value
        

    elif(selector_position == 2): # A
        bind_to_joy_arr[2] = '0'
        value = current_mapping['0']
        value = cycle_right_dict[value]
        bind_to_joy_arr[3] = value
        
    elif(selector_position == 3): # B
        bind_to_joy_arr[2] = '1'
        value = current_mapping['1']
        value = cycle_right_dict[value]
        bind_to_joy_arr[3] = value
        
    elif(selector_position == 4): # X
        bind_to_joy_arr[2] = '2'
        value = current_mapping['2']
        value = cycle_right_dict[value]
        bind_to_joy_arr[3] = value
        
    elif(selector_position == 5): # Y
        bind_to_joy_arr[2] = '3'
        value = current_mapping['3']
        value = cycle_right_dict[value]
        bind_to_joy_arr[3] = value
        
    elif(selector_position == 6): # Left Bumper
        bind_to_joy_arr[2] = '4'
        value = current_mapping['4']
        value = cycle_right_dict[value]
        bind_to_joy_arr[3] = value
        
    elif(selector_position == 7): # Right Bumper
        bind_to_joy_arr[2] = '5'
        value = current_mapping['5']
        value = cycle_right_dict[value]
        bind_to_joy_arr[3] = value
        
    elif(selector_position == 8): # Left Trigger
        bind_to_joy_arr[2] = 'lt'
        value = current_mapping['lt']
        value = cycle_right_dict[value]
        bind_to_joy_arr[3] = value
        
    elif(selector_position == 9): # Right Trigger
        bind_to_joy_arr[2] = 'rt'
        value = current_mapping['rt']
        value = cycle_right_dict[value]
        bind_to_joy_arr[3] = value
        
    elif(selector_position == 10): # Rumble
        bind_to_joy_arr[2] = 'rumble'
        value = current_mapping['rumble']
        value = not value
        bind_to_joy_arr[3] = value