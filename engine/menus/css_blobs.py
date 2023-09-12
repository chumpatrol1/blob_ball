from engine.unlocks import return_css_selector_blobs
from engine.button import Button
class CSS_BLOBS:
    def __init__(self):
        #self.blobs = return_css_selector_blobs()
        self.buttons = []
        #print(self.blobs)
        for y in range(1, 5):
            y_align = (100+ 768*(y * (100/768)) - (768*(130/768)))
            for x in range(1, 10):
                x_align = 1366*(x/10)-(1366*(50/1366))
                self.buttons.append(Button(y_align, y_align + 95, x_align, x_align + 133))
        '''for button in self.buttons:
            print(button)'''

    def check_buttons(self, token):
        token_to_mouse = [[token.x_pos, token.y_pos]]
        button_y = 0
        button_x = 0
        for button in self.buttons:
            if(button.check_hover(token_to_mouse)):
                return return_css_selector_blobs()[button_y][button_x]