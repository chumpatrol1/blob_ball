import pygame as pg
import sys
from os import getenv
from json import loads, dumps

from pygame.constants import K_KP_ENTER
from engine.get_events import get_events
from resources.graphics_engine.display_controller_pop_up import create_controller_pop_up
from resources.graphics_engine.handle_screen_size import return_mouse_wh
from resources.sound_engine.sfx_event import createSFXEvent
import copy
#print(tuple(filter(lambda x: x.startswith("K_"), pg.constants.__dict__.keys())))

pg.init()

# DEFAULT KEYBOARD CONTROLS

input_map = {
    'p1_up': pg.K_w,
    'p1_down': pg.K_s,
    'p1_left': pg.K_a,
    'p1_right': pg.K_d,
    'p1_ability': pg.K_1,
    'p1_kick': pg.K_2,
    'p1_block': pg.K_3,
    'p1_boost': pg.K_4,
    'p2_up': pg.K_UP,
    'p2_down': pg.K_DOWN,
    'p2_left': pg.K_LEFT,
    'p2_right': pg.K_RIGHT,
    'p2_ability': pg.K_n,
    'p2_kick': pg.K_m,
    'p2_block': pg.K_COMMA,
    'p2_boost': pg.K_PERIOD,
}
# INT KEYS MUST BE STRINGS - this is because when saving/loading the controls to file they are stored as strings!
# DEFAULT GAMECUBE CONTROLS - converts button press to an action

gamecube_map = {
    'horizontal_deadzone': 0.3,
    'vertical_deadzone': 0.5,
    'bumper_deadzone': 0.3,
    'rumble': True,
    '0': 'up', # X
    '1': 'ability', # A
    '2': 'kick', # B
    '3': 'down', # Y
    '4': 'block', # L
    '5': 'block', # R
    '6': 'none',
    '7': 'boost', # Z
    '8': 'none',
    '9': 'escape', # HOME
    '10': 'none',
}

xbox360_map = {
    'horizontal_deadzone': 0.3,
    'vertical_deadzone': 0.5,
    'bumper_deadzone': 0.3,
    'rumble': True,
    '0': 'ability', # A
    '1': 'kick', # B
    '2': 'up', # X
    '3': 'down', # Y
    '4': 'block', # L
    '5': 'block', # R
    '6': 'escape', # ?
    '7': 'escape', # Z
    '8': 'none',
    '9': 'none', # HOME
    '10': 'none',
    'lt': 'boost', # LT
    'rt': 'boost', # RT
}

ps3_map = {

}

ps4_map = {

}

switchpro_map = {

}

player_mapping = {
    'GameCube Controller Adapter': dict(gamecube_map),
    'Xbox 360 Controller': dict(xbox360_map),
    'Generic': dict(xbox360_map),
}

original_joystick_mapping = {
    "1": dict(player_mapping),
    "2": dict(player_mapping),
}

mapkey_names = {}
override = {
    '.': 'PERIOD',
    ',': 'COMMA',
    '/': 'FORWARDSLASH',
    ';': 'SEMICOLON',
    '\'': 'SINGLEQUOTE',
    '\\': 'BACKSLASH',
    '[': 'OPENBRACKET',
    ']': 'CLOSEBRACKET',
    '-': 'SUBTRACT',
    '=': 'EQUALS',
}
def update_mapkey_names(input_list, key = None):
    global mapkey_names
    global override
    if(key is None):
        for mapkey in input_list:
            key_name = pg.key.name(input_list[mapkey]).upper()
            if key_name in override:
                mapkey_names[mapkey] = override[key_name]
            else:
                mapkey_names[mapkey] = key_name
            
    else:
        key_name = pg.key.name(input_list[-1]).upper()
        if key_name in override:
            mapkey_names[key] = override[key_name]
        else:
            mapkey_names[key] = key_name

def return_mapkey_names():
    global mapkey_names
    return mapkey_names
