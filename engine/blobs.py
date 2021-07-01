import math
import os
print("BLOB",os.getcwd())
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
            'kick_cooldown_rate': 5,
            'block_cooldown_rate': 5,

            'boost_cost': 600,
            'boost_cooldown_rate': 5,
            'boost_duration': 5,

            'special_ability': 'boost',
            'special_ability_cost': 300,
            'special_ability_max': 1800,
            'special_ability_cooldown': 300
        }
    return blob_dict

def type_to_image(type):
    global cwd
    image_dict = {
        "quirkless": cwd+"\\resources\\images\\blobs\\quirkless_blob.png",
        "random": cwd+"\\resources\\images\\blobs\\random_blob.png",
        "invisible": cwd+"\\resources\\images\\blobs\\invisible_blob.png"
    }

    return image_dict[type]

def player_to_controls(player):
    if(player == 1):
        button_list = {
            'p1_up': 'up',
            'p1_down': 'down',
            'p1_left': 'left',
            'p1_right': 'right',
            'p1_ability': 'ability',
            'p1_kick': 'kick',
            'p1_block': 'block',
            'p1_boost': 'boost'
        }
    else:
        button_list = {
            'p2_up': 'up',
            'p2_down': 'down',
            'p2_left': 'left',
            'p2_right': 'right',
            'p2_ability': 'ability',
            'p2_kick': 'kick',
            'p2_block': 'block',
            'p2_boost': 'boost'
        }
    return button_list

