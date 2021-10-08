import math
import os
import random

cwd = os.getcwd()

# INSTRUCTIONS FOR ADDING A BLOB TO THE GAME
# Add the Blob's Stats to the species_to_stars function (see other blobs for a guide)
# Classify that Blob's ability in ability_to_classification function (so it will show the cooldown)
# Add that Blob's image in species_to_image (make sure that the image is in the resources/images/blobs folder)
# Add that Blob's ability icon (make sure that the image is in the resources/images/ability_icons folder)
# In the Blob class, navigate to the ability method to make sure that the ability can be activated.
# Depending on the ability, check the cooldown method 
# If the ability has the potential to impact another blob, update the check_ability_collision method
# If the ability has the potential to impact the ball, update the Ball class' check_blob_ability method
# In resources/graphics_engine/display_css.py, update the Blob Array to show your blob.
# In engine/main_menu.py (should be moved to css.py lol) update blob_list to allow your blob to be selectable
# In resources/graphics_engine/display_almanac.py, update the Blob Array there to show your blob on the matchup chart.
def species_to_stars(species):
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
    if(species == "quirkless"):
        blob_dict = {
            'max_hp': 3,
            'top_speed': 4,
            'traction': 4,
            'friction': 4,
            'gravity': 4,
            'kick_cooldown_rate': 5,
            'block_cooldown_rate': 5,

            'boost_cost': 840,
            'boost_cooldown_max': 5,
            'boost_duration': 5,

            'special_ability': 'boost',
            'special_ability_cost': 840,
            'special_ability_maintenance': 0,
            'special_ability_max': 1800,
            'special_ability_cooldown': 510,
            'special_ability_delay': 0,
            'special_ability_duration': 0,
        }
    elif(species == "fire"):
        blob_dict = {
            'max_hp': 2,
            'top_speed': 4,
            'traction': 4,
            'friction': 3,
            'gravity': 1,
            'kick_cooldown_rate': 3,
            'block_cooldown_rate': 4,

            'boost_cost': 600,
            'boost_cooldown_max': 3,
            'boost_duration': 3,

            'special_ability': 'fireball',
            'special_ability_cost': 150,
            'special_ability_maintenance': 12,
            'special_ability_max': 1800,
            'special_ability_cooldown': 2,
            'special_ability_delay': 0,
            'special_ability_duration': 0,
        }
    elif(species == "ice"):
        blob_dict = {
            'max_hp': 3,
            'top_speed': 4,
            'traction': 1,
            'friction': 3,
            'gravity': 4,
            'kick_cooldown_rate': 3,
            'block_cooldown_rate': 5,

            'boost_cost': 600,
            'boost_cooldown_max': 3,
            'boost_duration': 3,

            'special_ability': 'snowball',
            'special_ability_cost': 150,
            'special_ability_maintenance': 15,
            'special_ability_max': 1800,
            'special_ability_cooldown': 2,
            'special_ability_delay': 0,
            'special_ability_duration': 0,
        }
    elif(species == "water"):
        blob_dict = {
            'max_hp': 2,
            'top_speed': 4,
            'traction': 4,
            'friction': 2,
            'gravity': 3,
            'kick_cooldown_rate': 3,
            'block_cooldown_rate': 3,

            'boost_cost': 600,
            'boost_cooldown_max': 3,
            'boost_duration': 3,

            'special_ability': 'geyser',
            'special_ability_cost': 100,
            'special_ability_maintenance': 15,
            'special_ability_max': 1800,
            'special_ability_cooldown': 2,
            'special_ability_delay': 0,
            'special_ability_duration': 0,
        }
    elif(species == "rock"):
        blob_dict = {
            'max_hp': 5,
            'top_speed': 1,
            'traction': 5,
            'friction': 1,
            'gravity': 5,
            'kick_cooldown_rate': 1,
            'block_cooldown_rate': 2,

            'boost_cost': 600,
            'boost_cooldown_max': 3,
            'boost_duration': 4,

            'special_ability': 'spire',
            'special_ability_cost': 400,
            'special_ability_maintenance': 0,
            'special_ability_max': 1800,
            'special_ability_cooldown': 300,
            'special_ability_delay': 45,
            'special_ability_duration': 0,
        }
    elif(species == "lightning"):
        blob_dict = {
            'max_hp': 1,
            'top_speed': 5,
            'traction': 3,
            'friction': 5,
            'gravity': 5,
            'kick_cooldown_rate': 2,
            'block_cooldown_rate': 1,

            'boost_cost': 600,
            'boost_cooldown_max': 3,
            'boost_duration': 3,

            'special_ability': 'thunderbolt',
            'special_ability_cost': 600,
            'special_ability_maintenance': 0,
            'special_ability_max': 1800,
            'special_ability_cooldown': 240,
            'special_ability_delay': 30,
            'special_ability_duration': 0,
        }
    elif(species == "wind"):
        blob_dict = {
            'max_hp': 1,
            'top_speed': 5,
            'traction': 2,
            'friction': 5,
            'gravity': 1,
            'kick_cooldown_rate': 5,
            'block_cooldown_rate': 1,

            'boost_cost': 600,
            'boost_cooldown_max': 3,
            'boost_duration': 3,

            'special_ability': 'gale',
            'special_ability_cost': 900,
            'special_ability_maintenance': 0,
            'special_ability_max': 1800,
            'special_ability_cooldown': 720,
            'special_ability_delay': 0,
            'special_ability_duration': 240,
        }
    elif(species == "judge"):
        blob_dict = {
            'max_hp': 3,
            'top_speed': 3,
            'traction': 2,
            'friction': 3,
            'gravity': 3,
            'kick_cooldown_rate': 3,
            'block_cooldown_rate': 3,

            'boost_cost': 600,
            'boost_cooldown_max': 3,
            'boost_duration': 3,

            'special_ability': 'c&d',
            'special_ability_cost': 510,
            'special_ability_maintenance': 0,
            'special_ability_max': 1800,
            'special_ability_cooldown': 240,
            'special_ability_delay': 0,
            'special_ability_duration': 60,
        }
    elif(species == "doctor"):
        blob_dict = {
            'max_hp': 4,
            'top_speed': 2,
            'traction': 3,
            'friction': 3,
            'gravity': 4,
            'kick_cooldown_rate': 1,
            'block_cooldown_rate': 1,

            'boost_cost': 600,
            'boost_cooldown_max': 1,
            'boost_duration': 1,

            'special_ability': 'pill',
            'special_ability_cost': 300,
            'special_ability_maintenance': 0,
            'special_ability_max': 1800,
            'special_ability_cooldown': 240,
            'special_ability_delay': 0,
            'special_ability_duration': 0,
        }


    return blob_dict