joystick_map = {}
def reset_joystick_map():
    global joystick_map
    joystick_map = copy.deepcopy(original_joystick_mapping)
    with open(getenv('APPDATA')+"/BlobBall"+"/config/joysticks.txt", "w") as joy_file:
        joy_file.write(dumps(joystick_map))
    #print(joystick_map)

reset_joystick_map()

try:
    controls = open(getenv('APPDATA')+"/BlobBall"+"/config/controls.txt", "r+")
except:
    with open(getenv('APPDATA')+"/BlobBall"+"/config/controls.txt", "w") as controls:
        controls.write(dumps(input_map))
    controls = open(getenv('APPDATA')+"/BlobBall"+"/config/controls.txt", "r+")

try:
    with open(getenv('APPDATA')+"/BlobBall"+"/config/joysticks.txt", "r+") as joy_file:
        n_joystick_mapping = loads(joy_file.readlines()[0])

    for key in original_joystick_mapping:
        if not key in n_joystick_mapping:
            
            n_joystick_mapping[key] = original_joystick_mapping[key]
        else:
            for joy_button in original_joystick_mapping[key]:
                if not joy_button in n_joystick_mapping[key]:
                    n_joystick_mapping[key][joy_button] = original_joystick_mapping[key][joy_button]

    joystick_map = n_joystick_mapping
    with open(getenv('APPDATA')+"/BlobBall"+"/config/joysticks.txt", "w") as joy_file:
        joy_file.write(dumps(joystick_map))

except Exception as ex:
    with open(getenv('APPDATA')+"/BlobBall"+"/config/joysticks.txt", "w") as joystick_file:
        joystick_file.write(dumps(original_joystick_mapping))
    
    with open(getenv('APPDATA')+"/BlobBall"+"/config/joysticks.txt", "r+") as joy_file:
        joystick_map = loads(joy_file.readlines()[0])

forbidden_keys = [pg.K_ESCAPE, pg.K_LCTRL, pg.K_RCTRL, pg.K_RETURN]

input_map = loads(controls.readlines()[0])
controls.close()


def return_joystick_mapping():
    global joystick_map
    return joystick_map

def bind_to_joy(player, controller, key, value):
    global joystick_map
    joystick_map[player][controller][key] = value
    with open(getenv('APPDATA')+"/BlobBall"+"/config/joysticks.txt", "w") as joystick_file:
        joystick_file.write(dumps(joystick_map))
    


update_mapkey_names(input_map)

temp_binding = []

joysticks = {}
joystick_count = 0
joystick_handler = {
    'p1_joystick': None,
    'p2_joystick': None,
}

def detect_joysticks():
    global joysticks
    global joystick_count
    for event in get_events():
        
        #print(pg.JOYDEVICEADDED)
        if(event.type == pg.JOYDEVICEADDED):
            #print(event)
            jindex = event.__dict__['device_index']
            dindex = pg.joystick.Joystick(jindex).get_instance_id()
            joysticks[dindex] = pg.joystick.Joystick(jindex)
            #print(joysticks[dindex])
            joysticks[dindex].init()
            name = joysticks[dindex].get_name()
            if(name == "GameCube Controller Adapter"):
                name = "GCCA"
            elif(name == "Xbox 360 Controller"):
                name = "XBox 360 Controller"
            else:
                name = "Generic"
            print("Connected", name)
            
            create_controller_pop_up(jindex + 1, name, 0)
            joystick_count += 1
            
        elif(event.type == pg.JOYDEVICEREMOVED): # TODO: Ensure this works correctly for non 4 port adapters
            #print(event)
            dindex = event.__dict__['instance_id']
            jindex = joysticks[dindex].get_id()
            
            name = joysticks[dindex].get_name()
            if(name == "GameCube Controller Adapter"):
                name = "GCCA"
            elif(name == "Xbox 360 Controller"):
                name = "XBox 360 Controller"
            else:
                name = "Generic"
            print("Disconnected", name)
            joystick_count -= 1
            create_controller_pop_up(jindex + 1, name, -1)
            joysticks[dindex].quit()
            del(joysticks[dindex])
            
        
    #print(joysticks)
            

