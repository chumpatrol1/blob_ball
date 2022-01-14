import math
import os
import random
from resources.sound_engine.sfx_event import createSFXEvent
from engine.blob_stats import species_to_stars

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
# In engine/unlocks.py, update css_selector_list and original_css_display_list to allow that blob to be selected
# In engine/unlocks.py, update css_location_dict with the intended location of that blob
# In engine/unlocks.py, update blob_unlock_dict
# In engine/endgame.py, update attempt_unlocks with the number of games it takes to unlock that blob
# In engine/popup_list.py, update blob_unlock_popups to include the new blob's unlock text
# In resources/graphics_engine/display_almanac.py, update the Blob Array there to show your blob on the matchup chart.

def ability_to_classification(ability):
    held_abilities = ['fireball', 'snowball', 'geyser', 'gale',]
    if(ability in held_abilities):
        return "held"
    instant_abilities = ['boost', 'c&d', 'pill', 'tax', 'stoplight']
    if(ability in instant_abilities):
        return "instant"
    delayed_abilities = ['spire', 'thunderbolt', 'starpunch']
    if(ability in delayed_abilities):
        return "delayed"
    return "other"

def species_to_image(species):
    global cwd
    blob_cwd = cwd + '/resources/images/blobs/'
    image_dict = {
        "quirkless": blob_cwd + "quirkless_blob.png",
        "fire": blob_cwd + "fire_blob.png",
        "ice": blob_cwd + "ice_blob.png",
        'water': blob_cwd + "water_blob.png",
        'rock': blob_cwd + "rock_blob.png",
        'lightning': blob_cwd + "lightning_blob.png",
        'wind': blob_cwd + "wind_blob.png",
        'judge': blob_cwd + "judge_blob.png",
        'doctor': blob_cwd + "doctor_blob.png",
        'king': blob_cwd + 'king_blob.png',
        'cop': blob_cwd + 'cop_blob.png',
        'boxer': blob_cwd + 'boxer_blob.png',
        "random": blob_cwd + "random_blob.png",
        "invisible": blob_cwd + "invisible_blob.png"
    }

    return image_dict[species]