def ability_to_classification(ability):
    held_abilities = ['fireball', 'snowball', 'geyser']
    if(ability in held_abilities):
        return "held"
    instant_abilities = ['boost', 'gale', 'c&d', 'pill']
    if(ability in instant_abilities):
        return "instant"
    delayed_abilities = ['spire', 'thunderbolt']
    if(ability in delayed_abilities):
        return "delayed"
    return "other"

def species_to_image(species):
    global cwd
    image_dict = {
        "quirkless": cwd+"/resources/images/blobs/quirkless_blob.png",
        "fire": cwd+"/resources/images/blobs/fire_blob.png",
        "ice": cwd+"/resources/images/blobs/ice_blob.png",
        'water': cwd+"/resources/images/blobs/water_blob.png",
        'rock': cwd+"/resources/images/blobs/rock_blob.png",
        'lightning': cwd+"/resources/images/blobs/lightning_blob.png",
        'wind': cwd+"/resources/images/blobs/wind_blob.png",
        'judge': cwd+"/resources/images/blobs/judge_blob.png",
        'doctor': cwd+"/resources/images/blobs/doctor_blob.png",
        "random": cwd+"/resources/images/blobs/random_blob.png",
        "invisible": cwd+"/resources/images/blobs/invisible_blob.png"
    }

    return image_dict[species]

def species_to_ability_icon(species):
    global cwd
    image_dict = {
        "quirkless": cwd+"/resources/images/ui_icons/boost_icon.png",
        "fire": cwd+"/resources/images/ability_icons/fireball.png",
        "ice": cwd+"/resources/images/ability_icons/snowball.png",
        'water': cwd+"/resources/images/ability_icons/geyser.png",
        'rock': cwd+"/resources/images/ability_icons/spire.png",
        'lightning': cwd+"/resources/images/ability_icons/thunderbolt.png",
        'wind': cwd+"/resources/images/ability_icons/gale.png",
        'judge': cwd+"/resources/images/ability_icons/cnd.png",
        'doctor': cwd+"/resources/images/ability_icons/pill.png",
        "random": cwd+"/resources/images/blobs/random_blob.png",
    }
    
    return image_dict[species]

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

