import math
import os
cwd = os.getcwd()

def type_to_stars(type):
    '''
    max_hp: The most HP a blob has (the amount they start each round with)
    top_speed: The fastest that a blob can naturally accelerate to in the ground/air
    traction: The rate at which a blob accelerates on the ground, or the amount that they decelerate when no key is held
    friction: The rate at which a blob accelerates in the air, or the amount that they decelerate when no key is held
    jump_force: Affects the jump height of a blob (Gravity should not affect this)
    gravity: Affects how long it takes for a blob to get back to the ground after jumping. 
    kick_cooldown_rate: Affects how long it takes for a kick to cool down
    block_cooldown_rate: Affects how long it takes for a block to cool down
    boost_cost: Affects the cost of using a boost
    boost_cooldown_rate: Affects how long it takes for a boost to cool down
    boost_duration: The amount of time that a stat boost lasts
    special_ability: The type of SA a blob has
    special_ability_cost: The amount that using a special ability costs
    speical_ability_max: The most special ability that can be stored at once
    special_ability_cooldown: The time between special ability uses. 0 means that it can be held down.
    '''
    if(type == "quirkless"):
        blob_dict = {
            'max_hp': 4,
            'top_speed': 4,
            'traction': 4,
            'friction': 4,
            'gravity': 4,
            'kick_cooldown_rate': 4,
            'boost_cost': 300,
            'block_cooldown_rate': 4,
            'boost_cooldown_rate': 4,
            'boost_duration': 4,
            'special_ability': 'boost',
            'special_ability_cost': 300,
            'special_ability_max': 1800,
            'special_ability_cooldown': 300
        }
    return blob_dict

def type_to_image(type):
    global cwd
    print("The type is...")
    print(type)
    image_dict = {
        "quirkless": cwd+"\\resources\\images\\blobs\\quirkless_blob.png"
    }

    return image_dict[type]