def species_to_ability_icon(species):
    global cwd
    icon_cwd = cwd + "/resources/images/ui_icons/"
    ability_cwd = cwd + "/resources/images/ability_icons/"
    image_dict = {
        "quirkless": icon_cwd + "boost_icon.png",
        "fire": ability_cwd + "fireball.png",
        "ice": ability_cwd + "snowball.png",
        'water': ability_cwd + "geyser.png",
        'rock': ability_cwd + "spire.png",
        'lightning': ability_cwd + "thunderbolt.png",
        'wind': ability_cwd + "gale.png",
        'judge': ability_cwd + "cnd.png",
        'doctor': ability_cwd + "pill.png",
        'king': ability_cwd + "tax.png",
        'cop': ability_cwd + "block_icon.png",
        'boxer': ability_cwd + 'starpunch.png',
        "random": icon_cwd + "boost_icon.png",
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
    special_ability_charge_base = 1, danger_zone_enabled = True, is_cpu = False, stat_overrides = None):
        self.species = species
        self.player = player #Player 1 or 2
        if(player == 1):
            self.danger_zone = 225
        else:
            self.danger_zone = 1475
        self.is_cpu = is_cpu
        self.cpu_memory = {'press_queue': [], 'game_state': '', 'current_play': ''}
        self.image = species_to_image(species)
        self.ability_icon = species_to_ability_icon(species)
        self.stars = species_to_stars(species, stat_overrides) #Gets many values for each blob
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
        self.shorthopping = False
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
        self.holding_timer = 0 # Used for held abilities

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
            'ability_swap_b': False,
            'ability_swap': False,
            'kick': False,
            'block': False,
            'boost': False,
            'ability_energy': False,
        }
        self.status_effects = {
            "judged": 0,
            "pill": None,
            "pill_weights": {'pill_boost': 3, 'pill_cooldown': 3, 'pill_heal': 3},
            "taxing": 0,
            "taxed": 0,
            "stunned": 0,
        }

        if(self.species == "doctor" or self.species == "joker"):
            random_number = random.randint(0,1)
            if(random_number):
                self.status_effects['pill'] = 'pill_boost'
                self.update_ability_icon(cwd + "/resources/images/ability_icons/{}.png".format(self.status_effects['pill']))
            else:
                self.status_effects['pill'] = 'pill_cooldown'
                cwd + "/resources/images/ability_icons/{}.png".format(self.status_effects['pill'])
                self.update_ability_icon(cwd + "/resources/images/ability_icons/{}.png".format(self.status_effects['pill']))
    
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

            if(self.special_ability_cost + (self.special_ability_charge * 5) > self.special_ability_meter >= self.special_ability_cost and not self.recharge_indicators['ability_energy']\
                and not (self.ability_classification == "held" and self.special_ability_timer > 0)):
                self.toggle_recharge_indicator('ability_energy', 2)

            if(self.special_ability_meter > self.special_ability_max):
                self.special_ability_meter = self.special_ability_max

        for key in self.recharge_indicators:
            if(self.recharge_indicators[key]):
                if(key == "damage_flash" and self.recharge_indicators[key]):
                    self.toggle_recharge_indicator('damage')
                elif(key == "heal_flash" and self.recharge_indicators[key]):
                    self.toggle_recharge_indicator('heal')
                elif(key == "ability_swap" and self.recharge_indicators[key]):
                    self.toggle_recharge_indicator('ability_swap_b')
                self.toggle_recharge_indicator(key)

        if(self.special_ability_timer > 0):
            self.special_ability_timer -= 1
            if(self.holding_timer % 18 == 17 and self.used_ability == "fireball"):
                createSFXEvent('fire')
            elif(self.holding_timer % 20 == 19 and self.used_ability == "snowball"):
                createSFXEvent('ice')
            elif(self.holding_timer % 12 == 11 and self.used_ability == "geyser"):
                createSFXEvent('water')
            elif(self.holding_timer % 60 == 59 and self.used_ability == "gale"):
                createSFXEvent('gale')
            if(self.special_ability_timer == self.special_ability_cooldown_max - (self.special_ability_delay - 1) and self.used_ability == "spire_wait"):
                self.used_ability = "spire"
            elif(self.special_ability_timer == self.special_ability_cooldown_max - (self.special_ability_delay - 1) and self.used_ability == "thunderbolt_wait"):
                self.used_ability = "thunderbolt"
            elif(self.used_ability == "thunderbolt" and self.special_ability_timer == self.special_ability_cooldown_max - self.special_ability_delay - self.special_ability_duration):
                self.used_ability = None
                '''elif(self.used_ability == "gale"): # Move me back later i guess!
                if (self.special_ability_timer == self.special_ability_cooldown_max - self.special_ability_duration):
                    self.used_ability = None
                elif (self.special_ability_cooldown_max - self.special_ability_timer) % 60 == 0:
                    createSFXEvent('gale')'''
            elif(self.used_ability == "c&d" and self.special_ability_timer == self.special_ability_cooldown_max - 1):
                self.used_ability = None
            elif(self.used_ability == "pill" and self.special_ability_timer == self.special_ability_cooldown_max - 2):
                self.used_ability = None
            elif(self.used_ability == "tax" and self.special_ability_timer == self.special_ability_cooldown_max - 1):
                self.used_ability = None
            elif(self.used_ability == "stoplight" and self.special_ability_timer == self.special_ability_cooldown_max -1):
                self.used_ability = "stoplight_pfx"
            elif(self.used_ability == "stoplight_pfx"):
                self.used_ability = None
            elif(self.used_ability == "starpunch_wait" and self.special_ability_timer == self.special_ability_cooldown_max - (self.special_ability_delay - 1)):
                self.used_ability = "starpunch"
            elif(self.used_ability == "starpunch"):
                self.used_ability = None

            if(self.special_ability_timer == 0):
                self.used_ability = None
        
        if(self.special_ability_cooldown > 0):
            self.special_ability_cooldown -= 1
            if(self.special_ability_cooldown == 0):
                self.toggle_recharge_indicator('ability')
        

        for effect in self.status_effects:
            if(self.status_effects[effect]):
                try:
                    self.status_effects[effect] -= 1
                    if((effect == 'taxing' or effect == 'taxed') and self.status_effects[effect] == 1):
                        if(effect == 'taxing'):
                            createSFXEvent('chime_error')
                        self.set_base_stats(self.stars)
                except:
                    pass # Typically pass for strings, like current pill

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
    
    def check_cooldown_completion(self, updatedAbility = True, updatedKick = True, updatedBlock = True, updatedBoost = True):
        if(self.special_ability_cooldown <= 0 and updatedAbility):
            self.toggle_recharge_indicator('ability', 2)
        if(self.kick_cooldown <= 0 and updatedKick):
            self.toggle_recharge_indicator('kick', 2)
        if(self.block_cooldown <= 0 and updatedBlock):
            self.toggle_recharge_indicator('block', 2)
        if(self.boost_cooldown_timer <= 0 and updatedBoost):
            self.toggle_recharge_indicator('boost', 2)

    def update_ability_icon(self, icon):
        self.ability_icon = icon
        self.recharge_indicators['ability_swap'] = True

    def ability(self):
        if(self.special_ability == ""):
            pass
        else:
            special_ability = self.special_ability

        if(special_ability == 'boost'):
            self.boost()
        elif(special_ability == 'fireball'):
            if(self.special_ability_meter >= self.special_ability_cost and self.special_ability_timer <= 2):
                if(self.special_ability_timer > 0):
                    #If we were holding down the button before
                    self.used_ability = "fireball"
                    self.special_ability_timer = self.special_ability_cooldown_max #Set the cooldown between uses timer
                    self.special_ability_meter -= self.special_ability_maintenance #Remove some SA meter
                    self.holding_timer += 1
                else:
                    #If we ignite the ball
                    self.used_ability = "fireball"
                    self.special_ability_timer = self.special_ability_cooldown_max #Set the cooldown between uses timer
                    self.special_ability_meter -= self.special_ability_cost #Remove some SA meter
                    self.holding_timer = 0
                    createSFXEvent('fire')
        elif(special_ability == 'snowball'):
            if(self.special_ability_meter >= self.special_ability_cost and self.special_ability_timer <= 2):
                if(self.special_ability_timer > 0):
                    #If we were holding down the button before
                    self.used_ability = "snowball"
                    self.special_ability_timer = self.special_ability_cooldown_max #Set the cooldown between uses timer
                    self.special_ability_meter -= self.special_ability_maintenance #Remove some SA meter
                    self.holding_timer += 1
                else:
                    #If we ignite the ball
                    self.used_ability = "snowball"
                    self.special_ability_timer = self.special_ability_cooldown_max #Set the cooldown between uses timer
                    self.special_ability_meter -= self.special_ability_cost #Remove some SA meter
                    self.holding_timer = 0 # Reset holding timer
                    createSFXEvent('ice')
        elif(special_ability == 'geyser'):
            if(self.special_ability_meter >= self.special_ability_cost and self.special_ability_timer <= 2):
                if(self.special_ability_timer > 0):
                    #If we were holding down the button before
                    self.used_ability = "geyser"
                    self.special_ability_timer = self.special_ability_cooldown_max #Set the cooldown between uses timer
                    self.special_ability_meter -= self.special_ability_maintenance #Remove some SA meter
                    self.holding_timer += 1
                else:
                    #If we ignite the ball
                    self.used_ability = "geyser"
                    self.special_ability_timer = self.special_ability_cooldown_max #Set the cooldown between uses timer
                    self.special_ability_meter -= self.special_ability_cost #Remove some SA meter
                    self.holding_timer = 0
                    createSFXEvent('water')
        elif(special_ability == "spire"):
            if(self.special_ability_meter >= self.special_ability_cost and self.special_ability_cooldown <= 0):
                #Spire activation
                self.used_ability = "spire_wait"
                self.special_ability_cooldown = self.special_ability_cooldown_max
                self.special_ability_timer = self.special_ability_cooldown_max #Set the cooldown between uses timer
                self.special_ability_meter -= self.special_ability_cost #Remove some SA meter
        elif(special_ability == "thunderbolt"):
            if(self.special_ability_meter >= self.special_ability_cost and self.special_ability_cooldown <= 0):
                #Thunderbolt activation
                self.used_ability = 'thunderbolt_wait' #This is done for a technical reason, to prevent premature electrocution
                self.special_ability_cooldown = self.special_ability_cooldown_max
                self.special_ability_timer = self.special_ability_cooldown #Set the cooldown between uses timer
                self.special_ability_meter -= self.special_ability_cost #Remove some SA meter
        elif(special_ability == "gale"):
            if(self.special_ability_meter >= self.special_ability_cost and self.special_ability_timer <= 2):
                if(self.special_ability_timer > 0):
                    #If we were holding down the button before
                    self.used_ability = "gale"
                    self.special_ability_timer = self.special_ability_cooldown_max #Set the cooldown between uses timer
                    self.special_ability_meter -= self.special_ability_maintenance #Remove some SA meter
                    self.holding_timer += 1
                else:
                    #If we ignite the ball
                    self.used_ability = "gale"
                    self.special_ability_timer = self.special_ability_cooldown_max #Set the cooldown between uses timer
                    self.special_ability_meter -= self.special_ability_cost #Remove some SA meter
                    self.holding_timer = 0
                    createSFXEvent('gale')
        elif(special_ability == "c&d"):
            if(self.special_ability_meter >= self.special_ability_cost and self.special_ability_cooldown <= 0):
                self.used_ability = "c&d"
                self.special_ability_cooldown = self.special_ability_cooldown_max
                self.special_ability_timer = self.special_ability_cooldown
                self.special_ability_meter -= self.special_ability_cost
        elif(special_ability == "pill"):
            if(self.special_ability_meter >= self.special_ability_cost and self.special_ability_cooldown <= 0):
                # Spend cost and activate cooldown
                self.special_ability_cooldown = self.special_ability_cooldown_max
                self.special_ability_timer = self.special_ability_cooldown
                self.special_ability_meter -= self.special_ability_cost
                self.used_ability = "pill"

                # Activate the correct effect based on self.status_effects['pill']
                if(self.status_effects['pill'] == 'pill_heal'):
                    if(self.hp == self.max_hp):
                        sac = bool(self.special_ability_cooldown > 0)
                        skc = bool(self.kick_cooldown > 0)
                        slc = bool(self.block_cooldown > 0)
                        sbc = bool(self.boost_cooldown_timer > 0)
                        self.special_ability_cooldown -= 15
                        self.kick_cooldown -= 15
                        self.block_cooldown -= 15
                        if(self.boost_cooldown_timer > 0):
                            self.boost_cooldown_timer -= 15
                        self.check_cooldown_completion(sac, skc, slc, sbc)
                    else:
                        self.heal_hp(heal_amt = 1)
                elif(self.status_effects['pill'] == 'pill_cooldown'):
                    sac = bool(self.special_ability_cooldown > 0)
                    skc = bool(self.kick_cooldown > 0)
                    slc = bool(self.block_cooldown > 0)
                    sbc = bool(self.boost_cooldown_timer > 0)
                    self.special_ability_cooldown -= 90
                    self.kick_cooldown -= 90
                    self.block_cooldown -= 90
                    if(self.boost_cooldown_timer > 0):
                        self.boost_cooldown_timer -= 90
                    self.check_cooldown_completion(sac, skc, slc, sbc)

                else:
                    self.boost(boost_cost = 0, boost_duration=120, boost_cooldown=0, ignore_cooldown=True)

                
                pill_list = ['pill_boost', 'pill_cooldown', 'pill_heal']
                pill_weights = [0 if x <= 0 else x for x in self.status_effects['pill_weights'].values()]
                print("PRE", self.status_effects['pill_weights'])
                current_pill = random.choices(pill_list, weights = pill_weights)[0]
                self.status_effects['pill'] = current_pill
                print("CHOSEN", current_pill)
