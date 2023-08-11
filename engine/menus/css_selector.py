class CSS_PLAYER:
    def __init__(self, player = 1, x_pos = 0, y_pos = 0):
        self.menu = CSS_MENU()
        self.cursor = CSS_CURSOR(player, x_pos, y_pos)
        self.token = CSS_TOKEN()
        self.profile = None
        self.player_type = None # Can be NoneType, "Human", or "Computer"
        self.cpu_level = 5 # Scales from 1-5, or something. 1 is very easy, 5 is max difficulty

class CSS_MENU:
    def __init__(self):
        self.player = None
        self.kick_setting = "default"
        self.block_setting = "default"
        self.boost_setting = "default"

class CSS_CURSOR:
    def __init__(self, player = 1, x_pos = 0, y_pos = 0):
        self.player = player
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.x_stick = 0
        self.y_stick = 0
        self.visible = False
        self.held_token = None
        self.clicking = False
        self.current_image = None
        self.acceptable_inputs = None
        self.define_acceptable_inputs()
    
    def define_acceptable_inputs(self):
        self.acceptable_inputs = {f"p{self.player}_up", f"p{self.player}_down", f"p{self.player}_left", f"p{self.player}_right", f"p{self.player}_ability", f"p{self.player}_kick", f"p{self.player}_block", f"p{self.player}_boost"}

    def player_interaction(self, input_list):
        pressed = set()
        for key_input in input_list:
            if(str(self.player) in key_input):
                pressed.add(key_input.split("_")[1])
        
        if('left' in pressed):
            self.x_pos -= 1
        elif('right' in pressed):
            self.x_pos += 1

        if('up' in pressed):
            self.y_pos -= 1
        elif('down' in pressed):
            self.y_pos += 1

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
            self.y_stick  =0
class CSS_TOKEN:
    def __init__(self):
        self.player = None
        self.x_pos = None
        self.y_pos = None
        self.visible = False
        self.interactable_by_all = False
        self.is_cpu = False
        self.on_blob = False # True if placed on a blob to select it.
        self.current_image = None