class Button:
    def __init__(self, top = 0, bottom = 10, left = 0, right = 10, state = 'idle'):
        self.top = top
        self.bottom = bottom
        self.left = left
        self.right = right
        self.surfaces = {'idle': None, 'hover': None, 'click': None, 'disabled': None}
        self.state = state # Can be "idle", "hover", or "click"
    
    def check_hover(self, mouse, update_override = False):
        if(mouse[0][0] >= self.left and mouse[0][0] < self.right\
            and mouse[0][1] >= self.top and mouse[0][1] < self.bottom):
            if(not update_override):
                self.state = "hover"
            return True
        if(not update_override):
            self.state = "idle"
        return False

    def check_click(self, mouse):
        return mouse[1][0] or mouse[1][1] or mouse[1][2]

    def check_left_click(self, mouse):
        return mouse[1][0]

    def check_middle_click(self, mouse):
        return mouse[1][1]

    def check_right_click(self, mouse):
        return mouse[1][2]
    
    def check_button_enabled(self):
        return not self.state == "disabled"

    def __repr__(self):
        return f"Left: {self.left}, Top: {self.top}, Width: {self.right - self.left}, Height: {self.bottom - self.top}"