def unbind_inputs(mode = 'all'):
    global input_map
    global temp_binding
    print("MODE", mode)
    if(mode == 'p1'):
        for button in input_map:
            if 'p1' in button:
                pass
                #input_map[button] = 0
        
        for key in input_map:
            if 'p2' in key:
                temp_binding.append(input_map[key])

    elif(mode == 'p2'):
        for button in input_map:
            if 'p2' in button:
                pass
                #input_map[button] = 0
        
        for key in input_map:
            if 'p1' in key:
                temp_binding.append(input_map[key])
    

    elif(mode == 'all'):
        for button in input_map:
            pass
            #input_map[button] = 0
    
    else:
        input_map[mode] = 0
        print(input_map)
        for key in input_map:
            print(key)
            if(key != mode):
                temp_binding.append(input_map[key])

def bind_input(key_to_rebind, last_key):
    global input_map
    global temp_binding
    for event in get_events():
        if event.type == pg.KEYDOWN:
            if(not event.key in temp_binding and not event.key in forbidden_keys):
                input_map[key_to_rebind] = event.key
                temp_binding.append(event.key)
                update_mapkey_names(temp_binding, key=key_to_rebind)
                print(temp_binding)
                if(key_to_rebind == last_key):
                    temp_binding = []
                    with open(getenv('APPDATA')+"/BlobBall"+"/config/controls.txt", "w") as control_list:
                        control_list.write(dumps(input_map))
                else:
                    createSFXEvent('chime_progress')
                return True
            else:
                return False
    else:
        return False

def reset_inputs():
    global input_map
    input_map = {
    'p1_up': pg.K_w,
    'p1_down': pg.K_s,
    'p1_left': pg.K_a,
    'p1_right': pg.K_d,
    'p1_ability': pg.K_1,
    'p1_kick': pg.K_2,
    'p1_block': pg.K_3,
    'p1_boost': pg.K_4,
    'p2_up': pg.K_UP,
    'p2_down': pg.K_DOWN,
    'p2_left': pg.K_LEFT,
    'p2_right': pg.K_RIGHT,
    'p2_ability': pg.K_n,
    'p2_kick': pg.K_m,
    'p2_block': pg.K_COMMA,
    'p2_boost': pg.K_PERIOD,
    }
    update_mapkey_names(input_map)
    with open(getenv('APPDATA')+"/BlobBall"+"/config/controls.txt", "w") as control_list:
                    control_list.write(dumps(input_map))

