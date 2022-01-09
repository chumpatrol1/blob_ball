import ctypes

def initialize_screen_size():
    global real_screen_size
    try:
        user32 = ctypes.windll.user32
        real_screen_size = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)
    except:
        print("Real Screen Size Exception")
        real_screen_size = (960, 540)
    
    return real_screen_size

def update_width_and_height(width, height):
    global display_width
    global display_height
    global mouse_dh
    global mouse_dw
    display_height = height
    display_width = width
    mouse_dw = width
    mouse_dh = height

def update_mouse_wh(width, height):
    global mouse_dh
    global mouse_dw
    mouse_dw = width
    mouse_dh = height

real_screen_size = initialize_screen_size()
display_width = 1024
display_height = 576
mouse_dw = 1024
mouse_dh = 576


def return_real_screen_size():
    global real_screen_size
    return real_screen_size

def return_width_and_height():
    global display_height
    global display_width
    return display_width, display_height

def return_mouse_wh():
    global mouse_dw
    global mouse_dh
    return mouse_dw, mouse_dh