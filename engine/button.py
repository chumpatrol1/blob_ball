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