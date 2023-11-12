import math
from engine.unlocks import return_available_costumes
from engine.game_mode_flags import return_game_mode
class CSS_PLAYER:
    def __init__(self, player = 1, x_pos = 0, y_pos = 0, blob_selector = None):
        self.player = player
        self.menu = CSS_MENU(player, x_pos, y_pos)
        self.cursor = CSS_CURSOR(self, player, x_pos + 100, y_pos + 75)
        self.token = CSS_TOKEN(self, player, x_pos + 100, y_pos + 75, blob_selector)
        self.profile = None
        self.player_type = 'human' # Can be NoneType, "Human", or "Computer"
        self.cpu_level = 5 # Scales from 1-5, or something. 1 is very easy, 5 is max difficulty
        self.game_mode = "classic"

    def update_game_mode(self):
        self.game_mode = return_game_mode()
        if(self.game_mode == "squadball" and type(self.token) != SQUADBALL_TOKEN):
            print("Update")
            self.menu = SQUADBALL_MENU(self.menu.player, self.menu.x_pos, self.menu.y_pos)
            self.token = SQUADBALL_TOKEN(self, self.token.player, self.token.x_pos, self.token.y_pos, self.token.blob_selector)


class CSS_MENU:
    def __init__(self, player, x_pos, y_pos):
        self.player = player
        self.image_cache = {"human": None, "cpu": None, "none":None}
        self.kick_setting = "default"
        self.block_setting = "default"
        self.boost_setting = "default"
        self.x_pos = x_pos
        self.y_pos = y_pos
    
    def set_image(self, image_dict):
        self.image_cache = image_dict

