class Button:
    def __init__(self, top = 0, bottom = 10, left = 0, right = 10):
        self.top = top
        self.bottom = bottom
        self.left = left
        self.right = right
    
    def check_hover(self, mouse):
        if(mouse[0][0] >= self.left and mouse[0][0] < self.right\
            and mouse[0][1] >= self.top and mouse[0][1] < self.bottom):
            return True
        return False

    def check_click(self, mouse):
        return mouse[1][0] or mouse[1][1] or mouse[1][2]

    def check_left_click(self, mouse):
        return mouse[1][0]

    def check_middle_click(self, mouse):
        return mouse[1][1]

    def check_right_click(self, mouse):
        return mouse[1][2]