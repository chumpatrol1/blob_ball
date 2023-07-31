class em_base_class:
    def __init__(self, player = 0, affects = set(), species = "", random_image = 0, x_pos = 0, y_pos = 0, x_speed = 0, y_speed = 0, gravity = 0, ground_clip = False, lifetime = 60, hp = 1, special_functions = []):
        self.player = player # 0 is a general hazard spawned by the stage, else player # spawned it
        '''
        'self': affects only the player that spawned it
        'team': affects only teammates
        'enemy': affects only the enemy
        'ball': affects only the ball
        '''
        self.affects = affects # Empty set means it affects no one - adding things to it increases # of targets
        self.species = species # Different species means it has a different effect
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.x_speed = x_speed
        self.y_speed = y_speed
        self.gravity = gravity
        self.ground_clip = ground_clip
        self.lifetime = lifetime
        self.max_lifetime = lifetime
        self.random_image = random_image
        self.hp = hp
        
        self.special_functions = special_functions # Needs to always be a list.

    def update(self):
        self.x_pos += self.x_speed
        self.y_pos += self.y_speed
        #if(self.y_pos > 685 - self.image.get_height()/2 and not self.ground_clip):
        #    self.y_pos = 685 - self.image.get_height()/2
        self.y_speed += self.gravity
        self.lifetime -= 1