def bind_gcca_to_player(event, detect_new_controllers, new_controller, controller_name):
    generated_event = -2
    controller_name = "GCCA"
    if(joysticks[event.__dict__['instance_id']].get_button(15) and detect_new_controllers):
        old_joystick = joystick_handler['p1_joystick']
        if(joystick_handler['p1_joystick'] == None): # No Controller Currently Assigned
            joystick_handler['p1_joystick'] = new_controller
            generated_event = 1
            if(joystick_handler['p1_joystick'] == joystick_handler['p2_joystick']):
                # Unassign Port 2's controller if we are swapping the ports of this controller
                generated_event = 3
                joystick_handler['p2_joystick'] = None
            # GENERATE HERE
            create_controller_pop_up(new_controller, controller_name, generated_event)
        else: # P1 already has a controller
            if(new_controller != old_joystick): # If we mash DLeft, nothing will happen
                joystick_handler['p1_joystick'] = new_controller # Assign new controller to P1
                generated_event = 5
                # Check if the controller used to be assigned to P2, or if P2 is empty
                if(new_controller == joystick_handler['p2_joystick']): # True if we swap
                    # P1's old controller is now P2's new controller
                    joystick_handler['p2_joystick'] = old_joystick
                    generated_event = 10 + old_joystick + new_controller
                elif(joystick_handler['p2_joystick'] == None): # True if P2 is currently unbound
                    joystick_handler['p2_joystick'] = old_joystick
                    create_controller_pop_up(old_joystick, controller_name, 2)
                else: # True if we unbound P1's old controller
                    create_controller_pop_up(old_joystick, controller_name, 7)
                create_controller_pop_up(new_controller, controller_name, generated_event)
                # GENERATE HERE
        print(joystick_handler)
        print("Assigned joystick to P1")
        #print(joystick_handler)
    # Right on DPAD
    elif(joysticks[event.__dict__['instance_id']].get_button(13) and detect_new_controllers):    
        #print("test r passed")
        old_joystick = joystick_handler['p2_joystick']
        if(joystick_handler['p2_joystick'] == None):
            joystick_handler['p2_joystick'] = new_controller
            generated_event = 2
            if(joystick_handler['p1_joystick'] == joystick_handler['p2_joystick']):
                generated_event = 4
                joystick_handler['p1_joystick'] = None
            create_controller_pop_up(new_controller, controller_name, generated_event)
        else:
            if(new_controller != old_joystick):
                joystick_handler['p2_joystick'] = new_controller
                generated_event = 6
                if(new_controller == joystick_handler['p1_joystick']):
                    joystick_handler['p1_joystick'] = old_joystick
                    generated_event = 10 + old_joystick + new_controller
                elif(joystick_handler['p1_joystick'] == None):
                    joystick_handler['p1_joystick'] = old_joystick
                    create_controller_pop_up(old_joystick, controller_name, 1)
                else: # True if we unbound P2's old controller
                    create_controller_pop_up(old_joystick, controller_name, 8)
                create_controller_pop_up(new_controller, controller_name, generated_event)
        print(joystick_handler)
        print("Assigned joystick to P2")
        #print(joystick_handler)
    else:
        pass
        #print(joystick_handler)
        #print(new_controller)
    
def bind_xbox_360_to_player(event, detect_new_controllers, new_controller, controller_name):
    generated_event = -2
    controller_name = "XBox 360"
    if(joysticks[event.__dict__['instance_id']].get_hat(0)[0] == -1 and detect_new_controllers):
        old_joystick = joystick_handler['p1_joystick']
        if(joystick_handler['p1_joystick'] == None): # No Controller Currently Assigned
            joystick_handler['p1_joystick'] = new_controller
            generated_event = 1
            if(joystick_handler['p1_joystick'] == joystick_handler['p2_joystick']):
                # Unassign Port 2's controller if we are swapping the ports of this controller
                generated_event = 3
                joystick_handler['p2_joystick'] = None
            # GENERATE HERE
            create_controller_pop_up(new_controller, controller_name, generated_event)
        else: # P1 already has a controller
            if(new_controller != old_joystick): # If we mash DLeft, nothing will happen
                joystick_handler['p1_joystick'] = new_controller # Assign new controller to P1
                generated_event = 5
                # Check if the controller used to be assigned to P2, or if P2 is empty
                if(new_controller == joystick_handler['p2_joystick']): # True if we swap
                    # P1's old controller is now P2's new controller
                    joystick_handler['p2_joystick'] = old_joystick
                    generated_event = 10 + old_joystick + new_controller
                elif(joystick_handler['p2_joystick'] == None): # True if P2 is currently unbound
                    joystick_handler['p2_joystick'] = old_joystick
                    create_controller_pop_up(old_joystick, controller_name, 2)
                else: # True if we unbound P1's old controller
                    create_controller_pop_up(old_joystick, controller_name, 7)
                create_controller_pop_up(new_controller, controller_name, generated_event)
                # GENERATE HERE
        print(joystick_handler)
        print("Assigned joystick to P1")
        #print(joystick_handler)
    # Right on DPAD
    elif(joysticks[event.__dict__['instance_id']].get_hat(0)[0] == 1 and detect_new_controllers):    
        #print("test r passed")
        old_joystick = joystick_handler['p2_joystick']
        if(joystick_handler['p2_joystick'] == None):
            joystick_handler['p2_joystick'] = new_controller
            generated_event = 2
            if(joystick_handler['p1_joystick'] == joystick_handler['p2_joystick']):
                generated_event = 4
                joystick_handler['p1_joystick'] = None
            create_controller_pop_up(new_controller, controller_name, generated_event)
        else:
            if(new_controller != old_joystick):
                joystick_handler['p2_joystick'] = new_controller
                generated_event = 6
                if(new_controller == joystick_handler['p1_joystick']):
                    joystick_handler['p1_joystick'] = old_joystick
                    generated_event = 10 + old_joystick + new_controller
                elif(joystick_handler['p1_joystick'] == None):
                    joystick_handler['p1_joystick'] = old_joystick
                    create_controller_pop_up(old_joystick, controller_name, 1)
                else: # True if we unbound P2's old controller
                    create_controller_pop_up(old_joystick, controller_name, 8)
                create_controller_pop_up(new_controller, controller_name, generated_event)
        print(joystick_handler)
        print("Assigned joystick to P2")
        #print(joystick_handler)
    else:
        pass
        #print(joystick_handler)
        #print(new_controller)