class CSS_CURSOR:
    def __init__(self, player_obj = None, player = 1, x_pos = 0, y_pos = 0):
        self.player = player # player number
        self.player_obj = player_obj
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.x_stick = 0
        self.y_stick = 0
        self.visible = False
        self.held_token = None
        self.called_detach_from_cursor = False
        self.was_clicking = True
        self.clicking = True
        self.snap_clicking = False
        self.current_image = None
        self.idle_image = None
        self.grab_image = None
        self.acceptable_inputs = None
        self.define_acceptable_inputs()
    
    def define_acceptable_inputs(self):
        self.acceptable_inputs = {f"p{self.player}_up", f"p{self.player}_down", f"p{self.player}_left", f"p{self.player}_right", f"p{self.player}_ability", f"p{self.player}_kick", f"p{self.player}_block", f"p{self.player}_boost"}

    def player_interaction(self, input_list):
        self.was_clicking = self.clicking
        self.snap_clicking = False
        pressed = set()
        for key_input in input_list:
            if(str(self.player) in key_input):
                pressed.add(key_input.split("_")[1])
        
        if('left' in pressed):
            self.x_pos -= 10
        elif('right' in pressed):
            self.x_pos += 10

        if('up' in pressed):
            self.y_pos -= 10
        elif('down' in pressed):
            self.y_pos += 10

        if('ability' in pressed):
            self.clicking = True # Ability to select, kick to deselect
        else:
            self.clicking = False
        
        if('kick' in pressed and not self.was_clicking and not self.held_token):
            self.snap_clicking = True

        if(self.x_pos > 1325 and self.x_stick < 30):
            self.x_stick += 1
            self.x_pos = 1325
        elif(self.x_pos > 1325 and self.x_stick >= 30):
            self.x_pos = 0
            self.x_stick = 0
        elif(self.x_pos < 0 and self.x_stick < 30):
            self.x_stick += 1
            self.x_pos = 0
        elif(self.x_pos < 0 and self.x_stick >= 30):
            self.x_pos = 1325
            self.x_stick = 0
        else:
            self.x_stick = 0

        if(self.y_pos > 740 and self.y_stick < 30):
            self.y_stick += 1
            self.y_pos = 740
        elif(self.y_pos > 740 and self.y_stick >= 30):
            self.y_pos = 0
            self.y_stick = 0
        elif(self.y_pos < 0 and self.y_stick < 30):
            self.y_stick += 1
            self.y_pos = 0
        elif(self.y_pos < 0 and self.y_stick >= 30):
            self.y_pos = 740
            self.y_stick = 0
        else:
            self.y_stick = 0

        if(self.held_token):
            self.held_token.track_attached_cursor()

    def dist_to_element(self, other):
        # Mostly for tokens lol
        return math.dist([self.x_pos, self.y_pos], [other.x_pos-25, other.y_pos-25])

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
    def __init__(self, player_obj = None, player = 1, x_pos = 0, y_pos = 0, blob_selector = None):
        self.player_obj = player_obj
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
        self.current_costume = 0
        self.player_state = 'human' # 'human', 'cpu', none'
        self.ps_cycle = {'human': 'cpu', 'cpu': 'none', 'none': 'human'}
        self.image_cache = {"human": None, "cpu": None, "none":None}
        self.toggle_select_cooldown = 0
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
                self.current_costume = 0
                #print("15X")
            else:
                self.current_blob = None
                self.current_blob_x = None
                self.current_blob_y = None
                #print("16X")
                self.current_costume = 0
    
    def update_selected_costume(self):
        self.current_costume += 1
        costumes = return_available_costumes()
        if(self.current_costume >= len(costumes[self.current_blob])):
            self.current_costume = 0

    def check_costume_toggle(self, input_list):
        pressed = set()
        for key_input in input_list:
            if(str(self.player) in key_input):
                pressed.add(key_input.split("_")[1])
        
        # TODO: Stop using return_available_costumes() because it's slow. Ideally, it should be called when entering the CSS
        if('block' in pressed and self.current_blob and not (self.current_blob == 'quirkless' and self.current_blob_x != 0 and self.current_blob_y != 0) and not self.toggle_select_cooldown):
            self.toggle_select_cooldown = 15
            self.update_selected_costume()
            

    def costume_toggle_cooldown(self, input_list):
        # TODO: Just make this a function?
        pressed = set()
        for key_input in input_list:
            if(str(self.player) in key_input):
                pressed.add(key_input.split("_")[1])

        if('block' not in pressed):
            self.toggle_select_cooldown = 0

    def update_player_status(self):
        self.player_state = self.ps_cycle[self.player_state]
        if(self.player_state == "none" and self.attached_to):
            self.attached_to.current_image = self.attached_to.idle_image
            self.detach_from_cursor()

    def set_image(self, image_dict):
        self.image_cache = image_dict

class SQUADBALL_MENU(CSS_MENU):
    def __init__(self, player, x_pos, y_pos):
        super().__init__(player, x_pos, y_pos)
        self.stored_blobs = [] # Array of dicts: {"blob": "quirkless", "costume": 0}
    
    def store_new_blob(self, blob, costume, x, y):
        if(len(self.stored_blobs) < 3):
            self.stored_blobs.append({"blob": blob, "costume": costume, "x": x, "y": y}) # TODO: Handle costumes better
            print(self.stored_blobs)
            return True
        return False

    def remove_blob(self):
        if(len(self.stored_blobs)):
            self.stored_blobs.pop()
        

class SQUADBALL_TOKEN(CSS_TOKEN):
    def detach_from_cursor(self):
        if(self.current_blob and self.player_obj.menu.store_new_blob(self.current_blob, self.current_costume, self.current_blob_x, self.current_blob_y)):
            self.x_pos, self.y_pos = self.player_obj.menu.x_pos + 100, self.player_obj.menu.y_pos + 75
            self.current_blob = None
            self.current_costume = 0 # TODO: You should be able to edit the costume at some point
        elif(self.player_obj.menu.x_pos < self.x_pos < self.player_obj.menu.x_pos + 150 and self.player_obj.menu.y_pos < self.y_pos < self.player_obj.menu.y_pos + 200):
            self.player_obj.menu.remove_blob()
        return super().detach_from_cursor()    
        