def create_visualization(number):
    return math.ceil(number/6)/10

class Blob:
    def __init__(self, species = "quirkless", x_pos = 50, y_pos = 1200, facing = 'left', player = 1, 
    special_ability_charge_base = 1, danger_zone_enabled = True, is_cpu = False):
        self.species = species
        self.player = player #Player 1 or 2
        if(player == 1):
            self.danger_zone = 225
        else:
            self.danger_zone = 1475
        self.is_cpu = is_cpu
        self.cpu_memory = []
        self.image = species_to_image(species)
        self.ability_icon = species_to_ability_icon(species)
        self.stars = species_to_stars(species) #Gets many values for each blob
        self.max_hp = 2 * (self.stars['max_hp'] + 3) #Each star adds an additional HP.
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
        self.gravity_mod = round(.3 + (self.stars['gravity'] + 5) * .15, 3) #Fastfalling increases gravity
        self.fastfalling = False
        self.jump_force = 14.5 + (self.stars['gravity'] * 2) #Initial velocity is based off of gravity
        
        self.kick_cooldown_rate = 1 #Each star reduces kick cooldown
        self.kick_cooldown = 0 #Cooldown timer between kicks
        self.kick_timer = 0 #Active frames of kick
        self.kick_cooldown_max = 240 + 30 * (5 - self.stars['kick_cooldown_rate'])
        self.kick_visualization = 0
        self.kick_visualization_max = 15

        self.block_cooldown_rate = 1 #Each star reduces block cooldown
        self.block_cooldown = 0 #Block cooldown timer
        self.block_timer = 0 #How much time is left in the current block
        self.block_timer_max = 15 #How many frames a block lasts.
        self.block_cooldown_max = 300 + 30 * (5 - self.stars['block_cooldown_rate']) #How long the block cooldown lasts

        self.block_outer = 150
        self.block_inner = -25
        self.block_upper = -200
        self.block_lower = 200

        self.boost_cost = self.stars['boost_cost'] #How much SA meter must be spent to boost
        self.boost_cooldown_max = 300 + 30 *  (5 - self.stars['boost_cooldown_max']) #Each star reduces boost cooldown
        self.boost_cooldown_timer = 0 #Timer that measures between boosts
        self.boost_duration = 60 + (30 * self.stars['boost_duration']) #Each star increases boost duration by half a second
        self.boost_timer = 0 #How much time is left in the current boost
        self.boost_top_speed = 10+(1*self.stars['top_speed'] + 3) #This stat is increased by 3 stars
        self.boost_traction = 0.2 + ((self.stars['traction'] + 5) * 0.15) #These stats are increased by 5 stars
        self.boost_friction = 0.2 + ((self.stars['friction'] + 5) * 0.15) 

        self.focus_lock = 0 #Timer that locks movement when a blob is focusing
        self.focus_lock_max = 60
        self.focusing = False
        self.impact_land_frames = 0 #Locks the player from focusing after landing (fastfall leniency)

        self.special_ability = self.stars['special_ability'] #Special Ability of a Blob
        self.ability_classification = ability_to_classification(self.special_ability)
        self.special_ability_max = self.stars['special_ability_max'] #Highest that the SA gauge can go
        self.special_ability_cost = self.stars['special_ability_cost'] #Price to activate SA
        self.special_ability_maintenance = self.stars['special_ability_maintenance'] #Price to maintain SA
        self.special_ability_charge = 1 #Charge rate. Each frame increases the SA meter by 1 point, or more if focusing
        self.special_ability_meter = 0 #Amount of SA charge stored up
        self.special_ability_timer = 0 #Timer that counts down between uses of an SA
        self.special_ability_duration = 0 #Time that a SA is active
        self.special_ability_cooldown = 0 #Cooldown between uses
        self.special_ability_cooldown_max = self.stars['special_ability_cooldown']
        self.special_ability_charge_base = special_ability_charge_base
        self.special_ability_duration = self.stars['special_ability_duration']
        self.special_ability_delay = self.stars['special_ability_delay']
        self.used_ability = None

        self.collision_distance = 104 #Used for calculating ball collisions
        self.collision_timer = 0 #Prevents double hitting in certain circumstances

        self.damage_flash_timer = 0 #Flashes when damage is taken
        self.parried = False #True when parrying
        self.clanked = False #True when clanking

        self.ability_cooldown_visualization = 0
        self.ability_cooldown_percentage = 0
        self.kick_cooldown_visualization = 0
        self.kick_cooldown_percentage = 0
        self.block_cooldown_visualization = 0
        self.block_cooldown_percentage = 0
        self.boost_cooldown_visualization = 0
        self.boost_cooldown_percentage = 0
        self.boost_timer_visualization = 0
        self.boost_timer_percentage = 0
        self.movement_lock = 0 #Caused if the blob has its movement blocked
        self.danger_zone_enabled = danger_zone_enabled
        self.info = {
            'species': self.species,
            'damage_taken': 0,
            'points_from_goals': 0,
            'points_from_kos': 0,
            'kick_count': 0,
            'block_count': 0,
            'boost_count': 0,
            'parries': 0,
            'clanks': 0,
            'x_distance_moved': 0,
            'wavebounces': 0,
            'jumps': 0,
            'jump_cancelled_focuses': 0,
            'time_focused': 0,
            'time_focused_seconds': 0,
            'time_airborne': 0,
            'time_airborne_seconds': 0,
            'time_grounded': 0,
            'time_grounded_seconds': 0,
        }
        self.recharge_indicators = {
            'damage': False,
            'heal': False,
            'heal_flash': False,
            'damage_flash': False,
            'ability': False,
            'kick': False,
            'block': False,
            'boost': False,
        }
        self.status_effects = {
            "judged": 0,
        }
    
    ground = 1200
    ceiling = 200

    def cooldown(self): #Reduces timers
        if(self.focusing):
            self.special_ability_charge = self.special_ability_charge_base * 5
            self.info['time_focused'] += 1
            self.info['time_focused_seconds'] = round(self.info['time_focused']/60, 2)
            if(self.y_pos < Blob.ground):
                self.focusing = False
                self.focus_lock = 0
        else:
            self.special_ability_charge = self.special_ability_charge_base

        if(self.impact_land_frames):
            self.impact_land_frames -= 1

        if(self.focus_lock > 0):
            self.focus_lock -= 1
        if(self.special_ability_meter < self.special_ability_max):
            self.special_ability_meter += self.special_ability_charge
            if(self.special_ability_meter > self.special_ability_max):
                self.special_ability_meter = self.special_ability_max

        for key in self.recharge_indicators:
            if(self.recharge_indicators[key]):
                if(key == "damage_flash" and self.recharge_indicators[key]):
                    self.toggle_recharge_indicator('damage')
                self.toggle_recharge_indicator(key)

        if(self.special_ability_timer > 0):
            self.special_ability_timer -= 1
            if(self.special_ability_timer == self.special_ability_cooldown_max - (self.special_ability_delay - 1) and self.used_ability == "spire_wait"):
                self.used_ability = "spire"
            if(self.special_ability_timer == self.special_ability_cooldown_max - (self.special_ability_delay - 1) and self.used_ability == "thunderbolt_wait"):
                self.used_ability = "thunderbolt"
            elif(self.used_ability == "thunderbolt" and self.special_ability_timer == self.special_ability_cooldown_max - 180):
                self.used_ability = None
            elif(self.used_ability == "gale" and self.special_ability_timer == self.special_ability_cooldown_max - self.special_ability_duration):
                self.used_ability = None
            elif(self.used_ability == "c&d" and self.special_ability_timer == self.special_ability_cooldown_max - 1):
                self.used_ability = None
            
            if(self.special_ability_timer == 0):
                self.used_ability = None
        
        if(self.special_ability_cooldown > 0):
            self.special_ability_cooldown -= 1
            if(self.special_ability_cooldown == 0):
                self.toggle_recharge_indicator('ability')

        for effect in self.status_effects:
            if(self.status_effects[effect]):
                self.status_effects[effect] -= 1

        if(self.kick_cooldown > 0):
            self.kick_cooldown -= self.kick_cooldown_rate
            if(self.kick_cooldown == 0):
                self.toggle_recharge_indicator('kick')
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
            if(self.block_cooldown == 0):
                self.toggle_recharge_indicator('block')
        
        if(self.boost_timer > 0): #Reduces duration of active boost by 1
            self.boost_timer -= 1 
            if(self.boost_timer <= 0): #Once the boost ends, revert to normal
                self.top_speed = 10+(1*self.stars['top_speed'])
                self.traction = 0.2 + (self.stars['traction'] * 0.15) #Each star increases traction
                self.friction = 0.2 + (self.stars['friction'] * 0.15) #Each star increases friction
        elif(self.boost_cooldown_timer > 0): #If the boost is over, cool down
            self.boost_cooldown_timer -= 1
            if(self.boost_cooldown_timer == 0):
                self.toggle_recharge_indicator('boost')

        if(self.collision_timer > 0):
            self.collision_timer -=1 
        
        if(self.damage_flash_timer > 0):
            self.damage_flash_timer -= 1
            if((self.damage_flash_timer // 10) % 2 == 1):
                self.image = species_to_image('invisible')
            else:
                self.image = species_to_image(self.species)
        
        if(self.movement_lock > 0):
            self.movement_lock -= 1

        if(self.parried):
            self.parried -= 1

        if(self.clanked):
            self.clanked -= 1

        self.ability_cooldown_visualization = create_visualization(self.special_ability_cooldown)
        self.ability_cooldown_percentage = self.special_ability_cooldown/self.special_ability_cooldown_max
        self.kick_cooldown_visualization = create_visualization(self.kick_cooldown/self.kick_cooldown_rate)
        self.kick_cooldown_percentage = self.kick_cooldown/self.kick_cooldown_max
        self.block_cooldown_visualization = create_visualization(self.block_cooldown/self.block_cooldown_rate)
        self.block_cooldown_percentage = self.block_cooldown/self.block_cooldown_max
        self.boost_cooldown_visualization = create_visualization(self.boost_cooldown_timer)
        self.boost_cooldown_percentage = self.boost_cooldown_timer/self.boost_cooldown_max
        self.boost_timer_visualization = create_visualization(self.boost_timer)
        self.boost_timer_percentage = self.boost_timer/self.boost_duration
    
    def ability(self):
        if(self.special_ability == 'boost'):
            self.boost()
        elif(self.special_ability == 'fireball'):
            if(self.special_ability_meter >= self.special_ability_cost and self.special_ability_timer <= 2):
                if(self.special_ability_timer > 0):
                    #If we were holding down the button before
                    self.used_ability = "fireball"
                    self.special_ability_timer = self.special_ability_cooldown_max #Set the cooldown between uses timer
                    self.special_ability_meter -= self.special_ability_maintenance #Remove some SA meter
                else:
                    #If we ignite the ball
                    self.used_ability = "fireball"
                    self.special_ability_timer = self.special_ability_cooldown_max #Set the cooldown between uses timer
                    self.special_ability_meter -= self.special_ability_cost #Remove some SA meter
        elif(self.special_ability == 'snowball'):
            if(self.special_ability_meter >= self.special_ability_cost and self.special_ability_timer <= 2):
                if(self.special_ability_timer > 0):
                    #If we were holding down the button before
                    self.used_ability = "snowball"
                    self.special_ability_timer = self.special_ability_cooldown_max #Set the cooldown between uses timer
                    self.special_ability_meter -= self.special_ability_maintenance #Remove some SA meter
                else:
                    #If we ignite the ball
                    self.used_ability = "snowball"
                    self.special_ability_timer = self.special_ability_cooldown_max #Set the cooldown between uses timer
                    self.special_ability_meter -= self.special_ability_cost #Remove some SA meter
        elif(self.special_ability == 'geyser'):
            if(self.special_ability_meter >= self.special_ability_cost and self.special_ability_timer <= 2):
                if(self.special_ability_timer > 0):
                    #If we were holding down the button before
                    self.used_ability = "geyser"
                    self.special_ability_timer = self.special_ability_cooldown_max #Set the cooldown between uses timer
                    self.special_ability_meter -= self.special_ability_maintenance #Remove some SA meter
                else:
                    #If we ignite the ball
                    self.used_ability = "geyser"
                    self.special_ability_timer = self.special_ability_cooldown_max #Set the cooldown between uses timer
                    self.special_ability_meter -= self.special_ability_cost #Remove some SA meter
        elif(self.special_ability == "spire"):
            if(self.special_ability_meter >= self.special_ability_cost and self.special_ability_cooldown <= 0):
                #Spire activation
                self.used_ability = "spire_wait"
                self.special_ability_cooldown = self.special_ability_cooldown_max
                self.special_ability_timer = self.special_ability_cooldown_max #Set the cooldown between uses timer
                self.special_ability_meter -= self.special_ability_cost #Remove some SA meter
        elif(self.special_ability == "thunderbolt"):
            if(self.special_ability_meter >= self.special_ability_cost and self.special_ability_cooldown <= 0):
                #Thunderbolt activation
                self.used_ability = 'thunderbolt_wait' #This is done for a technical reason, to prevent premature electrocution
                self.special_ability_cooldown = self.special_ability_cooldown_max
                self.special_ability_timer = self.special_ability_cooldown #Set the cooldown between uses timer
                self.special_ability_meter -= self.special_ability_cost #Remove some SA meter
        elif(self.special_ability == "gale"):
            if(self.special_ability_meter >= self.special_ability_cost and self.special_ability_cooldown <= 0):
                #Gale activation
                self.used_ability = "gale"
                self.special_ability_cooldown = self.special_ability_cooldown_max
                self.special_ability_timer = self.special_ability_cooldown
                self.special_ability_meter -= self.special_ability_cost
        elif(self.special_ability == "c&d"):
            if(self.special_ability_meter >= self.special_ability_cost and self.special_ability_cooldown <= 0):
                self.used_ability = "c&d"
                self.special_ability_cooldown = self.special_ability_cooldown_max
                self.special_ability_timer = self.special_ability_cooldown
                self.special_ability_meter -= self.special_ability_cost
        elif(self.special_ability == "pill"):
            if(self.special_ability_meter >= self.special_ability_cost and self.special_ability_cooldown <= 0):
                self.special_ability_cooldown = self.special_ability_cooldown_max
                self.special_ability_timer = self.special_ability_cooldown
                self.special_ability_meter -= self.special_ability_cost
                random_number = random.randint(0, 15)
                if(0 <= random_number <= 7):
                    self.used_ability = "pill_heal"
                    if(self.hp == self.max_hp):
                        if(0 <= random_number <= 3):
                            self.used_ability = "pill_cooldown"
                            self.special_ability_cooldown -= 60
                            self.kick_cooldown -= 60
                            self.block_cooldown -= 60
                            self.boost_cooldown_timer -= 60
                        else:
                            self.used_ability = "pill_boost"
                            self.boost_timer += 120
                    else:
                        self.hp += 1
                elif(8 <= random_number <= 11):
                    self.used_ability = "pill_cooldown"
                    self.special_ability_cooldown -= 60
                    self.kick_cooldown -= 60
                    self.block_cooldown -= 60
                    self.boost_cooldown_timer -= 60
                else:
                    self.used_ability = "pill_boost"
                    self.boost(boost_duration=120, boost_cooldown=0)
 
    def kick(self):
        if(self.kick_cooldown <= 0):
            self.block_cooldown += 5 * (self.block_cooldown_rate)
            self.kick_timer = 2
            self.kick_cooldown = self.kick_cooldown_max
            self.collision_distance = 175
            self.kick_visualization = self.kick_visualization_max
            self.info['kick_count'] += 1

    def block(self):
        if(self.block_cooldown <= 0):
            self.kick_cooldown += 5 * (self.kick_cooldown_rate)
            self.block_cooldown = self.block_cooldown_max #Set block cooldown
            self.block_timer = self.block_timer_max #Set active block timer
            self.movement_lock = 30
            self.x_speed = 0
            if(self.y_speed < 0): #If we are moving upwards, halt your momentum!
                self.y_speed = 0
            self.info['block_count'] += 1

    def boost(self, boost_duration = None, boost_cooldown = None):
        if(self.special_ability_meter >= self.boost_cost and self.boost_cooldown_timer <= 0):
            self.special_ability_meter -= self.boost_cost #Remove some SA meter
            self.top_speed = self.boost_top_speed
            self.traction = self.boost_traction
            self.friction = self.boost_friction
            if(boost_duration is None):
                self.boost_timer += self.boost_duration #Set the boost's timer to its maximum duration, about 5 seconds
            else:
                self.boost_timer += boost_duration
            if(boost_cooldown is None):
                self.boost_cooldown_timer += self.boost_cooldown_max
            else:
                self.boost_cooldown_timer += boost_cooldown
            self.info['boost_count'] += 1
            if(self.species == "quirkless"):
                self.special_ability_cooldown = self.special_ability_cooldown_max
    
    def check_blob_collision(self, blob):
        #Used to see if a blob is getting kicked!
        if(self.x_center - (1.5 * self.collision_distance) <= blob.x_center <= self.x_center + (1.5 * self.collision_distance)):
            if(self.y_center - (1.1 * self.collision_distance) <= blob.y_center <= self.y_center + (self.collision_distance)):
                accumulated_damage = 2
                if(self.boost_timer > 0):  # Take additional damage if the enemy is boosting
                    accumulated_damage += 1
                if(((blob.player == 2 and blob.x_pos >= blob.danger_zone) or (blob.player == 1 and blob.x_pos <= blob.danger_zone)) and blob.danger_zone_enabled):
                    #Take additional damage from kicks if you are hiding by your goal
                    accumulated_damage += 1
                blob.take_damage(accumulated_damage)
                    
    def check_ability_collision(self, blob, ball):
        if(self.used_ability == "spire" and self.special_ability_timer == self.special_ability_cooldown_max - self.special_ability_delay
        and ball.x_center - 150 <= blob.x_center <= ball.x_center + 150):
            if(blob.block_timer == 0):
                blob.take_damage(y_speed_mod = -30 - (5 * (blob.gravity_stars - 1.05)), movement_lock = 20)
            else:
                blob.block_cooldown += 30
        elif(self.used_ability == "thunderbolt" and self.special_ability_timer == self.special_ability_cooldown_max - self.special_ability_delay
        and ball.x_center - 150 <= blob.x_center <= ball.x_center + 150
        and blob.block_timer == 0):
            blob.take_damage()
        elif((self.used_ability == "gale") or \
            (blob.used_ability == "gale")):
            if blob.y_pos != blob.ground and not blob.block_timer: #Gale Affecting the opponent
                if(self.player == 1 and self.used_ability == "gale" and blob.x_speed < 5): #Airborne
                    blob.x_speed += 1
                elif(self.player == 2 and self.used_ability == "gale" and blob.x_speed > -5):
                    blob.x_speed -= 1

        elif(self.used_ability == "c&d"):
            blob.status_effects['judged'] = self.special_ability_duration

    def take_damage(self, damage = 1, unblockable = False, unclankable = False, damage_flash_timer = 60, y_speed_mod = 0, movement_lock = 0):
        damage_taken = False
        def check_block():  # Returns true if the hit goes through
            if(self.block_timer):  # Blocking?
                self.parried = 2
                self.info['parries'] += 1
                return False
            else:
                return True

        def check_clank(): # Returns true if the hit goes through
            if(self.kick_timer == 1):  # Kicking?
                self.clanked = 2
                self.info['clanks'] += 1
                return False
            else:
                return True
                
        if(unblockable and unclankable):
            self.hp -= damage
            damage_taken = True
        elif(unclankable):
            if check_block():
                damage_taken = True
        elif(unblockable):
            if check_clank():
                damage_taken = True
        else:
            if(check_block() and check_clank()):
                damage_taken = True
        
        if(damage_taken):
            self.hp -= damage
            self.damage_flash_timer = damage_flash_timer
            self.info['damage_taken'] += damage
            self.movement_lock = movement_lock
            self.y_speed = y_speed_mod
            if(not self.recharge_indicators['damage_flash']):  # If we're hit twice on the same frame, don't disable the flash!
                self.toggle_recharge_indicator('damage_flash')

    def blob_ko(self):
        self.y_speed = 10
        if(self.y_pos < 2000):
            self.y_pos += self.y_speed

    def reset(self, player):
        self.x_speed = 0
        self.y_speed = 0
        if(player == 1):
            self.x_pos = 100
            self.facing = 'right'
        else:
            self.x_pos = 1600
            self.facing = 'left'
        self.y_pos = Blob.ground
        if(self.species == "quirkless" and self.boost_timer):
            self.special_ability_cooldown -= self.boost_timer
        self.boost_timer = 0
        self.focus_lock = 0
        self.kick_visualization = 0
        self.block_timer = 0
        self.focusing = False
        self.damage_flash_timer = 0
        self.image = species_to_image(self.species)
        self.special_ability_timer = 0
        self.used_ability = None
        self.top_speed = self.base_top_speed
        self.friction = self.base_friction
        self.traction = self.base_traction
        self.impact_land_frames = 0
        self.movement_lock = 0
        self.status_effects['judged'] = 0
        
    def move(self, pressed_buttons):
        pressed_conversions = player_to_controls(self.player)

        pressed = []
        for button in pressed_buttons:
            if(button in pressed_conversions):
                if(self.focusing):
                    if(pressed_conversions[button] == "down"):
                        pressed.append(pressed_conversions[button])
                    elif(pressed_conversions[button] == "up"):
                        pressed.append(pressed_conversions[button])
                        self.info['jump_cancelled_focuses'] += 1
                    else:
                        continue
                else:
                    pressed.append(pressed_conversions[button])
        
        if(self.movement_lock > 0):
            pressed = []
        if(self.status_effects['judged']):
            if('kick' in pressed):
                pressed.remove('kick')
            if('block' in pressed):
                pressed.remove('block')
            if('boost' in pressed):
                pressed.remove('boost')
            if('ability' in pressed):
                pressed.remove('ability')

            #HORIZONTAL MOVEMENT
        if(self.y_pos == Blob.ground): #Applies traction if grounded
            if('left' in pressed and not 'right' in pressed): #If holding left but not right
                self.facing = "left"
                if(self.x_pos <= 0): #Are we in danger of going off screen?
                    self.x_speed = 0
                    self.x_pos = 0
                else:
                    if(abs(self.x_speed) < self.top_speed):
                        self.x_speed -= self.traction #Accelerate based off of traction
                    else:
                        prev_speed = self.x_speed
                        self.x_speed = -1*self.top_speed #If at max speed, maintain it
                        if(not round(prev_speed) == -1*self.top_speed):
                            self.info['wavebounces'] += 1
                        
            elif(not 'left' in pressed and 'right' in pressed): #If holding right but not left
                self.facing = 'right'
                if(self.x_pos >= 1700): #Are we in danger of going off screen?
                    self.x_speed = 0
                    self.x_pos = 1700
                else:
                    if(abs(self.x_speed) < self.top_speed):
                        self.x_speed += self.traction #Accelerate based off of traction
                    else:
                        prev_speed = self.x_speed
                        self.x_speed = self.top_speed #If at max speed, maintain it
                        if(not round(prev_speed) == self.top_speed):
                            self.info['wavebounces'] += 1
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
        self.info['x_distance_moved'] += abs(self.x_speed)
        if(self.x_pos <= 0): #Don't move off screen!
            self.x_speed = 0
            self.x_pos = 0
        elif(self.x_pos >= 1700): #Don't move off screen!
            self.x_speed = 0
            self.x_pos = 1700
        
        #VERTICAL MOVEMENT
        if('up' in pressed and self.y_pos == Blob.ground): #If you press jump while grounded, jump!
            self.y_speed = -1 * self.jump_force
            self.focus_lock = 0
            self.focusing = False
            self.info['jumps'] += 1
        elif('down' in pressed):
            if(self.y_pos < Blob.ground): #If you are above ground and press down
                self.fastfalling = True #Fast fall, increasing your gravity by 3 stars
            else:
                if(not self.focusing and not self.impact_land_frames):
                    self.focusing = True
                    self.focus_lock = self.focus_lock_max
                elif(self.focusing):
                    self.focusing = True
        if(not 'down' in pressed and self.focus_lock == 0 and self.focusing):
            #True if we're not holding down, focus lock is done and we're focusing
            self.focusing = False
        if(self.y_pos < Blob.ground): #Applies gravity while airborne, respecting fast fall status.
            self.info['time_airborne'] += 1
            self.info['time_airborne_seconds'] = round(self.info['time_airborne']/60, 2)
            if(self.fastfalling):
                self.y_speed += self.gravity_mod
            else:
                self.y_speed += self.gravity_stars
        else:
            self.info['time_grounded'] += 1
            self.info['time_grounded_seconds'] = round(self.info['time_grounded']/60, 2)
        
        if(self.fastfalling and self.y_pos == Blob.ground): #If you land, cancel the fastfall.
            self.fastfalling = False
        self.y_pos += self.y_speed #This ensures that we are always adjusting our position
        if(self.y_pos < Blob.ceiling): #How did we get here?
            self.y_pos = Blob.ceiling
            self.y_speed = 0
        if(self.y_pos > Blob.ground): #Don't go under the floor!
            self.y_speed = 0
            self.y_pos = Blob.ground
            self.impact_land_frames = 10
        
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
    
    #The following functions are for visualizations and timers

    def get_ability_visuals(self):
        return self.ability_cooldown_percentage, self.ability_cooldown_visualization
    
    def get_kick_visuals(self):
        return self.kick_cooldown_percentage, self.kick_cooldown_visualization
    
    def get_block_visuals(self):
        return self.block_cooldown_percentage, self.block_cooldown_visualization

    def get_boost_timer_visuals(self):
        return self.boost_timer_percentage, self.boost_timer_visualization

    def get_boost_cooldown_visuals(self):
        return self.boost_cooldown_percentage, self.boost_cooldown_visualization

    def toggle_recharge_indicator(self, indicator):
        self.recharge_indicators[indicator] = not self.recharge_indicators[indicator]
    