def bind_generic_to_player(event, detect_new_controllers, new_controller, controller_name):
    generated_event = -2
    controller_name = "Generic"
    if(joysticks[event.__dict__['instance_id']].get_hat(0)[0] == -1 and detect_new_controllers):
        old_joystick = joystick_handler['p1_joystick']
        if(joystick_handler['p1_joystick'] == None): # No Controller Currently Assigned
            joystick_handler['p1_joystick'] = new_controller
            generated_event = 1
            if(joystick_handler['p1_joystick'] == joystick_handler['p2_joystick']):
                # Unassign Port 2's controller if we are swapping the ports of this controller
                generated_event = 3
                joystick_handler['p2_joystick'] = None
            # GENERATE HERE
            create_controller_pop_up(new_controller, controller_name, generated_event)
        else: # P1 already has a controller
            if(new_controller != old_joystick): # If we mash DLeft, nothing will happen
                joystick_handler['p1_joystick'] = new_controller # Assign new controller to P1
                generated_event = 5
                # Check if the controller used to be assigned to P2, or if P2 is empty
                if(new_controller == joystick_handler['p2_joystick']): # True if we swap
                    # P1's old controller is now P2's new controller
                    joystick_handler['p2_joystick'] = old_joystick
                    generated_event = 10 + old_joystick + new_controller
                elif(joystick_handler['p2_joystick'] == None): # True if P2 is currently unbound
                    joystick_handler['p2_joystick'] = old_joystick
                    create_controller_pop_up(old_joystick, controller_name, 2)
                else: # True if we unbound P1's old controller
                    create_controller_pop_up(old_joystick, controller_name, 7)
                create_controller_pop_up(new_controller, controller_name, generated_event)
                # GENERATE HERE
        print(joystick_handler)
        print("Assigned joystick to P1")
        #print(joystick_handler)
    # Right on DPAD
    elif(joysticks[event.__dict__['instance_id']].get_hat(0)[0] == 1 and detect_new_controllers):    
        #print("test r passed")
        old_joystick = joystick_handler['p2_joystick']
        if(joystick_handler['p2_joystick'] == None):
            joystick_handler['p2_joystick'] = new_controller
            generated_event = 2
            if(joystick_handler['p1_joystick'] == joystick_handler['p2_joystick']):
                generated_event = 4
                joystick_handler['p1_joystick'] = None
            create_controller_pop_up(new_controller, controller_name, generated_event)
        else:
            if(new_controller != old_joystick):
                joystick_handler['p2_joystick'] = new_controller
                generated_event = 6
                if(new_controller == joystick_handler['p1_joystick']):
                    joystick_handler['p1_joystick'] = old_joystick
                    generated_event = 10 + old_joystick + new_controller
                elif(joystick_handler['p1_joystick'] == None):
                    joystick_handler['p1_joystick'] = old_joystick
                    create_controller_pop_up(old_joystick, controller_name, 1)
                else: # True if we unbound P2's old controller
                    create_controller_pop_up(old_joystick, controller_name, 8)
                create_controller_pop_up(new_controller, controller_name, generated_event)
        print(joystick_handler)
        print("Assigned joystick to P2")
        #print(joystick_handler)
    else:
        pass
        #print(joystick_handler)
        #print(new_controller)