class blob:
    def __init__(self, type = "quirkless", x_pos = 50, y_pos = 1200, facing = 'left', player = 1):
        self.type = type
        self.player = player #Player 1 or 2
        self.image = type_to_image(type)
        stars = type_to_stars(type) #Gets many values for each blob
        self.max_hp = stars['max_hp'] + 2 #Each star adds an additional HP.
        self.hp = self.max_hp
        self.top_speed = 10+(1*stars['top_speed']) #Each star adds some speed
        self.x_speed = 0
        self.y_speed = 0
        self.x_pos = x_pos #Where the blob is on the X axis
        self.y_pos = y_pos #Where the blob is on the Y axis, 1200 is grounded
        self.x_center = x_pos + 80
        self.y_center = y_pos + 110
        self.facing = facing #Where the blob is currently facing
        self.traction = 0.2 + (stars['traction'] * 0.15) #Each star increases traction
        self.friction = 0.2 + (stars['friction'] * 0.15) #Each star increases
        self.gravity_stars = round(.3 + (stars['gravity'] * .15), 3) #Each star increases gravity
        self.gravity_mod = round(.3 + (stars['gravity'] + 3) * .15, 3) #Fastfalling increases gravity
        self.fastfalling = False
        self.jump_force = 14.5 + (stars['gravity'] * 2) #Initial velocity is based off of gravity
        self.kick_cooldown_rate = stars['kick_cooldown_rate'] #Each star reduces kick cooldown
        self.kick_cooldown = 0
        self.block_cooldown_rate = stars['block_cooldown_rate'] #Each star reduces block cooldown
        self.block_cooldown = 0
        self.boost_cost = stars['boost_cost'] #How much SA meter must be spent to boost
        self.boost_cooldown_rate = stars['boost_cooldown_rate'] #Each star reduces boost cooldown
        self.boost_cooldown = 0 #Each star reduces time between boosts
        self.boost_duration = stars['boost_duration'] #Each star increases boost duration
        self.focus_lock = 0 #Timer that locks movement when a blob is focusing
        self.special_ability = stars['special_ability'] #Special Ability of a Blob
        self.special_ability_max = stars['special_ability_max'] #Highest that the SA gauge can go
        self.special_ability_cost = stars['special_ability_cost'] #Price to use SA
        self.special_ability_charge = 1 #Each frame increases the SA meter by 1 point, or more if focusing
    
    def reset(self, player):
        self.hp = self.max_hp
        self.x_speed = 0
        self.y_speed = 0
        if(player == 1):
            self.x_pos = 100
            self.facing = 'right'
        else:
            self.x_pos = 1600
            self.facing = 'left'
        
    def move(self, pressed):
        if(self.player == 1):

            #HORIZONTAL MOVEMENT
            if(self.y_pos == 1200): #Applies traction if grounded
                if('p1_left' in pressed and not 'p1_right' in pressed): #If holding left but not right
                    self.facing = "left"
                    if(self.x_pos <= 0): #Are we in danger of going off screen?
                        self.x_speed = 0
                        self.x_pos = 0
                    else:
                        if(abs(self.x_speed) < self.top_speed):
                            self.x_speed -= self.traction #Accelerate based off of traction
                        else:
                            self.x_speed = -1*self.top_speed #If at max speed, maintain it
                elif(not 'p1_left' in pressed and 'p1_right' in pressed): #If holding right but not left
                    self.facing = 'right'
                    if(self.x_pos >= 1700): #Are we in danger of going off screen?
                        self.x_speed = 0
                        self.x_pos = 1700
                    else:
                        if(abs(self.x_speed) < self.top_speed):
                            self.x_speed += self.traction #Accelerate based off of traction
                        else:
                            self.x_speed = self.top_speed #If at max speed, maintain it
                else: #We're either not holding anything, or pressing both at once
                    if(self.x_speed < 0): #If we're going left, decelerate
                        if(self.x_speed + self.traction) > 0:
                            self.x_speed = 0 #Ensures that we don't decelerate and start moving backwards
                        else:
                            self.x_speed += self.traction #Normal deceleration
                    elif(self.x_speed > 0):
                        if(self.x_speed - self.traction) < 0:
                            self.x_speed = 0 #Ensures that we don't decelerate and start moving backwards
                        else:
                            self.x_speed -= self.traction #Normal deceleration
            else: #Applies friction if airborne
                if('p1_left' in pressed and not 'p1_right' in pressed): #If holding left but not right
                    self.facing = "left"
                    if(self.x_pos <= 0): #Are we in danger of going off screen?
                        self.x_speed = 0
                        self.x_pos = 0
                    else:
                        if(abs(self.x_speed) < self.top_speed):
                            self.x_speed -= self.friction #Accelerate based off of traction
                        else:
                            self.x_speed = -1*self.top_speed #If at max speed, maintain it
                elif(not 'p1_left' in pressed and 'p1_right' in pressed): #If holding right but not left
                    self.facing = 'right'
                    if(self.x_pos >= 1700): #Are we in danger of going off screen?
                        self.x_speed = 0
                        self.x_pos = 1700
                    else:
                        if(abs(self.x_speed) < self.top_speed):
                            self.x_speed += self.friction #Accelerate based off of friction
                        else:
                            self.x_speed = self.top_speed #If at max speed, maintain it
                else: #We're either not holding anything, or pressing both at once
                    if(self.x_speed < 0): #If we're going left, decelerate
                        if(self.x_speed + self.friction) > 0:
                            self.x_speed = 0 #Ensures that we don't decelerate and start moving backwards
                        else:
                            self.x_speed += self.friction #Normal deceleration
                    elif(self.x_speed > 0):
                        if(self.x_speed - self.friction) < 0:
                            self.x_speed = 0 #Ensures that we don't decelerate and start moving backwards
                        else:
                            self.x_speed -= self.friction #Normal deceleration
            self.x_pos += self.x_speed #This ensures that we are always adjusting our position
            if(self.x_pos <= 0): #Don't move off screen!
                self.x_speed = 0
                self.x_pos = 0
            elif(self.x_pos >= 1700): #Don't move off screen!
                self.x_speed = 0
                self.x_pos = 1700
            
            #VERTICAL MOVEMENT
            if('p1_up' in pressed and self.y_pos == 1200): #If you press jump while grounded, jump!
                self.y_speed = -1 * self.jump_force
            if('p1_down' in pressed and self.y_pos < 1200): #If you are above ground and press down
                self.fastfalling = True #Fast fall, increasing your gravity by 3 stars
            if(self.y_pos < 1200): #Applies gravity while airborne, respecting fast fall status.
                if(self.fastfalling):
                    self.y_speed += self.gravity_mod
                else:
                    self.y_speed += self.gravity_stars
            if(self.fastfalling and self.y_pos == 1200): #If you land, cancel the fastfall.
                self.fastfalling = False
            self.y_pos += self.y_speed #This ensures that we are always adjusting our position
            if(self.y_pos < 0): #How did we get here?
                self.y_pos = 0
                self.y_speed = 0
            if(self.y_pos > 1200): #Don't go under the floor!
                self.y_speed = 0
                self.y_pos = 1200
        
        if(self.player == 2):
            
            #HORIZONTAL MOVEMENT
            if(self.y_pos == 1200): #Applies traction if grounded
                if('p2_left' in pressed and not 'p2_right' in pressed): #If holding left but not right
                    self.facing = "left"
                    if(self.x_pos <= 0): #Are we in danger of going off screen?
                        self.x_speed = 0
                        self.x_pos = 0
                    else:
                        if(abs(self.x_speed) < self.top_speed):
                            self.x_speed -= self.traction #Accelerate based off of traction
                        else:
                            self.x_speed = -1*self.top_speed #If at max speed, maintain it
                elif(not 'p2_left' in pressed and 'p2_right' in pressed): #If holding right but not left
                    self.facing = 'right'
                    if(self.x_pos >= 1700): #Are we in danger of going off screen?
                        self.x_speed = 0
                        self.x_pos = 1700
                    else:
                        if(abs(self.x_speed) < self.top_speed):
                            self.x_speed += self.traction #Accelerate based off of traction
                        else:
                            self.x_speed = self.top_speed #If at max speed, maintain it
                else: #We're either not holding anything, or pressing both at once
                    if(self.x_speed < 0): #If we're going left, decelerate
                        if(self.x_speed + self.traction) > 0:
                            self.x_speed = 0 #Ensures that we don't decelerate and start moving backwards
                        else:
                            self.x_speed += self.traction #Normal deceleration
                    elif(self.x_speed > 0):
                        if(self.x_speed - self.traction) < 0:
                            self.x_speed = 0 #Ensures that we don't decelerate and start moving backwards
                        else:
                            self.x_speed -= self.traction #Normal deceleration
            else: #Applies friction if airborne
                if('p2_left' in pressed and not 'p2_right' in pressed): #If holding left but not right
                    self.facing = "left"
                    if(self.x_pos <= 0): #Are we in danger of going off screen?
                        self.x_speed = 0
                        self.x_pos = 0
                    else:
                        if(abs(self.x_speed) < self.top_speed):
                            self.x_speed -= self.friction #Accelerate based off of traction
                        else:
                            self.x_speed = -1*self.top_speed #If at max speed, maintain it
                elif(not 'p2_left' in pressed and 'p2_right' in pressed): #If holding right but not left
                    self.facing = 'right'
                    if(self.x_pos >= 1700): #Are we in danger of going off screen?
                        self.x_speed = 0
                        self.x_pos = 1700
                    else:
                        if(abs(self.x_speed) < self.top_speed):
                            self.x_speed += self.friction #Accelerate based off of friction
                        else:
                            self.x_speed = self.top_speed #If at max speed, maintain it
                else: #We're either not holding anything, or pressing both at once
                    if(self.x_speed < 0): #If we're going left, decelerate
                        if(self.x_speed + self.friction) > 0:
                            self.x_speed = 0 #Ensures that we don't decelerate and start moving backwards
                        else:
                            self.x_speed += self.friction #Normal deceleration
                    elif(self.x_speed > 0):
                        if(self.x_speed - self.friction) < 0:
                            self.x_speed = 0 #Ensures that we don't decelerate and start moving backwards
                        else:
                            self.x_speed -= self.friction #Normal deceleration
            self.x_pos += self.x_speed #This ensures that we are always adjusting our position
            if(self.x_pos <= 0): #Don't move off screen!
                self.x_speed = 0
                self.x_pos = 0
            elif(self.x_pos >= 1700): #Don't move off screen!
                self.x_speed = 0
                self.x_pos = 1700
            
            #VERTICAL MOVEMENT
            if('p2_up' in pressed and self.y_pos == 1200): #If you press jump while grounded, jump!
                self.y_speed = -1 * self.jump_force
            if('p2_down' in pressed and self.y_pos < 1200): #If you are above ground and press down
                self.fastfalling = True #Fast fall, increasing your gravity by 3 stars
            if(self.y_pos < 1200): #Applies gravity while airborne, respecting fast fall status.
                if(self.fastfalling):
                    self.y_speed += self.gravity_mod
                else:
                    self.y_speed += self.gravity_stars
            if(self.fastfalling and self.y_pos == 1200): #If you land, cancel the fastfall.
                self.fastfalling = False
            self.y_pos += self.y_speed #This ensures that we are always adjusting our position
            if(self.y_pos < 0): #How did we get here?
                self.y_pos = 0
                self.y_speed = 0
            if(self.y_pos > 1200): #Don't go under the floor!
                self.y_speed = 0
                self.y_pos = 1200
        self.x_center = self.x_pos + 83 #Rough estimate :)
        self.y_center = self.y_pos + 110 #Rough estimate :)