class blob:
    def __init__(self, type = "quirkless", x_pos = 50, y_pos = 1200, facing = 'left', player = 1):
        self.type = type
        self.player = player #Player 1 or 2
        self.image = type_to_image(type)
        self.stars = type_to_stars(type) #Gets many values for each blob
        self.max_hp = self.stars['max_hp'] + 2 #Each star adds an additional HP.
        self.hp = self.max_hp
        self.top_speed = 10+(1*self.stars['top_speed']) #Each star adds some speed
        self.base_top_speed = self.top_speed #Non-boosted
        self.x_speed = 0
        self.y_speed = 0
        self.x_pos = x_pos #Where the blob is on the X axis
        self.y_pos = y_pos #Where the blob is on the Y axis, 1200 is grounded
        self.x_center = x_pos + 80
        self.y_center = y_pos + 110
        self.facing = facing #Where the blob is currently facing
        self.traction = 0.2 + (self.stars['traction'] * 0.15) #Each star increases traction
        self.friction = 0.2 + (self.stars['friction'] * 0.15) #Each star increases friction
        self.base_traction = self.traction #Non-boosted
        self.base_friction = self.friction #No boost
        self.gravity_stars = round(.3 + (self.stars['gravity'] * .15), 3) #Each star increases gravity
        self.gravity_mod = round(.3 + (self.stars['gravity'] + 3) * .15, 3) #Fastfalling increases gravity
        self.fastfalling = False
        self.jump_force = 14.5 + (self.stars['gravity'] * 2) #Initial velocity is based off of gravity
        
        self.kick_cooldown_rate = 5 + self.stars['kick_cooldown_rate'] #Each star reduces kick cooldown
        self.kick_cooldown = 0 #Cooldown timer between kicks
        self.kick_timer = 0 #Active frames of kick
        self.kick_cooldown_max = 2400
        self.kick_visualization = 0
        self.kick_visualization_max = 15

        self.block_cooldown_rate = 5 + self.stars['block_cooldown_rate'] #Each star reduces block cooldown
        self.block_cooldown = 0 #Block cooldown timer
        self.block_timer = 0 #How much time is left in the current block
        self.block_timer_max = 15 #How many frames a block lasts.
        self.block_cooldown_max = 3000 #How long the block cooldown lasts

        self.block_outer = 150
        self.block_inner = -25
        self.block_upper = -200
        self.block_lower = 200

        self.boost_cost = self.stars['boost_cost'] #How much SA meter must be spent to boost
        self.boost_cooldown_rate = 1 + self.stars['boost_cooldown_rate'] #Each star reduces boost cooldown
        self.boost_cooldown_timer = 0 #Timer that measures between boosts
        self.boost_duration = 60 + (30 * self.stars['boost_duration']) #Each star increases boost duration by half a second
        self.boost_timer = 0 #How much time is left in the current boost
        self.boost_top_speed = 10+(1*self.stars['top_speed'] + 1) #These stats are increased by 1 star
        self.boost_traction = 0.2 + ((self.stars['traction'] + 1) * 0.15)
        self.boost_friction = 0.2 + ((self.stars['friction'] + 1) * 0.15) 

        self.focus_lock = 0 #Timer that locks movement when a blob is focusing
        self.focus_lock_max = 60
        self.focusing = False

        self.special_ability = self.stars['special_ability'] #Special Ability of a Blob
        self.special_ability_max = self.stars['special_ability_max'] #Highest that the SA gauge can go
        self.special_ability_cost = self.stars['special_ability_cost'] #Price to use SA
        self.special_ability_charge = 1 #Charge rate. Each frame increases the SA meter by 1 point, or more if focusing
        self.special_ability_meter = 0 #Amount of SA charge stored up

        self.collision_distance = 104 #Used for calculating ball collisions
        self.collision_timer = 0 #Prevents double hitting in certain circumstances

        self.damage_flash_timer = 0 #Flashes when damage is taken
        self.movement_lock = 0 #Caused if the blob has its movement blocked
    
    ground = 1200

    def cooldown(self): #Reduces timers
        if(self.focusing):
            self.special_ability_charge = 5
        else:
            self.special_ability_charge = 1

        if(self.focus_lock > 0):
            self.focus_lock -= 1
        if(self.special_ability_meter < self.special_ability_max):
            self.special_ability_meter += self.special_ability_charge
            if(self.special_ability_meter > self.special_ability_max):
                self.special_ability_meter = self.special_ability_max

        if(self.kick_cooldown > 0):
            self.kick_cooldown -= self.kick_cooldown_rate
        if(self.kick_timer > 0):
            self.kick_timer -= 1
            if(self.kick_timer == 0):
                self.collision_distance = 104

        if(self.kick_visualization > 0):
            self.kick_visualization -= 1

        if(self.block_timer > 0):
            self.block_timer -= 1
        if(self.block_cooldown > 0):
            self.block_cooldown -= self.block_cooldown_rate
        
        if(self.boost_timer > 0): #Reduces duration of active boost by 1
            self.boost_timer -= 1 
            if(self.boost_timer <= 0): #Once the boost ends, revert to normal
                self.top_speed = 10+(1*self.stars['top_speed'])
                self.traction = 0.2 + (self.stars['traction'] * 0.15) #Each star increases traction
                self.friction = 0.2 + (self.stars['friction'] * 0.15) #Each star increases friction
        elif(self.boost_cooldown_timer > 0): #If the boost is over, cool down
            self.boost_cooldown_timer -= self.boost_cooldown_rate

        if(self.collision_timer > 0):
            self.collision_timer -=1 
        
        if(self.damage_flash_timer > 0):
            self.damage_flash_timer -= 1
            if((self.damage_flash_timer // 10) % 2 == 1):
                self.image = type_to_image('invisible')
            else:
                self.image = type_to_image(self.type)
        
        if(self.movement_lock > 0):
            self.movement_lock -= 1
    def ability(self):
        if(self.special_ability == 'boost'):
            self.boost()

    def kick(self):
        if(self.kick_cooldown <= 0):
            self.block_cooldown += 5 * (self.block_cooldown_rate)
            self.kick_timer = 2
            self.kick_cooldown = self.kick_cooldown_max
            self.collision_distance = 175
            self.kick_visualization = self.kick_visualization_max

    def block(self):
        if(self.block_cooldown <= 0):
            self.kick_cooldown += 5 * (self.kick_cooldown_rate)
            self.block_cooldown = self.block_cooldown_max #Set block cooldown
            self.block_timer = self.block_timer_max #Set active block timer
            self.movement_lock = 30
            self.x_speed = 0

    def boost(self):
        if(self.special_ability_meter >= self.boost_cost and self.boost_cooldown_timer <= 0):
            self.boost_cooldown_timer = 600 #About 5 seconds
            self.special_ability_meter -= self.boost_cost #Remove some SA meter
            self.top_speed = self.boost_top_speed
            self.traction = self.boost_traction
            self.friction = self.boost_friction
            self.boost_timer = self.boost_duration #Set the boost's timer to its maximum duration
            print(self.boost_timer)

    def check_blob_collision(self, blob):
        #Used to see if a blob is getting kicked!
        if(self.x_center - (1.5 * self.collision_distance) <= blob.x_center <= self.x_center + (1.5 * self.collision_distance)):
            if(self.y_center - (1.1 * self.collision_distance) <= blob.y_center <= self.y_center + (self.collision_distance)):
                if(blob.block_timer == 0):
                    if(self.boost_timer > 0):
                        blob.hp -= 2
                    else:
                        blob.hp -= 1
                    blob.damage_flash_timer = 60

    def blob_ko(self):
        self.y_speed = 10
        print(self.y_pos)
        if(self.y_pos < 2000):
            self.y_pos += self.y_speed

    def reset(self, player):
        self.x_speed = 0
        self.y_speed = 0
        if(player == 1):
            self.x_pos = 1600
            self.facing = 'left'
        else:
            self.x_pos = 100
            self.facing = 'right'
        self.y_pos = blob.ground
        self.boost_timer = 0
        self.focus_lock = 0
        self.kick_visualization = 0
        self.block_timer = 0
        
    def move(self, pressed_buttons):
        pressed_conversions = player_to_controls(self.player)

        pressed = []
        for button in pressed_buttons:
            if(button in pressed_conversions):
                pressed.append(pressed_conversions[button])

        if(self.focusing):
            for button in pressed:
                if(button == "down"):
                    continue
                else:
                    pressed.remove(button)
        
        if(self.movement_lock > 0):
            pressed = []

            #HORIZONTAL MOVEMENT
        if(self.y_pos == blob.ground): #Applies traction if grounded
            if('left' in pressed and not 'right' in pressed): #If holding left but not right
                self.facing = "left"
                if(self.x_pos <= 0): #Are we in danger of going off screen?
                    self.x_speed = 0
                    self.x_pos = 0
                else:
                    if(abs(self.x_speed) < self.top_speed):
                        self.x_speed -= self.traction #Accelerate based off of traction
                    else:
                        self.x_speed = -1*self.top_speed #If at max speed, maintain it
            elif(not 'left' in pressed and 'right' in pressed): #If holding right but not left
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
            if('left' in pressed and not 'right' in pressed): #If holding left but not right
                self.facing = "left"
                if(self.x_pos <= 0): #Are we in danger of going off screen?
                    self.x_speed = 0
                    self.x_pos = 0
                else:
                    if(abs(self.x_speed) < self.top_speed):
                        self.x_speed -= self.friction #Accelerate based off of traction
                    else:
                        self.x_speed = -1*self.top_speed #If at max speed, maintain it
            elif(not 'left' in pressed and 'right' in pressed): #If holding right but not left
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
        if('up' in pressed and self.y_pos == blob.ground): #If you press jump while grounded, jump!
            self.y_speed = -1 * self.jump_force
        if('down' in pressed):
            if(self.y_pos < blob.ground): #If you are above ground and press down
                self.fastfalling = True #Fast fall, increasing your gravity by 3 stars
            else:
                if(not self.focusing):
                    self.focusing = True
                    self.focus_lock = self.focus_lock_max
        if(not 'down' in pressed and self.focus_lock == 0 and self.focusing):
            #True if we're not holding down, focus lock is done and we're focusing
            self.focusing = False
        if(self.y_pos < blob.ground): #Applies gravity while airborne, respecting fast fall status.
            if(self.fastfalling):
                self.y_speed += self.gravity_mod
            else:
                self.y_speed += self.gravity_stars
        if(self.fastfalling and self.y_pos == blob.ground): #If you land, cancel the fastfall.
            self.fastfalling = False
        self.y_pos += self.y_speed #This ensures that we are always adjusting our position
        if(self.y_pos < 0): #How did we get here?
            self.y_pos = 0
            self.y_speed = 0
        if(self.y_pos > blob.ground): #Don't go under the floor!
            self.y_speed = 0
            self.y_pos = blob.ground
        
        #ABILITY
        if('ability' in pressed):
            self.ability()

        # BOOST
        if('boost' in pressed):
            self.boost()
        
        #Kick
        if('kick' in pressed):
            self.kick()
        elif('block' in pressed):
            self.block()
    
        self.x_center = self.x_pos + 83 #Rough estimate :)
        self.y_center = self.y_pos + 110 #Rough estimate :)


if __name__ == "__main__":
    new_blob = blob("quirkless", 0, 0)