def get_keypress(detect_new_controllers = True, menu_input = True):
    global input_map
    pressed = pg.key.get_pressed()
    events = get_events()
    pressed_array = []
    if(pressed[input_map['p1_up']]):
        pressed_array.append('p1_up')
    if(pressed[input_map['p1_down']]):
        pressed_array.append('p1_down')
    if(pressed[input_map['p1_left']]):
        pressed_array.append('p1_left')
    if(pressed[input_map['p1_right']]):
        pressed_array.append('p1_right')
    if(pressed[input_map['p1_ability']]):
        pressed_array.append('p1_ability')
    if(pressed[input_map['p1_kick']]):
        pressed_array.append('p1_kick')
    if(pressed[input_map['p1_block']]):
        pressed_array.append('p1_block')
    if(pressed[input_map['p1_boost']]):
        pressed_array.append('p1_boost')
    if(pressed[input_map['p2_up']]):
        pressed_array.append('p2_up')
    if(pressed[input_map['p2_down']]):
        pressed_array.append('p2_down')
    if(pressed[input_map['p2_left']]):
        pressed_array.append('p2_left')
    if(pressed[input_map['p2_right']]):
        pressed_array.append('p2_right')
    if(pressed[input_map['p2_ability']]):
        pressed_array.append('p2_ability')
    if(pressed[input_map['p2_kick']]):
        pressed_array.append('p2_kick')
    if(pressed[input_map['p2_block']]):
        pressed_array.append('p2_block')
    if(pressed[input_map['p2_boost']]):
        pressed_array.append('p2_boost')
    if(pressed[pg.K_RETURN]):
        pressed_array.append('return')
    if(pressed[pg.K_ESCAPE]):
        pressed_array.append('escape')
    
    # Handle Joystick Events
    # TODO: Create popup when connecting a new controller
    for event in events:
        if(event.type in {pg.JOYAXISMOTION, pg.JOYHATMOTION}):

            #print(event)
            #print(joysticks)
            #print(joysticks[event.__dict__['instance_id']].get_button(2))
            try:
                new_controller = joysticks[event.__dict__['instance_id']].get_instance_id() - 1 # Get Controller ID
            except KeyError:
                continue
            controller_name = joysticks[event.__dict__['instance_id']].get_name()
            if(controller_name == "Xbox 360 Controller"):
                #print(joysticks[event.__dict__['instance_id']].get_hat(0))
                bind_xbox_360_to_player(event, detect_new_controllers, new_controller, controller_name)
        elif(event.type == pg.JOYBUTTONDOWN):
            #print(event)
            # Assign Controller to Port
            # Left on DPAD
            try:
                new_controller = joysticks[event.__dict__['instance_id']].get_instance_id() - 1 # Get Controller ID
            except KeyError:
                continue
            controller_name = joysticks[event.__dict__['instance_id']].get_name()
            if(controller_name == "GameCube Controller Adapter"):
                bind_gcca_to_player(event, detect_new_controllers, new_controller, controller_name)
                if(joysticks[event.__dict__['instance_id']].get_button(14)): # Down on DPAD
                    pressed_array.append('return')
            elif(controller_name == "Xbox 360 Controller"):
                bind_xbox_360_to_player(event, detect_new_controllers, new_controller, controller_name)
            else:
                print("Unsupported for now!")
            


            

        
    for joystick in joysticks:
        header = ""
        if(joystick - 1 == joystick_handler['p1_joystick']):
            header = "p1_"
            player_key = "1"
        elif(joystick - 1 == joystick_handler['p2_joystick']):
            header = "p2_"
            player_key = "2"
        else:
            continue
        
        if(joysticks[joystick].get_name() in {"GameCube Controller Adapter", "Xbox 360 Controller"}):
            player_joystick = joysticks[joystick].get_name()
        else:
            player_joystick = "Generic"
        # Control Stick
        # TODO: C-Stick Attack(?)
        if(joysticks[joystick].get_axis(0) > joystick_map[player_key][player_joystick]['horizontal_deadzone']):
            #print("Holding Right")
            pressed_array.append(header + "right")
        elif(joysticks[joystick].get_axis(0) < -1 * joystick_map[player_key][player_joystick]['horizontal_deadzone']):
            #print("Holding Left")
            pressed_array.append(header + "left")

        if(joysticks[joystick].get_axis(1) > joystick_map[player_key][player_joystick]['vertical_deadzone']):
            #print("Holding Down")
            pressed_array.append(header + "down")
        elif(joysticks[joystick].get_axis(1) < -1 * joystick_map[player_key][player_joystick]['vertical_deadzone']):
            #print("Holding Up")
            pressed_array.append(header + "up")

        if(player_joystick == "Xbox 360 Controller"):
            if(joysticks[joystick].get_axis(2) > 0.3):
                #print("Holding Down")
                pressed_array.append(header + joystick_map[player_key][player_joystick]['lt'])
            if(joysticks[joystick].get_axis(2) > 0.3):
                #print("Holding Up")
                pressed_array.append(header + joystick_map[player_key][player_joystick]['rt'])

        
        used_map = original_joystick_mapping
        if(not menu_input):
            used_map = joystick_map

        # Buttons
        for button in range(joysticks[joystick].get_numbuttons()):
            if(str(button) in used_map[player_key][player_joystick] and joysticks[joystick].get_button(button)):
                #print(used_map)
                #print(joystick_map == original_joystick_mapping)
                #  and joystick.get_button(button)
                joy_button_pressed = used_map[player_key][player_joystick][str(button)]
                if(joy_button_pressed != "escape"):
                    pressed_array.append(header + used_map[player_key][player_joystick][str(button)])
                else:
                    pressed_array.append('escape')
                
            

        '''if(joystick.get_button(2)): # GC B
            pressed_array.append(header + "kick")
        
        if(joystick.get_button(1)): # GC A 
            pressed_array.append(header + "ability")

        if(joystick.get_button(7)): # GC Z
            pressed_array.append(header + "block")

        if(joystick.get_button(0) or joystick.get_button(3)): # GC X Y
            pressed_array.append(header + "boost")

        if(joystick.get_button(9)): # GC Home Button
            pressed_array.append('escape')
        '''
        # TODO: Shoulder buttons/triggers
        

        
    
    #print(joysticks)
    #print(joysticks[3].get_button(9))
    return pressed_array