<<<<<<< HEAD

                def return_inc_weight():
                    print(round((self.max_hp - self.hp) / 5))
                    if(round((self.max_hp - self.hp) / 5) <= 2):
                        return round((self.max_hp - self.hp) / 5)
                    else:
                        return 2

                if(self.hp <= self.max_hp):
                    self.status_effects['pill_weights']['pill_heal'] += return_inc_weight() # Prioritize healing
                    self.status_effects['pill_weights'][current_pill] -= return_inc_weight()
=======
                
                if(self.hp <= self.max_hp//2):
                    self.status_effects['pill_weights']['pill_heal'] += 2 # Prioritize healing
                    self.status_effects['pill_weights'][current_pill] -= 2
>>>>>>> parent of 5b28844 (Incrementing Health Pill Chance.)
                else:
                    for pill in self.status_effects['pill_weights']:
                        self.status_effects['pill_weights'][pill] += 1 # Add 1 to each
                    self.status_effects['pill_weights'][current_pill] -= 3 # Effectively subtracting 2
                print("~~~~~~~~~~~~~~~~~~~~~~~~~~")


                self.update_ability_icon(cwd + "/resources/images/ability_icons/{}.png".format(self.status_effects['pill']))
        elif(special_ability == "tax"):
            if(self.special_ability_meter >= self.special_ability_cost and self.special_ability_cooldown <= 0):
                self.used_ability = "tax"
                self.special_ability_cooldown = self.special_ability_cooldown_max
                self.special_ability_timer = self.special_ability_cooldown
                self.special_ability_meter -= self.special_ability_cost

                skc = bool(self.kick_cooldown > 0)
                slc = bool(self.block_cooldown > 0)
                sbc = bool(self.boost_cooldown_timer > 0)
                self.kick_cooldown -= 60
                self.block_cooldown -= 60
                if(self.boost_cooldown_timer > 0):
                    self.boost_cooldown_timer -= 60
                self.check_cooldown_completion(updatedKick=skc, updatedBlock=slc, updatedBoost=sbc)

                createSFXEvent('chime_progress')
        elif(special_ability == "stoplight"):
            if(self.special_ability_meter >= self.special_ability_cost and self.special_ability_cooldown <= 0):
                self.used_ability = "stoplight"
                self.special_ability_cooldown = self.special_ability_cooldown_max
                self.special_ability_timer = self.special_ability_cooldown
                self.special_ability_meter -= self.special_ability_cost
                self.block_cooldown += 60
                createSFXEvent('chime_progress')
        elif(special_ability == "starpunch"):
            if(self.special_ability_meter >= self.special_ability_cost and self.special_ability_cooldown <= 0):
                self.used_ability = "starpunch_wait"
                self.special_ability_cooldown = self.special_ability_cooldown_max
                self.special_ability_timer = self.special_ability_cooldown
                self.special_ability_meter -= self.special_ability_cost
                self.kick_cooldown += 60
                createSFXEvent('chime_progress')


    def kick(self):
        if(self.kick_cooldown <= 0):
            createSFXEvent('kick')
            self.block_cooldown += 5 * (self.block_cooldown_rate)
            self.kick_timer = 2
            self.kick_cooldown = self.kick_cooldown_max
            self.collision_timer = 0
            self.collision_distance = 175
            self.kick_visualization = self.kick_visualization_max
            self.info['kick_count'] += 1

    def block(self):
        if(self.block_cooldown <= 0):
            createSFXEvent('block')
            self.kick_cooldown += 5 * (self.kick_cooldown_rate)
            self.block_cooldown = self.block_cooldown_max #Set block cooldown
            self.block_timer = self.block_timer_max #Set active block timer
            self.movement_lock = 30
            self.x_speed = 0
            if(self.y_speed < 0): #If we are moving upwards, halt your momentum!
                self.y_speed = 0
            self.info['block_count'] += 1

    def boost(self, boost_cost = None, boost_duration = None, boost_cooldown = None, ignore_cooldown = None):
        if(boost_cost is None):
            boost_cost = self.boost_cost

        if(self.special_ability_meter >= boost_cost and (self.boost_cooldown_timer <= 0 or ignore_cooldown is not None)):
            createSFXEvent('boost')
            self.special_ability_meter -= boost_cost # Remove some SA meter
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
        #Hit self with Lightning bolt
        if(self.used_ability == "thunderbolt" and self.special_ability_timer == self.special_ability_cooldown_max - self.special_ability_delay
        and ball.x_center - 175 <= self.x_center <= ball.x_center + 175):
            self.boost(boost_cost = 0, boost_duration=120, boost_cooldown=0, ignore_cooldown=True)


        if(self.used_ability == "spire" and self.special_ability_timer == self.special_ability_cooldown_max - self.special_ability_delay
        and ball.x_center - 150 <= blob.x_center <= ball.x_center + 150):
            if(blob.block_timer == 0):
                blob.take_damage(y_speed_mod = -40 - (5 * (blob.gravity_mod - 1.05)), stun_amount = 20)
            else:
                blob.take_damage(damage=0)
                blob.block_cooldown += 30
        elif(self.used_ability == "thunderbolt" and self.special_ability_timer == self.special_ability_cooldown_max - self.special_ability_delay
        and ball.x_center - 150 <= blob.x_center <= ball.x_center + 150):
            blob.take_damage()
        elif((self.used_ability == "gale") or \
            (blob.used_ability == "gale")):
            if blob.y_pos != blob.ground and not blob.block_timer: #Gale Affecting the opponent
                if(self.player == 1 and self.used_ability == "gale"): #Airborne
                    blob.x_pos += 7
                elif(self.player == 2 and self.used_ability == "gale"):
                    blob.x_pos -= 7
        elif(self.used_ability == "c&d"):
            blob.status_effects['judged'] = self.special_ability_duration
        elif(self.used_ability == "tax"):
            self.status_effects['taxing'] = self.special_ability_duration
            blob.status_effects['taxed'] = self.special_ability_duration
            self.set_base_stats(blob.return_stars())
            blob.set_base_stats(self.return_stars())
            '''if(blob.kick_cooldown < self.kick_cooldown):
                self.kick_cooldown = (self.kick_cooldown + blob.kick_cooldown)//2
            
            if(blob.block_cooldown < self.block_cooldown):
                self.block_cooldown = (self.block_cooldown + blob.block_cooldown)//2

            if(blob.boost_cooldown_timer < self.boost_cooldown_timer):
                self.boost_cooldown_timer = (self.boost_cooldown_timer + blob.boost_cooldown_timer)//2'''

        elif(self.used_ability == "stoplight"):
            blob.collision_timer = 30
        
        elif(self.used_ability == "starpunch"):
            if(self.x_center - (1.5 * 250) <= blob.x_center <= self.x_center + (1.5 * 250)):
                if(self.y_center - (1.1 * 300) <= blob.y_center <= self.y_center + 300):
                    accumulated_damage = 3
                    stun_amount = 30
                    if(self.boost_timer):
                        accumulated_damage += 1
                    if(((blob.player == 2 and blob.x_pos >= blob.danger_zone) or (blob.player == 1 and blob.x_pos <= blob.danger_zone)) and blob.danger_zone_enabled):
                        #Take additional damage from kicks if you are hiding by your goal
                        accumulated_damage += 1
                    
                    if(blob.block_timer):
                        accumulated_damage -= 2
                        stun_amount = 0

                    blob.take_damage(damage = accumulated_damage, unblockable=True, unclankable=True, stun_amount = stun_amount,)

    def take_damage(self, damage = 1, unblockable = False, unclankable = False, damage_flash_timer = 60, y_speed_mod = 0, stun_amount = 0,\
        show_parry = True):
        damage_taken = False
        def check_block():  # Returns true if the hit goes through
            if(self.block_timer):  # Blocking?
                if(show_parry):
                    self.parried = 2
                    self.info['parries'] += 1
                    createSFXEvent('parry')
                return False # We failed the block check, don't take damage
            else:
                
                return True # Return true if the block check passes

        def check_clank(): # Returns true if the hit goes through
            if(self.kick_timer == 1):  # Kicking?
                self.clanked = 2
                self.info['clanks'] += 1
                createSFXEvent('clank')
                return False # We failed the clank check, don't take damage
            else:
                return True # Return true if the clank check passes
                
        if(unblockable and unclankable):
            check_block()
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
            self.status_effects['stunned'] = stun_amount
            self.y_speed = y_speed_mod
            createSFXEvent('hit')
            if(not self.recharge_indicators['damage_flash']):  # If we're hit twice on the same frame, don't disable the flash!
                self.toggle_recharge_indicator('damage_flash')

    def heal_hp(self, heal_amt = 1, overheal = False):
        if overheal:
            self.hp += heal_amt
            self.toggle_recharge_indicator('heal_flash')
        else:
            self.hp += heal_amt
            if(self.hp > self.max_hp):
                self.hp = self.max_hp
            else:
                self.toggle_recharge_indicator('heal_flash')

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
        self.status_effects['taxed'] = 0
        self.status_effects['taxing'] = 0
        self.status_effects['stunned'] = 0
        self.set_base_stats(self.stars)
        
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
        
        if(self.movement_lock > 0 or self.status_effects['stunned']):
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
                        if(self.x_speed > 0):
                            self.x_speed -= 1.2 * self.traction # Turn around faster by holding left
                        else:
                            self.x_speed -= self.traction # Accelerate based off of traction
                    else:
                        prev_speed = self.x_speed
                        self.x_speed = -1*self.top_speed #If at max speed, maintain it
                        if(round(prev_speed) == self.top_speed):
                            self.info['wavebounces'] += 1
                            createSFXEvent('wavebounce')
                        
            elif(not 'left' in pressed and 'right' in pressed): #If holding right but not left
                self.facing = 'right'
                if(self.x_pos >= 1700): #Are we in danger of going off screen?
                    self.x_speed = 0
                    self.x_pos = 1700
                else:
                    if(abs(self.x_speed) < self.top_speed):
                        if(self.x_speed < 0):
                            self.x_speed += 1.2 * self.traction # Turn around faster by holding left
                        else:
                            self.x_speed += self.traction # Accelerate based off of traction
                    else:
                        prev_speed = self.x_speed
                        self.x_speed = self.top_speed #If at max speed, maintain it
                        if(round(prev_speed) == -1 * self.top_speed):
                            self.info['wavebounces'] += 1
                            createSFXEvent('wavebounce') 
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
                        if(self.x_speed > 0):
                            self.x_speed -= 1.5 * self.friction # Turn around faster by holding left
                        else:
                            self.x_speed -= self.friction # Accelerate based off of friction
                    else:
                        prev_speed = self.x_speed
                        self.x_speed = -1*self.top_speed #If at max speed, maintain it
                        if(round(prev_speed) == self.top_speed):
                            self.info['wavebounces'] += 1
                            createSFXEvent('wavebounce') 
            elif(not 'left' in pressed and 'right' in pressed): #If holding right but not left
                self.facing = 'right'
                if(self.x_pos >= 1700): #Are we in danger of going off screen?
                    self.x_speed = 0
                    self.x_pos = 1700
                else:
                    if(abs(self.x_speed) < self.top_speed):
                        if(self.x_speed < 0):
                            self.x_speed += 1.5 * self.friction # Turn around faster by holding left
                        else:
                            self.x_speed += self.friction # Accelerate based off of friction
                    else:
                        prev_speed = self.x_speed
                        self.x_speed = self.top_speed #If at max speed, maintain it
                        if(round(prev_speed) == -1 * self.top_speed):
                            self.info['wavebounces'] += 1
                            createSFXEvent('wavebounce') 
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
        elif('up' in pressed and self.y_speed < 0):
            self.shorthopping = False
        elif('up' not in pressed and self.y_speed < 0):
            self.shorthopping = True
        
        if('down' in pressed):
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
            if(self.y_speed < 0):
                if(self.shorthopping):
                    self.y_speed += self.gravity_mod
                else:
                    self.y_speed += self.gravity_stars
            else:
                if(self.fastfalling):
                    self.y_speed += self.gravity_mod
                else:
                    self.y_speed += self.gravity_stars
        else:
            self.info['time_grounded'] += 1
            self.info['time_grounded_seconds'] = round(self.info['time_grounded']/60, 2)
        
        if(self.fastfalling and self.y_pos == Blob.ground): #If you land, cancel the fastfall.
            self.fastfalling = False
            self.shorthopping = False
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
    
    def set_base_stats(self, stars):
        self.top_speed = 10+(1*stars['top_speed'])
        self.base_top_speed = self.top_speed
        self.traction = 0.2 + (stars['traction'] * 0.15) #Each star increases traction
        self.friction = 0.2 + (stars['friction'] * 0.15) #Each star increases friction
        self.base_traction = self.traction #Non-boosted
        self.base_friction = self.friction #No boost
        self.gravity_stars = round(.3 + (stars['gravity'] * .15), 3) #Each star increases gravity
        self.gravity_mod = round(.3 + (stars['gravity'] + 5) * .15, 3) #Fastfalling increases gravity
        self.jump_force = 14.5 + (stars['gravity'] * 2) #Initial velocity is based off of gravity
        self.boost_top_speed = 10+(1*stars['top_speed'] + 3) #This stat is increased by 3 stars
        self.boost_traction = 0.2 + ((stars['traction'] + 5) * 0.15) #These stats are increased by 5 stars
        self.boost_friction = 0.2 + ((stars['friction'] + 5) * 0.15)

        if(self.boost_timer > 0):
            self.top_speed = self.boost_top_speed
            self.traction = self.boost_traction
            self.friction = self.boost_friction

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

    def toggle_recharge_indicator(self, indicator, set_indicator = 1):
        indicator_state = self.recharge_indicators[indicator]
        if indicator_state == 2:
            indicator_state = 1
        elif(indicator_state == 1):
            indicator_state = 0
        else:
            indicator_state = set_indicator
        self.recharge_indicators[indicator] = indicator_state
    
    def __str__(self):
        return f"Player {self.player}: {self.species}."

    def return_stars(self):
        return self.stars