import math
class CSS_PLAYER:
    def __init__(self, player = 1, x_pos = 0, y_pos = 0, blob_selector = None):
        self.menu = CSS_MENU(player, x_pos, y_pos)
        self.cursor = CSS_CURSOR(player, x_pos + 65, y_pos + 75)
        self.token = CSS_TOKEN(player, x_pos + 65, y_pos + 75, blob_selector)
        self.profile = None
        self.player_type = None # Can be NoneType, "Human", or "Computer"
        self.cpu_level = 5 # Scales from 1-5, or something. 1 is very easy, 5 is max difficulty

class CSS_MENU:
    def __init__(self, player, x_pos, y_pos):
        self.player = player
        self.kick_setting = "default"
        self.block_setting = "default"
        self.boost_setting = "default"
        self.x_pos = x_pos
        self.y_pos = y_pos

class CSS_CURSOR:
    def __init__(self, player = 1, x_pos = 0, y_pos = 0):
        self.player = player
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.x_stick = 0
        self.y_stick = 0
        self.visible = False
        self.held_token = None
        self.was_clicking = False
        self.clicking = False
        self.current_image = None
        self.idle_image = None
        self.grab_image = None
        self.acceptable_inputs = None
        self.define_acceptable_inputs()
    
    def define_acceptable_inputs(self):
        self.acceptable_inputs = {f"p{self.player}_up", f"p{self.player}_down", f"p{self.player}_left", f"p{self.player}_right", f"p{self.player}_ability", f"p{self.player}_kick", f"p{self.player}_block", f"p{self.player}_boost"}

    def player_interaction(self, input_list):
        self.was_clicking = self.clicking

        pressed = set()
        for key_input in input_list:
            if(str(self.player) in key_input):
                pressed.add(key_input.split("_")[1])
        
        if('left' in pressed):
            self.x_pos -= 4
        elif('right' in pressed):
            self.x_pos += 4

        if('up' in pressed):
            self.y_pos -= 4
        elif('down' in pressed):
            self.y_pos += 4

        if('ability' in pressed):
            self.clicking = True # Ability to select, kick to deselect
        else:
            self.clicking = False

        if('kick' in pressed and self.held_token):
            self.clicking = True
            self.was_clicking = False

        if(self.x_pos > 1366 and self.x_stick < 30):
            self.x_stick += 1
            self.x_pos = 1366
        elif(self.x_pos > 1366 and self.x_stick >= 30):
            self.x_pos = 0
            self.x_stick = 0
        elif(self.x_pos < 0 and self.x_stick < 30):
            self.x_stick += 1
            self.x_pos = 0
        elif(self.x_pos < 0 and self.x_stick >= 30):
            self.x_pos = 1366
            self.x_stick = 0
        else:
            self.x_stick = 0

        if(self.y_pos > 768 and self.y_stick < 30):
            self.y_stick += 1
            self.y_pos = 768
        elif(self.y_pos > 768 and self.y_stick >= 30):
            self.y_pos = 0
            self.y_stick = 0
        elif(self.y_pos < 0 and self.y_stick < 30):
            self.y_stick += 1
            self.y_pos = 0
        elif(self.y_pos < 0 and self.y_stick >= 30):
            self.y_pos = 768
            self.y_stick = 0
        else:
            self.y_stick = 0

        if(self.held_token):
            self.held_token.track_attached_cursor()

    def dist_to_element(self, other):
        return math.dist([self.x_pos, self.y_pos], [other.x_pos, other.y_pos])

    def follow_mouse(self, mouse):
        self.x_pos = mouse[0]
        self.y_pos = mouse[1]

        if(self.held_token):
            self.held_token.track_attached_cursor()
    
    def set_image(self, idle, grab):
        self.idle_image = idle
        self.grab_image = grab
        self.current_image = self.idle_image
        print(self.current_image, self.player)


class CSS_TOKEN:
    def __init__(self, player = 1, x_pos = 0, y_pos = 0, blob_selector = None):
        self.player = player
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.visible = True
        self.interactable_by_all = False
        self.is_cpu = False
        self.on_blob = False # True if placed on a blob to select it.
        self.current_image = None
        self.current_blob = None
        self.current_blob_x = None
        self.current_blob_y = None
        self.attached_to = None # Is this attached to a cursor?
        self.blob_selector = blob_selector

    def attach_to_cursor(self, cursor):
        self.attached_to = cursor
        cursor.held_token = self

    def detach_from_cursor(self):
        self.attached_to.held_token = None
        self.attached_to = None
        

    def track_attached_cursor(self):
        if(self.attached_to):
            self.x_pos = self.attached_to.x_pos
            self.y_pos = self.attached_to.y_pos
            button_tuple = self.blob_selector.check_buttons(self)
            if(button_tuple):
                self.current_blob = button_tuple[0]
                self.current_blob_x = button_tuple[1]
                self.current_blob_y = button_tuple[2]
            else:
                self.current_blob = None
                self.current_blob_x = None
                self.current_blob_y = None
            