button_timer = 0
def merge_inputs(pressed, override = False):
    '''
    Merges the inputs of two players into one set.
    Override: forces inputs to be merged regardless of the button timer being active
    '''
    global button_timer
    merged_press = []
    if not button_timer or override:
        if('p1_up' in pressed or 'p2_up' in pressed):
            merged_press.append('up')
        if('p1_down' in pressed or 'p2_down' in pressed):
            merged_press.append('down')
        if('p1_left' in pressed or 'p2_left' in pressed):
            merged_press.append('left')
        if('p1_right' in pressed or 'p2_right' in pressed):
            merged_press.append('right')
        if('p1_ability' in pressed or 'p2_ability' in pressed):
            merged_press.append('ability')
        if('p1_kick' in pressed or 'p2_kick' in pressed):
            merged_press.append('kick')
        if('p1_block' in pressed or 'p2_block' in pressed):
            merged_press.append('block')
        if('p1_boost' in pressed or 'p2_boost' in pressed):
            merged_press.append('boost')
        if('return' in pressed):
            merged_press.append('return')
    if(len(merged_press)):
        button_timer = 10
    return merged_press

def menu_input(pause_screen = False):
    global button_timer
    pressed = get_keypress()
    selected = False
    if(not pause_screen and ("p1_ability" in pressed or "p2_ability" in pressed or "return" in pressed)):
        selected = True
    elif(pause_screen and "return" in pressed):
        selected = True
    if(pressed == []):
        button_timer = 0
    if(button_timer == 0 and selected):
        button_timer = 30
        return pressed
    elif(button_timer == 0 and not pressed == []):
        button_timer = 15
        return pressed
    else:
        if(button_timer > 0):
            button_timer -= 1
        return []