if __name__ == "__main__":
    new_blob = blob("quirkless", 0, 0)
    def jumpHeight(jumpForce, gravity): #Pilfered from some custom SSF2 code lol
        atApex = False
        yv = jumpForce
        y = 0
        while not atApex:
            if((yv - gravity) <= 0):
                atApex = True
            else:
                yv -= gravity
                y += yv
        return (round(y * 1000) / 1000) 

    def jumpAirtime(jumpForce, gravity):
        frame = 0
        yv = round(jumpForce*1000)
        y = 0
        gravity = round(gravity * 1000)
        hasLanded = False
        while not hasLanded:
            if((frame > 0) and (y <= 0)):
                hasLanded = True
            else:
                yv -= gravity
                y += yv
                frame += 1
        return frame - 1
    
    def projectile_motion(jump_force, gravity):
        print("Jump Force: {}".format(jump_force))
        print("Gravity: {}".format(gravity))
        jump_height = jumpHeight(jump_force, gravity)
        print("Jump Height: {}".format(jump_height))
        print("Final Height: {}".format(1200-jump_height))
        jump_airtime = jumpAirtime(jump_force, gravity)
        print("Airtime: {}".format(jump_airtime))
        print("LIMIT BREAK!")
    
    #5 Star Gravity (1.0) + *23.73915 Jump Force (23.73915) results in JH of 270 (46 Frames)
    #4 Star Gravity (0.9) + *25 Jump Force (22.5) results in JH of 270 (48 Frames)
    #3 Star Gravity (0.8) + *26.48075 Jump Force (21.1846) results in JH of 270 (51 Frames)
    #2 Star Gravity (0.7) + *28.2755 Jump Force (19.79285) results in JH of 270 (55 Frames)
    #1 Star Gravity (0.6) + *30.5 Jump Force (18.3) results in JH of 270 (59 Frames)
    projectile_motion(24.5, 1.05)
    projectile_motion(22.5, 0.9)
    projectile_motion(20.5, 0.75)
    projectile_motion(18.5, 0.6)
    projectile_motion(16.5, 0.45)
    #Formula: 14.5 + gravity_stars * 2