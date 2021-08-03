class Particle:
    def __init__(self, image = "", alpha = 0, x_pos = 0, y_pos = 0, x_speed = 0, y_speed = 0, gravity = 0, fade = 5, lifetime = 60, ground_clip = False):
        self.image = image
        self.alpha = alpha
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.x_speed = x_speed
        self.y_speed = y_speed
        self.gravity = gravity
        self.fade = fade
        self.lifetime = lifetime
        self.ground_clip = ground_clip

    def update(self):
        self.alpha -= self.fade
        self.x_pos += self.x_speed
        self.y_pos += self.y_speed
        if(self.y_pos > 685 - self.image.get_height()/2 and not self.ground_clip):
            self.y_pos = 685 - self.image.get_height()/2
        self.y_speed += self.gravity
        self.lifetime -= 1