p1_timer = 0
p2_timer = 1
def css_input(detect_new_controllers = True):
    global button_timer
    if(button_timer == 0):
        return get_keypress(detect_new_controllers = detect_new_controllers)
    else:
        button_timer -= 1
        return []

def player_to_controls(player):
    if(player == 2):
        button_list = {
            'p2_up': 'up',
            'p2_down': 'down',
            'p2_left': 'left',
            'p2_right': 'right',
            'p2_ability': 'ability',
            'p2_kick': 'kick',
            'p2_block': 'block',
            'p2_boost': 'boost'
        }
    else:
        button_list = {
            'p1_up': 'up',
            'p1_down': 'down',
            'p1_left': 'left',
            'p1_right': 'right',
            'p1_ability': 'ability',
            'p1_kick': 'kick',
            'p1_block': 'block',
            'p1_boost': 'boost'
        }
    return button_list

def toggle_fullscreen(force_override = False): # TODO: Override so it works with the settings menu
    
    pressed = pg.key.get_pressed()
    events = get_events()
    if(pressed[pg.K_LCTRL] or pressed[pg.K_RCTRL]):
        return True
    
    for event in events:
        if(event.type == pg.JOYBUTTONDOWN):
            # Up on DPAD
            if(joysticks[event.__dict__['instance_id']].get_name() == "GameCube Controller Adapter" and joysticks[event.__dict__['instance_id']].get_button(12)):
                    return True
        elif(event.type == pg.JOYHATMOTION):
            if(joysticks[event.__dict__['instance_id']].get_name() == "Xbox 360 Controller" and joysticks[event.__dict__['instance_id']].get_hat(0)[1] == 1):
                return True

    if(force_override):
        return True

    return False

def gameplay_input():
    pressed = get_keypress(menu_input = False)
    return pressed

was_pressed = [0, 0, 0]
prev_coords = [0, 0]
def handle_mouse(update = True):
    # What the mouse should give us:
    # Get Pos returns 2 value tuple (X, Y)
    # Get Pressed returns 3 value tuple (L, M, R)
    global was_pressed
    global prev_coords
    screen_size = return_mouse_wh()
    mouse_pos = list(pg.mouse.get_pos())
    mouse_pos[0] = mouse_pos[0] * (1366/screen_size[0])
    mouse_pos[1] = mouse_pos[1] * (768/screen_size[1])

    get_pressed = pg.mouse.get_pressed()
    return_pressed = [0, 0, 0]
    for i in range(len(was_pressed)): # This whole thing is a fancy mouse key up function
        if(was_pressed[i] and not get_pressed[i]):
            return_pressed[i] = was_pressed[i]
    
    moved_mouse = True
    if(prev_coords == mouse_pos):
        moved_mouse = False

    if(update):
        was_pressed = get_pressed
        prev_coords = mouse_pos

    return mouse_pos, return_pressed, moved_mouse

if "__name__" == "__main__":
    while True:
        get_keypress