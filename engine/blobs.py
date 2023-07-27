import math
import os
import random
from engine.environmental_modifiers import create_environmental_modifier
from engine.handle_input import merge_inputs
from resources.graphics_engine.display_particles import draw_teleportation_pfx
from resources.sound_engine.sfx_event import createSFXEvent
from engine.blob_stats import species_to_stars, species_to_ability_icon
cwd = os.getcwd()

# INSTRUCTIONS FOR ADDING A BLOB TO THE GAME
# Add the Blob's Stats to the species_to_stars function in blob_stats.py (see other blobs for a guide)
# Classify that Blob's ability in ability_to_classification function (so it will show the cooldown)
# Add that Blob's image in species_to_image (make sure that the image is in the resources/images/blobs folder)
# Adding to the above point, Key 0 is the default costume. It loads in the alive sprite (first item in the tuple) and the dead sprite
# Add that Blob's ability icon (make sure that the image is in the resources/images/ability_icons folder)
# In the Blob class, navigate to the ability method to make sure that the ability can be activated.
# Depending on the ability, check the cooldown method 
# If the ability has the potential to impact another blob, update the check_ability_collision method
# If the ability has the potential to impact the ball, update the Ball class' check_blob_ability method
# In engine/unlocks.py, update css_selector_list and original_css_display_list to allow that blob to be selected
# In engine/unlocks.py, update css_location_dict with the intended location of that blob
# In engine/unlocks.py, update blob_unlock_dict with the CSS position of the blob
# In engine/endgame.py, update attempt_unlocks with the number of games it takes to unlock that blob
# In engine/popup_list.py, update blob_unlock_popups to include the new blob's unlock text
# In resources/graphics_engine/almanac_blob_array.py, update the Blob Array there to show your blob in the almanac
# In engine/blob_tips.py, add the blob's ID to the dictionary at the bottom and add an array containing tips

# INSTRUCTIONS FOR ADDING ADDITIONAL COSTUMES
# Add Costume sprite + corresponding death sprite to resources/images/blobs
# In species_to_image, under the blob who you want to add a costume to, add a new key
# The key needs to be an integer (ideally one greater than the next largest costume)
# The left half of the tuple is the living sprite. The right half is the death sprite.
# In unlocks.py, under costume_unlock_dict, navigate to the blob who you want to add a costume to
# Add a new entry to the nested dictionary (formatted costumename_#) 
# The number at the end is very important and should match the key in species_to_image
# To be able to unlock the costume:
# In engine/endgame.py under the attempt_costume_unlocks function, find (or add) the blob who you want to tie the costume to
# Add a new key/value pair, with the key being the number of matches it takes to unlock that costume
# In engine/popup_list.py, add an entry formatted as blob/alt_# - this dictates what the popup screen says and shows

def ability_to_classification(ability):
    held_abilities = ['fireball', 'snowball', 'geyser', 'gale', 'hook', 'gluegun']
    if(ability in held_abilities):
        return "held"
    instant_abilities = ['boost', 'c&d', 'pill', 'tax', 'stoplight', 'mirror', 'teleport', 'cardpack', 'monado', 'spike', 'shop', 'bubble']
    if(ability in instant_abilities):
        return "instant"
    delayed_abilities = ['spire', 'thunderbolt', 'starpunch']
    if(ability in delayed_abilities):
        return "delayed"
    return "other"

#TODO: Implement costume support and include death sprites
def species_to_image(species, costume):
    global cwd
    blob_cwd = cwd + '/resources/images/blobs/'
    image_dict = {
        'quirkless': {0: (blob_cwd + "quirkless_blob.png", blob_cwd + "quirkless_blob_-1.png"), 1: (blob_cwd + "quirkless_blob_1.png", blob_cwd + "quirkless_blob_-1.png"), 2: (blob_cwd + "shadow_blob.png", blob_cwd + "quirkless_blob_-1.png")},
        'fire': {0: (blob_cwd + "fire_blob.png", blob_cwd + "fire_blob_-1.png"), 1: (blob_cwd + "fire_blob_1.png", blob_cwd + "fire_blob_-1.png")},
        'ice': {0: (blob_cwd + "ice_blob.png", blob_cwd + "ice_blob_-1.png"), 1: (blob_cwd + "ice_blob_1.png", blob_cwd + "ice_blob_-1.png")},
        'water': {0: (blob_cwd + "water_blob.png", blob_cwd + "water_blob_-1.png"), 1: (blob_cwd + "water_blob_1.png", blob_cwd + "water_blob_-1.png")},
        'rock': {0: (blob_cwd + "rock_blob.png", blob_cwd + "rock_blob_-1.png"), 1: (blob_cwd + "rock_blob_1.png", blob_cwd + "rock_blob_-1.png")},
        'lightning': {0: (blob_cwd + "lightning_blob.png", blob_cwd + "lightning_blob_-1.png"), 1: (blob_cwd + "lightning_blob_1.png", blob_cwd + "lightning_blob_-1.png")},
        'wind': {0: (blob_cwd + "wind_blob.png", blob_cwd + "wind_blob_-1.png"), 1: (blob_cwd + "wind_blob_1.png", blob_cwd + "wind_blob_-1.png")},
        'judge': {0: (blob_cwd + "judge_blob.png", blob_cwd + "judge_blob_-1.png"), 1: (blob_cwd + "judge_blob_1.png", blob_cwd + "judge_blob_-1.png")},
        'doctor': {0: (blob_cwd + "doctor_blob.png", blob_cwd + "doctor_blob_-1.png"), 1: (blob_cwd + "doctor_blob_1.png", blob_cwd + "doctor_blob_-1.png")},
        'king': {0: (blob_cwd + "king_blob.png", blob_cwd + "king_blob_-1.png"), 1: (blob_cwd + "king_blob_1.png", blob_cwd + "king_blob_-1.png")},
        'cop': {0: (blob_cwd + "cop_blob.png", blob_cwd + "cop_blob_-1.png"), 1: (blob_cwd + "cop_blob_1.png", blob_cwd + "cop_blob_-1.png")},
        'boxer': {0: (blob_cwd + "boxer_blob.png", blob_cwd + "boxer_blob_-1.png"), 1: (blob_cwd + "boxer_blob_1.png", blob_cwd + "boxer_blob_-1.png")},
        'mirror': {0: (blob_cwd + "mirror_blob.png", blob_cwd + "mirror_blob_-1.png"), 1: (blob_cwd + "mirror_blob_1.png", blob_cwd + "mirror_blob_-1.png")},
        'fisher': {0: (blob_cwd + "fisher_blob.png", blob_cwd + "fisher_blob_-1.png"), 1: (blob_cwd + "fisher_blob_1.png", blob_cwd + "fisher_blob_-1.png"), 2: (blob_cwd + "fisher_blob_2.png", blob_cwd + "fisher_blob_-2.png")},
        'glue': {0: (blob_cwd + "glue_blob.png", blob_cwd + "glue_blob_-1.png"), 1: (blob_cwd + "glue_blob_1.png", blob_cwd + "glue_blob_-1.png")},
        'arcade': {0: (blob_cwd + "arcade_blob.png", blob_cwd + "arcade_blob_-1.png"), 1: (blob_cwd + "arcade_blob_1.png", blob_cwd + "arcade_blob_-1.png")},
        'joker': {0: (blob_cwd + "joker_blob.png", blob_cwd + "joker_blob_-1.png"), 1: (blob_cwd + "joker_blob_1.png", blob_cwd + "joker_blob_-1.png"), 2: (blob_cwd + "joker_blob_2.png", blob_cwd + "joker_blob_-1.png"), 3: (blob_cwd + "joker_blob_3.png", blob_cwd + "joker_blob_-2.png")},
        'taco': {0: (blob_cwd + "taco_blob.png", blob_cwd + "taco_blob_-1.png"), 1: (blob_cwd + "taco_blob_1.png", blob_cwd + "taco_blob_-1.png")},
        'cactus': {0: (blob_cwd + "cactus_blob.png", blob_cwd + "cactus_blob_-1.png"), 1: (blob_cwd + "cactus_blob_1.png", blob_cwd + "cactus_blob_-1.png")},
        'merchant': {0: (blob_cwd + "merchant_blob.png", blob_cwd + "merchant_blob_-1.png"), 1: (blob_cwd + "merchant_blob_1.png", blob_cwd + "merchant_blob_-1.png")},
        'bubble': {0: (blob_cwd + "random_blob.png", blob_cwd + "random_blob.png"), 1: (blob_cwd + "random_blob.png", blob_cwd + "random_blob.png")},
        'random': {0: (blob_cwd + "random_blob.png", blob_cwd + "random_blob.png")},
        'locked': {0: (blob_cwd + "locked_blob.png", blob_cwd + "locked_blob.png")},
        'invisible': {0: (blob_cwd + "invisible_blob.png", blob_cwd + "invisible_blob.png")},
    }

    return image_dict[species][costume]

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
    special_ability_charge_base = 1, costume = 0, danger_zone_enabled = True, is_cpu = False, stat_overrides = []):
        self.species = species
        self.player = player #Player 1 or 2
        self.all_blobs = {}
        if(player == 1):
            self.danger_zone = 225
        else:
            self.danger_zone = 1475
        self.is_cpu = is_cpu
        self.cpu_memory = {'press_queue': [], 'game_state': '', 'current_play': ''}
        self.costume = costume
        self.image, self.image_death = species_to_image(species, costume)
        self.ability_icon = species_to_ability_icon(species)
        self.stars = species_to_stars(species, stat_overrides) #Gets many values for each blob
        self.max_hp = int(2 * (self.stars['max_hp'] + 3)) #Each star adds an additional HP.
        self.hp = self.max_hp
        self.top_speed = 10+(1*self.stars['top_speed']) #Each star adds some speed
        self.base_top_speed = self.top_speed #Non-boosted
        self.x_speed = 0
        self.y_speed = 0
        self.x_pos = x_pos #Where the blob is on the X axis
        self.y_pos = y_pos #Where the blob is on the Y axis, 1200 is grounded
        self.x_center = x_pos + 83
        self.y_center = y_pos + 110
        self.facing = facing #Where the blob is currently facing
        self.traction = 0.2 + (self.stars['traction'] * 0.15) #Each star increases traction
        self.friction = 0.2 + (self.stars['friction'] * 0.15) #Each star increases friction
        self.base_traction = self.traction #Non-boosted
        self.base_friction = self.friction #No boost
        self.gravity_stars = round(.3 + (self.stars['gravity'] * .15), 3) #Each star increases gravity
        self.gravity_mod = self.gravity_stars * 3 #Fastfalling increases gravity
        self.fastfalling = False
        self.shorthopping = False
        self.jump_force = 14.5 + (self.stars['gravity'] * 2) #Initial velocity is based off of gravity
        
        self.kick_cooldown_rate = 2 #Each star reduces kick cooldown
        self.kick_cooldown = 0 #Cooldown timer between kicks
        self.kick_timer = 0 #Active frames of kick
        self.kick_cooldown_max = (300 + 15 * (5 - self.stars['kick_cooldown_rate'])) * Blob.timer_multiplier
        self.kick_visualization = 0
        self.kick_visualization_max = 15

        self.block_cooldown_rate = 2 #Each star reduces block cooldown
        self.block_cooldown = 0 #Block cooldown timer
        self.block_timer = 0 #How much time is left in the current block
        self.block_timer_max = 15 #How many frames a block lasts.
        self.block_cooldown_max = (360 + 15 * (5 - self.stars['block_cooldown_rate'])) * Blob.timer_multiplier #How long the block cooldown lasts

        self.block_outer = 150
        self.block_inner = -25
        self.block_upper = -200
        self.block_lower = 200

        self.boost_cost = self.stars['boost_cost'] * Blob.nrg_multiplier #How much SA meter must be spent to boost
        self.boost_cooldown_rate = 2
        self.boost_cooldown_max = (300 + 30 *  (5 - self.stars['boost_cooldown_max'])) * Blob.timer_multiplier #Each star reduces boost cooldown
        self.boost_cooldown_timer = 0 #Timer that measures between boosts
        self.boost_duration = 60 + (30 * self.stars['boost_duration']) #Each star increases boost duration by half a second
        self.boost_timer = 0 #How much time is left in the current boost
        self.boost_top_speed = 10+(1*self.stars['top_speed'] + 3) #This stat is increased by 3 stars
        self.boost_traction = 0.2 + ((self.stars['traction'] + 5) * 0.15) #These stats are increased by 5 stars
        self.boost_friction = 0.2 + ((self.stars['friction'] + 5) * 0.15) 

        self.down_holding_timer = 0
        self.focus_lock = 0 #Timer that locks movement when a blob is focusing
        self.focus_lock_max = 60
        self.focusing = False
        self.impact_land_frames = 0 #Locks the player from focusing after landing (fastfall leniency)

        self.special_ability = self.stars['special_ability'] #Special Ability of a Blob
        self.ability_classification = ability_to_classification(self.special_ability)
        self.special_ability_max = self.stars['special_ability_max'] * Blob.nrg_multiplier #Highest that the SA gauge can go
        self.special_ability_cost = self.stars['special_ability_cost'] * Blob.nrg_multiplier #Price to activate SA
        self.special_ability_maintenance = self.stars['special_ability_maintenance'] * Blob.nrg_multiplier #Price to maintain SA
        self.special_ability_charge = 1 * Blob.nrg_multiplier #Charge rate. Each frame increases the SA meter by 1 point, or more if focusing
        self.special_ability_meter = 0 #Amount of SA charge stored up
        self.special_ability_timer = 0 #Timer that counts down between uses of an SA
        self.special_ability_duration = 0 #Time that a SA is active
        self.special_ability_cooldown = 0 #Cooldown between uses
        self.special_ability_cooldown_max = self.stars['special_ability_cooldown'] * Blob.timer_multiplier
        self.special_ability_charge_base = special_ability_charge_base * Blob.nrg_multiplier
        self.special_ability_duration = self.stars['special_ability_duration']
        self.special_ability_delay = self.stars['special_ability_delay']
        self.special_ability_cooldown_rate = 2
        self.used_ability = {}
        self.ability_holding_timer = 0 # Used for held abilities

        self.collision_distance = 104 #Used for calculating ball collisions
        self.collision_timer = 0 #Prevents double hitting in certain circumstances

        self.damage_flash_timer = 0 #Flashes when damage is taken
        self.parried = False #True when parrying
        self.perfect_parried = False
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
        self.wavedash_lock = 0 #Caused if the blob has wavedashed
        self.jump_lock = 0 #Caused by certain abilities and prevents jumps
        self.danger_zone_enabled = danger_zone_enabled
        self.info = {
            'species': self.species,
            'costume': self.costume,
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
            'wavedashes': 0,
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
            "pill": 'pill_cooldown',
            "pill_weights": {'pill_boost': 3, 'pill_cooldown': 3, 'pill_heal': 3},
            "menu": {'open': False, 'type': '', 'direction': 'neutral', 'time': 0},
            "cards": {'ability': None, 'kick': None, 'block': None, 'boost': None, 'equipped': set(), 'pool': {'c&d', 'pill', 'tax', 'stoplight', 'mirror', 'teleport', 'spire', 'thunderbolt', 'starpunch'}, 'recharge': set(), 'pulled': [], 'joker_particle': False},
            "monado_timer": 0,
            "monado_effect": None,
            "monado_smash_cooldown": 0,
            "monado_shield_cooldown": 0,
            "monado_speed_cooldown": 0,
            "monado_jump_cooldown": 0,
            "shop": {'offense_sale': 'dream_wielder', 'focus_sale': 'baldur_shell', 'passive_sale': 'soul_catcher', 'defense_sale': 'sharp_shadow', 'offense_equip': None, 'focus_equip': None, 'passive_equip': None, 'defense_equip': None, 'offense_durability': 0, 'focus_durability': 0, 'passive_durability': 0, 'defense_durability': 0, 'purchase_particle': None, 'discard_particle': None},

            "teleporter": [1],
            "taxing": 0,
            "taxed": 0,
            "stunned": 0,
            "reflecting": 0,
            "reflect_break": 0,
            "glued": 0,
            "buttered": 0,
            "hypothermia": 0,
            "steroided": 0,
            "overheat": 0,
            "stoplit": 0,
            "loaned": 0,
            "hyped": 0,
            "silenced": 0,
            "nrg_fatigue": 0,
        }

        if(self.species == "doctor"):
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
    timer_multiplier = 2
    nrg_multiplier = 5

    def cooldown(self): #Reduces timers
        if(self.focusing):
            self.special_ability_charge = (self.special_ability_charge_base - (bool(self.status_effects["nrg_fatigue"]) * 3) + (bool(self.status_effects['shop']['passive_equip'] == 'soul_catcher') * 10)) * 5 
            self.info['time_focused'] += 1
            self.info['time_focused_seconds'] = round(self.info['time_focused']/60, 2)
            if(self.y_pos < Blob.ground):
                self.focusing = False
                self.focus_lock = 0
        else:
            self.special_ability_charge = self.special_ability_charge_base - (bool(self.status_effects["nrg_fatigue"]) * 3) + (bool(self.status_effects['shop']['passive_equip'] == 'soul_catcher') * 10)

        if(self.impact_land_frames):
            self.impact_land_frames -= 1

        if(self.focus_lock > 0):
            self.focus_lock -= 1
            if(self.status_effects['shop']['focus_equip'] == 'explosive_focus' or self.status_effects['shop']['focus_equip'] == 'soul_focus'):
                self.focus_lock -= 2
            if(self.status_effects['shop']['defense_equip'] == 'sharp_shadow' or self.species == "cactus"):
                self.focus_lock -= 2
            if(self.focus_lock == 0 and self.status_effects['shop']['focus_equip'] == 'explosive_focus'):
                self.kick(ignore_cooldown=True)
                self.status_effects['shop']['focus_durability'] -= 1
            if(self.focus_lock == 0 and self.status_effects['shop']['focus_equip'] == 'soul_focus'):
                self.heal_hp(heal_amt = 1, overheal = False)
                self.status_effects['shop']['focus_durability'] -= 1
            
            if(self.status_effects['shop']['focus_durability'] == 0 and self.status_effects['shop']['focus_equip']):
                self.status_effects['shop']['discard_particle'] = self.status_effects['shop']['focus_equip']
                self.status_effects['shop']['focus_equip'] = None
                
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
            if(self.ability_holding_timer % 18 == 17 and "fireball" in self.used_ability):
                createSFXEvent('fire')
            elif(self.ability_holding_timer % 20 == 19 and "snowball" in self.used_ability):
                createSFXEvent('ice')
            elif(self.ability_holding_timer % 12 == 11 and "geyser" in self.used_ability):
                createSFXEvent('water')
            elif(self.ability_holding_timer % 60 == 59 and "gale" in self.used_ability):
                createSFXEvent('gale')
            '''elif("thunderbolt" in self.used_ability and self.special_ability_timer == self.special_ability_cooldown_max - self.special_ability_delay - self.special_ability_duration):
                self.used_ability = {}
            elif("c&d" in self.used_ability and (self.special_ability_timer == self.special_ability_cooldown_max - 1 or self.species == "joker")):
                self.used_ability = {}
            elif("pill" in self.used_ability):
                if(self.used_ability["pill"] == 2):
                    self.used_ability["pill"] -= 1
                else:
                    self.used_ability = {}
            elif("tax" in self.used_ability and self.special_ability_timer == self.special_ability_cooldown_max - 1):
                self.used_ability = {}
            elif("stoplight" in self.used_ability and (self.special_ability_timer == self.special_ability_cooldown_max - 1 or self.species == 'joker')):
                self.used_ability["stoplight_pfx"] = 2
                self.used_ability.pop("stoplight")
            
            if("stoplight_pfx" in self.used_ability):
                if(self.used_ability["stoplight_pfx"] == 2):
                    self.used_ability["stoplight_pfx"] -= 1
                else:
                    self.used_ability = {}
            elif("starpunch" in self.used_ability):
                self.used_ability = {}
            elif("mirror" in self.used_ability and (self.special_ability_timer == self.special_ability_cooldown_max - 1 or self.species == 'joker')):
                self.used_ability = {}'''

            new_dict = {}

            for ability in self.used_ability:
                if(self.used_ability[ability] > 0):
                    new_dict[ability] = self.used_ability[ability] - 1
            
            self.used_ability = new_dict

            '''if(self.ability_holding_timer == 0):
                self.used_ability = {}'''

        for effect in self.status_effects:
            if(self.status_effects[effect]):
                try:
                    self.status_effects[effect] -= 1

                    if(effect in {'taxed', 'stunned', 'hypothermia', 'overheat', 'silenced', 'nrg_fatigue'} and self.status_effects['shop']['defense_equip'] == 'izumi_tear' and self.status_effects['shop']['defense_durability'] > 0):
                        self.status_effects[effect] = 1

                    if((effect == 'taxing' or effect == 'taxed') and self.status_effects[effect] == 1):
                        if(effect == 'taxing'):
                            createSFXEvent('chime_error')
                        self.set_base_stats(self.stars)
                        
                    
                    if(effect == 'overheat'):
                        self.kick_cooldown_rate = 1
                        self.block_cooldown_rate = 1
                        self.special_ability_cooldown_rate = 1
                        self.boost_cooldown_rate = 1
                    if(effect == 'loaned'):
                        self.kick_cooldown_rate += 4
                        self.block_cooldown_rate += 4
                        self.special_ability_cooldown_rate += 4
                        self.boost_cooldown_rate += 4
                    if(effect == 'hyped'):
                        self.kick_cooldown_rate += 1
                        self.block_cooldown_rate += 1
                        self.special_ability_cooldown_rate += 1
                        self.boost_cooldown_rate += 1
                    if(effect == 'monado_timer' and self.status_effects[effect] == 1):
                        self.status_effects['monado_effect'] = None
                    if(effect == 'monado_timer' and self.status_effects[effect] > 1 and self.status_effects['monado_effect'] == "JUMP"):
                        '''self.kick_cooldown_rate += 1
                        self.block_cooldown_rate += 1
                        self.special_ability_cooldown_rate += 1
                        self.boost_cooldown_rate += 1'''
                    
                    if(effect == 'monado_timer' and self.status_effects[effect] > 1 and self.status_effects['monado_effect'] == "SHIELD"):
                        self.block_cooldown_rate += 5
                    
                    if(effect == 'monado_timer' and self.status_effects[effect] > 1 and self.status_effects['monado_effect'] == "SMASH"):
                        self.kick_cooldown_rate += 3

                    
                except:
                    pass # Typically pass for strings, like current pill
        
        if(self.special_ability_cooldown > 0):
            self.special_ability_cooldown -= self.special_ability_cooldown_rate
            if(self.special_ability_cooldown <= 0):
                self.special_ability_cooldown = 0
                self.toggle_recharge_indicator('ability')

        if(self.kick_cooldown > 0):
            self.kick_cooldown -= self.kick_cooldown_rate
            if(self.kick_cooldown <= 0):
                self.kick_cooldown = 0
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
            if(self.block_cooldown <= 0):
                self.block_cooldown = 0
                self.toggle_recharge_indicator('block')
        
        if(self.boost_timer > 0): #Reduces duration of active boost by 1
            self.boost_timer -= 1 
            if(self.boost_timer <= 0): #Once the boost ends, revert to normal
                self.top_speed = 10+(1*self.stars['top_speed'])
                self.traction = 0.2 + (self.stars['traction'] * 0.15) #Each star increases traction
                self.friction = 0.2 + (self.stars['friction'] * 0.15) #Each star increases friction
        elif(self.boost_cooldown_timer > 0): #If the boost is over, cool down
            self.boost_cooldown_timer -= self.boost_cooldown_rate
            if(self.boost_cooldown_timer <= 0):
                self.boost_cooldown_timer = 0
                self.toggle_recharge_indicator('boost')

        self.special_ability_cooldown_rate = Blob.timer_multiplier
        self.kick_cooldown_rate = Blob.timer_multiplier
        self.block_cooldown_rate = Blob.timer_multiplier
        self.boost_cooldown_rate = Blob.timer_multiplier
       
        if(self.collision_timer > 0):
            self.collision_timer -=1 
        
        if(self.damage_flash_timer > 0):
            self.damage_flash_timer -= 1
            if((self.damage_flash_timer // 10) % 2 == 1):
                self.image = species_to_image('invisible', 0)[0]
            else:
                self.image = species_to_image(self.species, self.costume)[0]
        
        if(self.movement_lock > 0):
            self.movement_lock -= 1

        if(self.wavedash_lock > 0):
            self.wavedash_lock -= 1
        
        if(self.jump_lock > 0):
            self.jump_lock -= 1

        if(self.parried):
            self.parried -= 1
        
        if(self.perfect_parried):
            self.perfect_parried -= 1

        if(self.clanked):
            self.clanked -= 1

        if(self.status_effects['shop']['defense_durability'] == 0 and self.status_effects['shop']['defense_equip']):
                createSFXEvent('crunch')
                self.status_effects['shop']['discard_particle'] = self.status_effects['shop']['defense_equip']
                self.status_effects['shop']['defense_equip'] = None
        
        if(self.status_effects['shop']['focus_durability'] == 0 and self.status_effects['shop']['focus_equip']):
                createSFXEvent('crunch')
                self.status_effects['shop']['discard_particle'] = self.status_effects['shop']['focus_equip']
                self.status_effects['shop']['focus_equip'] = None
        
        if(self.status_effects['shop']['passive_durability'] == 0 and self.status_effects['shop']['passive_equip']):
            createSFXEvent('crunch')
            self.status_effects['shop']['discard_particle'] = self.status_effects['shop']['passive_equip']
            self.status_effects['shop']['passive_equip'] = None
        else:
            self.status_effects['shop']['passive_durability'] -= 1

        self.ability_cooldown_visualization = create_visualization(self.special_ability_cooldown/Blob.timer_multiplier)
        self.ability_cooldown_percentage = self.special_ability_cooldown/self.special_ability_cooldown_max
        self.kick_cooldown_visualization = create_visualization(self.kick_cooldown/self.kick_cooldown_rate)
        self.kick_cooldown_percentage = self.kick_cooldown/self.kick_cooldown_max
        self.block_cooldown_visualization = create_visualization(self.block_cooldown/self.block_cooldown_rate)
        self.block_cooldown_percentage = self.block_cooldown/self.block_cooldown_max
        self.boost_cooldown_visualization = create_visualization(self.boost_cooldown_timer/Blob.timer_multiplier)
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

    def ability(self, card = ""):
        if(card == "" and self.status_effects['cards']['ability']):
            special_ability = self.status_effects['cards']['ability']
            cost = 0
            maintenance = 0
            cooldown = 60
            used_card = True
        elif(card == ""):
            special_ability = self.special_ability
            cost = self.special_ability_cost
            maintenance = self.special_ability_maintenance
            cooldown = self.special_ability_cooldown_max
            used_card = False
        else:
            special_ability = card
            cost = 0
            maintenance = 0
            cooldown = 60
            used_card = True

        if(special_ability == 'boost'):
            self.boost()
        elif(special_ability == 'fireball'):
            if('fireball' in self.used_ability and self.special_ability_meter > maintenance):
                #If we were holding down the button before
                self.used_ability["fireball"] += 1
                self.special_ability_timer = cooldown #Set the cooldown between uses timer
                self.special_ability_meter -= maintenance #Remove some SA meter
                self.ability_holding_timer += 1
                if(self.ability_holding_timer % 45 == 0):
                    self.status_effects['monado_effect'] = "SPEED"
                    self.status_effects['monado_timer'] += 300
            elif(self.special_ability_meter > cost):
                #If we ignite the ball
                self.used_ability["fireball"] = 1
                self.special_ability_timer = self.special_ability_cooldown_max #Set the cooldown between uses timer
                self.special_ability_meter -= cost #Remove some SA meter
                self.ability_holding_timer = 0
                createSFXEvent('fire')
            else:
                return
        elif(special_ability == 'snowball'):
            if('snowball' in self.used_ability and self.special_ability_meter > maintenance):
                #If we were holding down the button before
                self.used_ability["snowball"] += 1
                self.special_ability_timer = self.special_ability_cooldown_max #Set the cooldown between uses timer
                self.special_ability_meter -= maintenance #Remove some SA meter
                self.ability_holding_timer += 1
            elif(self.special_ability_meter > cost):
                #If we ignite the ball
                self.used_ability["snowball"] = 1
                self.special_ability_timer = self.special_ability_cooldown_max #Set the cooldown between uses timer
                self.special_ability_meter -= cost #Remove some SA meter
                self.ability_holding_timer = 0 # Reset holding timer
                createSFXEvent('ice')
            else:
                return
        elif(special_ability == 'geyser'):
            if('geyser' in self.used_ability and self.special_ability_meter > maintenance):
                #If we were holding down the button before
                self.used_ability["geyser"] += 1
                self.special_ability_timer = self.special_ability_cooldown_max #Set the cooldown between uses timer
                self.special_ability_meter -= maintenance #Remove some SA meter
                self.ability_holding_timer += 1
            elif(self.special_ability_meter > cost):
                #If we ignite the ball
                self.used_ability["geyser"] = 1
                self.special_ability_timer = self.special_ability_cooldown_max #Set the cooldown between uses timer
                self.special_ability_meter -= cost #Remove some SA meter
                self.ability_holding_timer = 0
                createSFXEvent('water')
            else:
                return
        elif(special_ability == "spire"):
            if(self.special_ability_meter >= cost and self.special_ability_cooldown <= 0):
                if(self.special_ability != 'spire'):
                    special_ability_delay = 30
                else:
                    special_ability_delay = self.special_ability_delay
                #Spire activation
                createSFXEvent('glyph')
                #self.used_ability = "spire_wait"
                self.special_ability_cooldown = cooldown
                self.special_ability_timer = cooldown #Set the cooldown between uses timer
                self.special_ability_meter -= cost #Remove some SA meter
                create_environmental_modifier(player = self.player, affects = {'enemy', 'ball'}, species = 'spire_glyph', lifetime = special_ability_delay, y_pos = 700)
            else:
                return
        elif(special_ability == "thunderbolt"):
            if(self.special_ability_meter >= cost and self.special_ability_cooldown <= 0):
                #Thunderbolt activation
                #createSFXEvent('glyph')
                #self.used_ability = 'thunderbolt_wait' #This is done for a technical reason, to prevent premature electrocution

                if(self.special_ability != 'thunderbolt'):
                    special_ability_delay = 10
                else:
                    special_ability_delay = self.special_ability_delay

                self.special_ability_cooldown = cooldown
                self.special_ability_timer = self.special_ability_cooldown #Set the cooldown between uses timer
                self.special_ability_meter -= cost #Remove some SA meter
                create_environmental_modifier(player = self.player, affects = {'self', 'enemy', 'ball'}, species = 'thunder_glyph', lifetime = special_ability_delay, y_pos = 700)
            else:
                return
        elif(special_ability == "gale"):
            if('gale' in self.used_ability and self.special_ability_meter > maintenance):
                #If we were holding down the button before
                self.used_ability["gale"] += 1
                self.special_ability_timer = self.special_ability_cooldown_max #Set the cooldown between uses timer
                self.special_ability_meter -= maintenance #Remove some SA meter
                self.ability_holding_timer += 1
            elif(self.special_ability_meter > cost):
                #If we ignite the ball
                self.used_ability["gale"] = 1
                self.special_ability_timer = self.special_ability_cooldown_max #Set the cooldown between uses timer
                self.special_ability_meter -= cost #Remove some SA meter
                self.ability_holding_timer = 0
                createSFXEvent('gale')
            else:
                return
        elif(special_ability == "c&d"):
            if(self.special_ability_meter >= cost and self.special_ability_cooldown <= 0):
                self.used_ability["c&d"] = 2
                self.special_ability_cooldown = cooldown
                self.special_ability_timer = self.special_ability_cooldown
                self.special_ability_meter -= cost
            else:
                return


            '''if(self.special_ability_meter >= cost and self.special_ability_timer <= 2):
                if(self.special_ability_timer > 0):
                    #If we were holding down the button before
                    self.used_ability = "c&d"
                    self.special_ability_timer = cooldown #Set the cooldown between uses timer
                    self.special_ability_meter -= cost #Remove some SA meter
                    self.ability_holding_timer += 1
                elif(self.special_ability_meter > cost):
                    #If we ignite the ball
                    self.used_ability = "c&d"
                    self.special_ability_timer = cooldown #Set the cooldown between uses timer
                    self.special_ability_meter -= cost #Remove some SA meter
                    self.ability_holding_timer = 0
                else:
                    return
            '''
        elif(special_ability == "pill"):
            if(self.special_ability_meter >= cost and self.special_ability_cooldown <= 0):
                # Spend cost and activate cooldown
                if(special_ability != 'pill'):
                    cooldown = 60
                self.special_ability_cooldown = cooldown
                self.special_ability_timer = cooldown
                self.special_ability_meter -= cost
                if(self.species == 'doctor'):
                    self.used_ability["pill"] = 1

                # Activate the correct effect based on self.status_effects['pill']
                if(self.status_effects['pill'] == 'pill_heal'):
                    if(self.hp != self.max_hp):
                        self.heal_hp(heal_amt = 1)
                    sac = bool(self.special_ability_cooldown > 0)
                    skc = bool(self.kick_cooldown > 0)
                    slc = bool(self.block_cooldown > 0)
                    sbc = bool(self.boost_cooldown_timer > 0)
                    self.special_ability_cooldown -= 30 * Blob.timer_multiplier
                    self.kick_cooldown -= 30 * Blob.timer_multiplier
                    self.block_cooldown -= 30 * Blob.timer_multiplier
                    if(self.boost_cooldown_timer > 0):
                        self.boost_cooldown_timer -= 30 * Blob.timer_multiplier
                    self.check_cooldown_completion(sac, skc, slc, sbc)
                elif(self.status_effects['pill'] == 'pill_cooldown'):
                    sac = bool(self.special_ability_cooldown > 0)
                    skc = bool(self.kick_cooldown > 0)
                    slc = bool(self.block_cooldown > 0)
                    sbc = bool(self.boost_cooldown_timer > 0)
                    #self.special_ability_cooldown -= 90 * Blob.timer_multiplier
                    self.kick_cooldown -= 90 * Blob.timer_multiplier
                    self.block_cooldown -= 90 * Blob.timer_multiplier
                    if(self.boost_cooldown_timer > 0):
                        self.boost_cooldown_timer -= 90 * Blob.timer_multiplier
                    self.check_cooldown_completion(sac, skc, slc, sbc)

                else:
                    self.status_effects['steroided'] += 180
                    self.boost(boost_cost = 0, boost_duration=180, boost_cooldown=0, ignore_cooldown=True)

                if(self.species == 'doctor'):
                    pill_list = ['pill_boost', 'pill_cooldown', 'pill_heal']
                    pill_weights = [0 if x <= 0 else x for x in self.status_effects['pill_weights'].values()]
                    #print("PRE", self.status_effects['pill_weights'])
                    current_pill = random.choices(pill_list, weights = pill_weights)[0]
                    self.status_effects['pill'] = current_pill
                    #print("CHOSEN", current_pill)

                    if(self.hp <= self.max_hp//2):
                        self.status_effects['pill_weights']['pill_heal'] += 2 # Prioritize healing
                        self.status_effects['pill_weights'][current_pill] -= 2
                    else:
                        for pill in self.status_effects['pill_weights']:
                            self.status_effects['pill_weights'][pill] += 1 # Add 1 to each
                        self.status_effects['pill_weights'][current_pill] -= 3 # Effectively subtracting 2
                else:
                    if(self.hp <= self.max_hp//2):
                        self.status_effects['pill'] = 'pill_heal'
                    else:
                        if(self.status_effects['pill'] == 'pill_cooldown'):
                            self.status_effects['pill'] = 'pill_boost'
                        elif(self.status_effects['pill'] == 'pill_boost'):
                            self.status_effects['pill'] = 'pill_heal'
                        else:
                            self.status_effects['pill'] = 'pill_cooldown'
                #print("~~~~~~~~~~~~~~~~~~~~~~~~~~")

                if(self.species == 'doctor'):
                    self.update_ability_icon(cwd + "/resources/images/ability_icons/{}.png".format(self.status_effects['pill']))
                createSFXEvent('crunch')
            else:
                return
        elif(special_ability == "tax"):
            if(self.special_ability_meter >= cost and self.special_ability_cooldown <= 0):
                self.used_ability["tax"] = 2
                self.special_ability_cooldown = cooldown
                self.special_ability_timer = self.special_ability_cooldown
                self.special_ability_meter -= cost

                skc = bool(self.kick_cooldown > 0)
                slc = bool(self.block_cooldown > 0)
                sbc = bool(self.boost_cooldown_timer > 0)
                self.kick_cooldown -= 30 * Blob.timer_multiplier
                self.block_cooldown -= 30 * Blob.timer_multiplier
                if(self.boost_cooldown_timer > 0):
                    self.boost_cooldown_timer -= 30 * Blob.timer_multiplier
                self.check_cooldown_completion(updatedKick=skc, updatedBlock=slc, updatedBoost=sbc)

                createSFXEvent('chime_progress')
            else:
                return
        elif(special_ability == "stoplight"):
            if(self.special_ability_meter >= cost and self.special_ability_cooldown <= 0):
                self.used_ability["stoplight"] = 1
                self.special_ability_cooldown = cooldown
                self.special_ability_timer = self.special_ability_cooldown
                self.special_ability_meter -= cost
                #self.block_cooldown += 60
                createSFXEvent('whistle')
            else:
                return
        elif(special_ability == "starpunch"):
            if(self.special_ability_meter >= cost and self.special_ability_cooldown <= 0):
                #self.used_ability = "starpunch_wait"
                if(self.special_ability != 'starpunch'):
                    special_ability_delay = 25
                else:
                    special_ability_delay = self.special_ability_delay
                self.special_ability_cooldown = cooldown
                self.special_ability_timer = self.special_ability_cooldown
                self.special_ability_meter -= cost
                #self.kick_cooldown += 120
                create_environmental_modifier(player = self.player, affects = {'enemy'}, species = 'starpunch_wait', lifetime = special_ability_delay, y_pos = self.y_center)
                createSFXEvent('boxing_bell')
            else:
                return
        elif(special_ability == "mirror"):
            if(self.special_ability_meter >= cost and self.special_ability_cooldown <= 0):
                self.used_ability["mirror"] = 2
                if(self.special_ability != "mirror"):
                    duration = 60
                else:
                    duration = self.special_ability_duration
                self.status_effects['reflecting'] = duration
                self.special_ability_cooldown = cooldown
                self.special_ability_timer = self.special_ability_cooldown
                self.special_ability_meter -= cost
                self.kick_cooldown += 60 * Blob.timer_multiplier
                self.block_cooldown += 60 * Blob.timer_multiplier
                self.boost_cooldown_timer += 60 * Blob.timer_multiplier
                createSFXEvent('chime_progress')
            else:
                return
        elif(special_ability == "hook"):
            if('hook' in self.used_ability and self.special_ability_meter > maintenance):
                #If we were holding down the button before
                self.used_ability["hook"] = 1
                self.special_ability_timer = self.special_ability_cooldown_max #Set the cooldown between uses timer
                self.special_ability_meter -= maintenance #Remove some SA meter
                self.ability_holding_timer += 1
                #self.status_effects['overheat'] += 5
                #print(self.status_effects['overheat'])
            elif(self.special_ability_meter > cost):
                #If we ignite the ball
                self.used_ability["hook"] = 1
                self.special_ability_timer = self.special_ability_cooldown_max #Set the cooldown between uses timer
                self.special_ability_meter -= cost #Remove some SA meter
                self.ability_holding_timer = 0
                self.status_effects['overheat'] += 5
                #createSFXEvent('water')
            else:
                return
        elif(special_ability == "gluegun"):
            if('gluegun' in self.used_ability and self.special_ability_meter > maintenance):
                #If we were holding down the button before
                self.used_ability["gluegun"] += 1
                self.special_ability_timer = self.special_ability_cooldown_max #Set the cooldown between uses timer
                self.special_ability_meter -= maintenance #Remove some SA meter
                self.ability_holding_timer += 1
            elif(self.special_ability_meter > cost):
                #If we ignite the ball
                self.used_ability["gluegun"] = 1
                self.special_ability_timer = self.special_ability_cooldown_max #Set the cooldown between uses timer
                self.special_ability_meter -= cost #Remove some SA meter
                self.ability_holding_timer = 0
            else:
                return
            if(self.facing == 'left'):
                x_mod = -1
            else:
                x_mod = 1
            if(not (self.ability_holding_timer % 4)):
                create_environmental_modifier(self.player, affects = {'enemy', 'self', 'ball'}, species = 'glue_shot', x_pos = self.x_center, y_pos = self.y_center - 10, x_speed = (3*self.x_speed/4) + (6*x_mod), y_speed = (self.y_speed/2) - 7, gravity = 0.25, lifetime = 600)
                #createSFXEvent('water')
        elif(special_ability == "teleport"):
            if(self.special_ability_meter >= cost and self.special_ability_cooldown <= 0):
                self.special_ability_cooldown = cooldown
                self.special_ability_timer = self.special_ability_cooldown
                self.special_ability_meter -= cost
                if(self.facing == 'left'):
                    x_mod = -1
                else:
                    x_mod = 1
                #if(self.status_effects['teleporter'] == 'console'):
                '''self.status_effects['teleporter'] = 'cartridge'
                create_environmental_modifier(self.player, affects = {'self'}, species = 'console', lifetime = 900, hp = 3, x_pos = self.x_center, y_pos = self.y_center - 10, x_speed = (1*self.x_speed/4) + (2*x_mod), y_speed = (self.y_speed/2) - 9, gravity = 0.25)
                ''''''else:'''
                create_environmental_modifier(self.player, affects = {'self'}, species = 'cartridge', lifetime = 600, hp = 1, x_pos = self.x_center, y_pos = self.y_center - 10, x_speed = (3*self.x_speed/4) + (4*x_mod), y_speed = (self.y_speed/2) - 12, gravity = 0.4, random_image = self.status_effects['teleporter'][0])
                self.status_effects['teleporter'][0] += 1
                if(self.status_effects['teleporter'][0]) > 3:
                    self.status_effects['teleporter'][0] = 1
            else:
                return
        elif(special_ability == "cardpack"):
            if(self.special_ability_meter >= cost and self.special_ability_cooldown <= 0):
                #self.special_ability_cooldown = 30 * Blob.timer_multiplier
                self.special_ability_timer = self.special_ability_cooldown
                self.special_ability_meter -= cost
                self.status_effects['menu']['open'] = True
                self.status_effects['menu']['type'] = 'cardpack'
                self.status_effects['menu']['time'] = 0

                #print("RECHARGE", self.status_effects['cards']['recharge'])

                self.status_effects['cards']['pulled'] = random.sample(self.status_effects['cards']['pool'], 3)
                for card in self.status_effects['cards']['pulled']:
                    self.status_effects['cards']['pool'].remove(card)
                for card in self.status_effects['cards']['recharge']:
                    self.status_effects['cards']['pool'].add(card)
                self.status_effects['cards']['recharge'] = set()

                #print("POOL", self.status_effects['cards']['pool'])
                #print("PULLED", self.status_effects['cards']['pulled'])
                #print("POST RECHARGE", self.status_effects['cards']['recharge'])
            else:
                return
        elif(special_ability == "monado"):
            if(self.special_ability_meter >= cost and self.special_ability_cooldown <= 0):
                #self.special_ability_cooldown = 30 * Blob.timer_multiplier
                self.status_effects['menu']['open'] = True
                self.status_effects['menu']['type'] = 'monado'
                self.status_effects['menu']['time'] = 0
        elif(special_ability == "spike"):
            if(self.special_ability_meter >= cost and self.special_ability_cooldown <= 0):
                #Spire activation
                createSFXEvent('glyph')
                #self.used_ability = "spire_wait"
                self.special_ability_cooldown = cooldown
                self.special_ability_timer = cooldown #Set the cooldown between uses timer
                self.special_ability_meter -= cost #Remove some SA meter
                create_environmental_modifier(player = self.player, x_pos = self.x_center, y_pos = self.y_center, affects = {'enemy', 'ball'}, species = 'cactus_spike', lifetime = 60)
            else:
                return
        elif(special_ability == "shop"):
            if(self.special_ability_meter >= cost and self.special_ability_cooldown <= 0):
                #self.special_ability_cooldown = 30 * Blob.timer_multiplier
                self.status_effects['menu']['open'] = True
                self.status_effects['menu']['type'] = 'shop'
                self.status_effects['menu']['time'] = 0
        elif(special_ability == "bubble"):
            if(self.special_ability_meter >= cost and self.special_ability_cooldown <= 0):
                #Spire activation
                createSFXEvent('glyph')
                #self.used_ability = "spire_wait"
                self.special_ability_cooldown = cooldown
                self.special_ability_timer = cooldown #Set the cooldown between uses timer
                self.special_ability_meter -= cost #Remove some SA meter
                create_environmental_modifier(player = self.player, x_pos = self.x_center - 75, y_pos = self.y_center - 200, y_speed=-0.1, gravity=0, affects = {'ball'}, species = 'bubble', lifetime = 600)
        
        if(card == "" and self.status_effects['cards']['ability']):
            #print(card, self.status_effects['cards']['ability'])
            self.status_effects['cards']['equipped'].remove(self.status_effects['cards']['ability'])
            self.status_effects['cards']['recharge'].add(self.status_effects['cards']['ability'])
            self.status_effects['cards']['ability'] = None
            self.recharge_indicators['ability_swap'] = True
            self.special_ability_cooldown = 180 * Blob.timer_multiplier
            if(self.kick_cooldown < 10 * Blob.timer_multiplier):
                self.kick_cooldown = 10 * Blob.timer_multiplier
            if(self.block_cooldown < 10 * Blob.timer_multiplier):
                self.block_cooldown = 10 * Blob.timer_multiplier
            if(self.boost_cooldown_timer < 10 * Blob.timer_multiplier):
                self.boost_cooldown_timer = 10 * Blob.timer_multiplier
                



    def kick(self, ignore_cooldown = False):
        if((self.kick_cooldown <= 0 or ignore_cooldown) and not self.status_effects['cards']['kick']):
            createSFXEvent('kick')
            self.block_cooldown += 5 * (self.block_cooldown_rate)
            self.kick_timer = 2
            self.kick_cooldown = self.kick_cooldown_max
            #self.collision_timer = 0
            self.collision_distance = 175
            self.kick_visualization = self.kick_visualization_max
            self.info['kick_count'] += 1
            if(self.status_effects['shop']['offense_equip']):
                self.status_effects['shop']['offense_durability'] -= 1
            if(self.status_effects['shop']['offense_equip'] == 'nailmasters_glory'):
                self.kick_cooldown /= 2
            
        elif((self.kick_cooldown <= 0 or ignore_cooldown) and self.status_effects['cards']['kick']):
            self.ability(card = self.status_effects['cards']['kick'])
            
            self.kick_cooldown = self.kick_cooldown_max//2
            if(self.special_ability_cooldown < 10 * Blob.timer_multiplier):
                self.special_ability_cooldown = 10 * Blob.timer_multiplier
            if(self.block_cooldown < 10 * Blob.timer_multiplier):
                self.block_cooldown = 10 * Blob.timer_multiplier
            if(self.boost_cooldown_timer < 10 * Blob.timer_multiplier):
                self.boost_cooldown_timer = 10 * Blob.timer_multiplier
            #print(self.status_effects['cards']['kick'])
            self.status_effects['cards']['equipped'].remove(self.status_effects['cards']['kick'])
            self.status_effects['cards']['recharge'].add(self.status_effects['cards']['kick'])
            self.status_effects['cards']['kick'] = None
            self.recharge_indicators['ability_swap'] = True

    def block(self):
        if(self.block_cooldown <= 0 and not self.status_effects['cards']['block']):
            createSFXEvent('block')
            self.kick_cooldown += 5 * (self.kick_cooldown_rate)
            self.block_cooldown = self.block_cooldown_max #Set block cooldown
            self.block_timer = self.block_timer_max #Set active block timer
            self.movement_lock = 30
            self.x_speed = 0
            if(self.y_speed < 0): #If we are moving upwards, halt your momentum!
                self.y_speed = 0
            if(self.status_effects['shop']['defense_equip'] == 'thorns_of_agony' and self.status_effects['shop']['defense_durability'] > 0):
                self.status_effects['reflecting'] = 180
            if(self.status_effects['shop']['defense_equip'] == 'izumi_tear' and self.status_effects['shop']['defense_durability'] > 0):
                self.block_cooldown /= 2
            if(self.status_effects['shop']['defense_equip'] in {'thorns_of_agony', 'izumi_tear'} and self.status_effects['shop']['defense_durability'] > 0):
                self.status_effects['shop']['defense_durability'] -= 1
            self.info['block_count'] += 1
        elif(self.block_cooldown <= 0 and self.status_effects['cards']['block']):
            self.ability(card = self.status_effects['cards']['block'])
            self.block_cooldown = self.block_cooldown_max//2 #Set block cooldown
            if(self.special_ability_cooldown < 10 * Blob.timer_multiplier):
                self.special_ability_cooldown = 10 * Blob.timer_multiplier
            if(self.kick_cooldown < 10 * Blob.timer_multiplier):
                self.kick_cooldown = 10 * Blob.timer_multiplier
            if(self.boost_cooldown_timer < 10 * Blob.timer_multiplier):
                self.boost_cooldown_timer = 10 * Blob.timer_multiplier
            #print(self.status_effects['cards']['block'])
            self.status_effects['cards']['equipped'].remove(self.status_effects['cards']['block'])
            self.status_effects['cards']['recharge'].add(self.status_effects['cards']['block'])
            self.status_effects['cards']['block'] = None
            self.recharge_indicators['ability_swap'] = True

    def boost(self, boost_cost = None, boost_duration = None, boost_cooldown = None, ignore_cooldown = None):
        if(boost_cost is None):
            boost_cost = self.boost_cost

        if(self.special_ability_meter >= boost_cost and (self.boost_cooldown_timer <= 0 or ignore_cooldown is not None) and not self.status_effects['cards']['boost']):
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
        elif(self.boost_cooldown_timer <= 0 and self.status_effects['cards']['boost']):
            self.ability(card = self.status_effects['cards']['boost'])
            if(self.special_ability_cooldown < 10 * Blob.timer_multiplier):
                self.special_ability_cooldown = 10 * Blob.timer_multiplier
            if(self.kick_cooldown < 10 * Blob.timer_multiplier):
                self.kicck_cooldown = 10 * Blob.timer_multiplier
            if(self.block_cooldown < 10 * Blob.timer_multiplier):
                self.boost_cooldown = 10 * Blob.timer_multiplier
            self.boost_cooldown_timer = self.boost_cooldown_max//2
            #print(self.status_effects['cards']['boost'])
            self.status_effects['cards']['equipped'].remove(self.status_effects['cards']['boost'])
            self.status_effects['cards']['recharge'].add(self.status_effects['cards']['boost'])
            self.status_effects['cards']['boost'] = None
            self.recharge_indicators['ability_swap'] = True
    
    def check_blob_collision(self, blob):
        #Used to see if a blob is getting kicked!
        status_effects = []
        if(self.x_center - (1.5 * self.collision_distance) <= blob.x_center <= self.x_center + (1.5 * self.collision_distance)):
            if(self.y_center - (1.1 * self.collision_distance) <= blob.y_center <= self.y_center + (self.collision_distance)):
                accumulated_damage = 2
                pierce = 0
                x_speed_mod = 0
                if(self.boost_timer > 0):  # Take additional damage if the enemy is boosting
                    accumulated_damage += 1
                    if(self.species == "ice"):
                        status_effects.append(['hypothermia', 180])
                    elif(self.species == "arcade" and not blob.block_timer and not blob.kick_timer):
                        create_environmental_modifier(blob.player, affects = {'self'}, species = 'console', lifetime = 480, hp = 1, x_pos = self.x_center, y_pos = self.y_center - 20, gravity = 0.5)
                    elif(self.species == "fire"):
                        status_effects.append(['overheat', 300])
                    elif(self.species == "boxer"):
                        self.special_ability_cooldown -= 120 * Blob.timer_multiplier
                        if(self.special_ability_cooldown < 0):
                            self.special_ability_cooldown = 0
                    elif(self.species == "judge"):
                        if(blob.status_effects['judged']):
                            status_effects.append(['stunned', 45])
                        else:
                            status_effects.append(['stunned', 15])
                    elif(self.species == "king" and not blob.block_timer and not blob.kick_timer):
                        create_environmental_modifier(blob.player, affects = {'self'}, species = 'royal_loan', lifetime = 360, hp = 0, x_pos = self.x_center - 20, y_pos = self.y_center - 150, gravity = 0, random_image=self.player)
                    elif(self.species == "glue"):
                        self.boost_timer += 60 * Blob.timer_multiplier
                    elif(self.species == "cactus" and not blob.block_timer and not blob.kick_timer):
                        self.special_ability_meter += 360 * Blob.nrg_multiplier if blob.special_ability_meter > 360 * Blob.nrg_multiplier else blob.special_ability_meter
                        blob.special_ability_meter -= 360 * Blob.nrg_multiplier if blob.special_ability_meter > 360 * Blob.nrg_multiplier else blob.special_ability_meter
                        if(self.special_ability_meter > self.special_ability_max):
                            self.special_ability_meter = self.special_ability_max
                    elif(self.species == "wind"):
                        if(self.x_pos < blob.x_pos):
                            x_speed_mod = 40
                        elif(self.x_pos > blob.x_pos):
                            x_speed_mod = -40
                        elif(self.x_pos < 902):
                            x_speed_mod = 40
                        else:
                            x_speed_mod = -40
                    #elif(self.species == "doctor"):
                    #    accumulated_damage += 1
                if(((blob.player == 2 and blob.x_pos >= blob.danger_zone) or (blob.player == 1 and blob.x_pos <= blob.danger_zone)) and blob.danger_zone_enabled):
                    #Take additional damage from kicks if you are hiding by your goal
                    accumulated_damage += 1
                if(self.status_effects['steroided']):
                    pierce += 1
                if(self.status_effects['monado_effect'] == "SMASH"):
                    pierce += 1
                    accumulated_damage += 1
                if(self.status_effects['monado_effect'] == "JUMP" or self.status_effects['monado_effect'] == "SPEED"):
                    accumulated_damage += 1
                if(self.status_effects['shop']['offense_equip'] == 'heavy_blow'):
                    accumulated_damage += 1
                    if(self.x_pos < blob.x_pos):
                        x_speed_mod = 30
                    else:
                        x_speed_mod = -30

                dealt_damage = blob.take_damage(accumulated_damage,  status_effects = status_effects, pierce = pierce, x_speed_mod = x_speed_mod)
                if(self.status_effects['shop']['offense_equip'] == 'dream_wielder'):
                    self.special_ability_meter += dealt_damage * 300 * Blob.nrg_multiplier
                    if(self.special_ability_meter > self.special_ability_max):
                            self.special_ability_meter = self.special_ability_max

                if(blob.status_effects['reflecting'] > 1):
                    self.take_damage(damage = 1, unblockable=True, unclankable=True)
                    blob.status_effects['reflect_break'] = 68
                    blob.status_effects['silenced'] += 360
        if(self.status_effects['shop']['offense_durability'] == 0 and self.status_effects['shop']['offense_equip']):
                createSFXEvent('crunch')
                self.status_effects['shop']['discard_particle'] = self.status_effects['shop']['offense_equip']
                self.status_effects['shop']['offense_equip'] = None
                #print("114X Offense Discard")


                    
    def check_ability_collision(self, blob):
        if(("gale" in self.used_ability) or \
            ("gale" in blob.used_ability)):
            if blob.y_pos != blob.ground and not blob.block_timer: #Gale Affecting the opponent
                if(self.player == 1 and "gale" in self.used_ability): #Airborne
                    blob.x_pos += 7
                elif(self.player == 2 and "gale" in self.used_ability):
                    blob.x_pos -= 7
        elif("c&d" in self.used_ability):
            blob.status_effects['judged'] = self.special_ability_duration
            if(self.species != "judge"):
                blob.status_effects['judged'] = 90
        elif("tax" in self.used_ability):
            self.status_effects['taxing'] = self.special_ability_duration
            blob.status_effects['taxed'] = self.special_ability_duration
            if(self.species != "king"):
                self.status_effects['taxing'] = 240
                blob.status_effects['taxed'] = 240
            self.set_base_stats(blob.return_stars())
            blob.set_base_stats(self.return_stars())
            '''if(blob.kick_cooldown < self.kick_cooldown):
                self.kick_cooldown = (self.kick_cooldown + blob.kick_cooldown)//2
            
            if(blob.block_cooldown < self.block_cooldown):
                self.block_cooldown = (self.block_cooldown + blob.block_cooldown)//2

            if(blob.boost_cooldown_timer < self.boost_cooldown_timer):
                self.boost_cooldown_timer = (self.boost_cooldown_timer + blob.boost_cooldown_timer)//2'''
        elif("stoplight" in self.used_ability):
            blob.status_effects['stoplit'] = 30

    def check_environmental_collisions(self, environment):
        for hazard in environment['glue_puddle']:
            #print(hazard.player, hazard.affects)
            if(hazard.player != self.player and "enemy" in hazard.affects):
                if(hazard.x_pos - 160 < self.x_pos < hazard.x_pos + 90 and self.y_pos == Blob.ground):
                    self.status_effects['glued'] = 2
                    break
            elif(hazard.player == self.player and "self" in hazard.affects):
                if(hazard.x_pos - 160 < self.x_pos < hazard.x_pos + 90 and self.y_pos == Blob.ground):
                    self.status_effects['buttered'] = 2
                    break

        for hazard in environment['spire_spike']:
            if(hazard.player != self.player and hazard.lifetime == hazard.max_lifetime - 1 and 'enemy' in hazard.affects and hazard.x_pos - 80 <= self.x_center <= hazard.x_pos + 215 and self.y_pos > 800):
                if(self.block_timer == 0):
                    self.take_damage(y_speed_mod = -40 - (5 * (self.gravity_mod - 1.05)), stun_amount = 20)
                    # TODO: Reflection
                    if(self.status_effects['reflecting'] > 1):
                        self.all_blobs[hazard.player].take_damage(damage = 1, unblockable=True, unclankable=True)
                        self.status_effects['reflect_break'] = 68
                        self.special_ability_cooldown += 180 * Blob.timer_multiplier
                else:
                    self.take_damage(damage=0)
                    self.block_cooldown += 30 * Blob.timer_multiplier
        
        for hazard in environment['thunder_bolt']:
            if(hazard.player == self.player and hazard.lifetime == hazard.max_lifetime - 1 and 'self' in hazard.affects and hazard.x_pos - 110 <= self.x_center <= hazard.x_pos + 240):
                self.boost(boost_cost = 0, boost_duration=120, boost_cooldown=0, ignore_cooldown=True)
            
            if(hazard.player != self.player and hazard.lifetime == hazard.max_lifetime - 1 and 'enemy' in hazard.affects and hazard.x_pos - 80 <= self.x_center <= hazard.x_pos + 215):
                self.take_damage()
                if(self.status_effects['reflecting'] > 1):
                    self.all_blobs[hazard.player].take_damage(damage = 1, unblockable=True, unclankable=True)
                    self.status_effects['reflect_break'] = 68
                    self.special_ability_cooldown += 180 * Blob.timer_multiplier
                '''if(self.status_effects['reflecting'] > 1):
                    self.take_damage(damage = 1, unblockable=True, unclankable=True)
                    self.status_effects['reflect_break'] = 68
                    self.special_ability_cooldown += 180'''

        # TODO: Line up Starpunch so it targets the player
        for hazard in environment['starpunch_wait']:
            if(hazard.player == self.player):
                hazard.x_pos = self.x_center - 20
                hazard.y_pos = self.y_center - 20

        for hazard in environment['starpunch']:
            if(hazard.player != self.player and hazard.lifetime == hazard.max_lifetime - 1 and 'enemy' in hazard.affects):
                punch_x = self.x_center - 20
                punch_y = self.y_center - 20
                # Rightwards Range
                if(self.x_center > hazard.x_pos + 265):
                    punch_x = hazard.x_pos + 265
                # Leftwards Range
                elif(hazard.x_pos - 285 > self.x_center):
                    punch_x = hazard.x_pos - 285
                # Downwards Range
                if(hazard.y_pos + 180 < self.y_center):
                    punch_y = hazard.y_pos + 180
                # Upwards Range
                elif(hazard.y_pos - 295 > self.y_center):
                    punch_y = hazard.y_pos - 295

                # TODO: Spawn Spring Particles

                x_midpoint = (punch_x + hazard.x_pos)/2
                y_midpoint = (punch_y + hazard.y_pos)/2

                create_environmental_modifier(hazard.player, species = 'starpunch_spring', x_pos = hazard.x_pos, y_pos = hazard.y_pos, lifetime=30)
                create_environmental_modifier(hazard.player, species = 'starpunch_spring', x_pos = (hazard.x_pos + x_midpoint)/2, y_pos = (hazard.y_pos + y_midpoint)/2, lifetime=30)
                create_environmental_modifier(hazard.player, species = 'starpunch_spring', x_pos = x_midpoint, y_pos = y_midpoint,lifetime=30)
                create_environmental_modifier(hazard.player, species = 'starpunch_spring', x_pos = (punch_x + x_midpoint)/2, y_pos = (punch_y + y_midpoint)/2, lifetime=30)

                hazard.x_pos, hazard.y_pos = punch_x, punch_y

                if(self.x_center - 130 <= hazard.x_pos <= self.x_center + 75 and self.y_center - 125 <= hazard.y_pos <= self.y_center + 50):
                    accumulated_damage = 3
                    stun_amount = 30

                    # TODO: Handle Danger Zone bonus
                    
                    if(self.all_blobs[hazard.player].boost_timer):
                        accumulated_damage += 1
                    
                    if(((self.player == 2 and self.x_pos >= self.danger_zone) or (self.player == 1 and self.x_pos <= self.danger_zone)) and self.danger_zone_enabled):
                        #Take additional damage from kicks if you are hiding by your goal
                        accumulated_damage += 1
                    
                    if(self.block_timer):
                        accumulated_damage -= 2
                        stun_amount = 0
                    self.all_blobs[hazard.player].kick_cooldown -= 180 * Blob.timer_multiplier
                    self.take_damage(damage = accumulated_damage, unblockable=True, unclankable=True, stun_amount = stun_amount,)
                    if(self.status_effects['reflecting'] > 1):
                        self.all_blobs[hazard.player].take_damage(damage = 1, unblockable=True, unclankable=True)
                        self.status_effects['reflect_break'] = 68
                        self.special_ability_cooldown += 180 * Blob.timer_multiplier
                else:
                    self.all_blobs[hazard.player].status_effects['overheat'] += 120

        teleported = False
        for hazard in environment['console']:
            if(hazard.player == self.player and hazard.lifetime == 1) or (hazard.player == self.player and not self.down_holding_timer % 40 and self.down_holding_timer and hazard.lifetime <= hazard.max_lifetime - 300 and not teleported):
                draw_teleportation_pfx([self.x_pos, self.y_pos])
                self.x_pos = hazard.x_pos
                self.y_pos = hazard.y_pos  
                hazard.lifetime = 0
                self.focusing = False
                if(self.y_pos > Blob.ground):
                    self.y_pos = Blob.ground
                teleported = True
                createSFXEvent('teleport')
                draw_teleportation_pfx([self.x_pos, self.y_pos])
                #print("teleported to", hazard.x_pos, hazard.y_pos, hazard.species)

        for hazard in environment['cartridge']:
            if(hazard.player == self.player and hazard.lifetime == 1) or (hazard.player == self.player and not self.down_holding_timer % 15 and self.down_holding_timer and not teleported):
                draw_teleportation_pfx([self.x_pos, self.y_pos])
                self.x_pos = hazard.x_pos
                self.y_pos = hazard.y_pos 
                hazard.lifetime = 0
                self.focusing = False
                if(self.y_pos > Blob.ground):
                    self.y_pos = Blob.ground
                teleported = True
                createSFXEvent('teleport')
                draw_teleportation_pfx([self.x_pos, self.y_pos])
                #print("teleported to", hazard.x_pos, hazard.y_pos, hazard.species)
        
        for hazard in environment['royal_loan']:
            if(hazard.player == self.player and hazard.lifetime == 1):
                self.status_effects['overheat'] += (hazard.hp * 180) + 90
                print("Punished for", self.status_effects['overheat'], "frames!")
                print("Accumulated", hazard.hp, "worth of debt!")
            elif(hazard.random_image == self.player and hazard.lifetime == 1):
                self.status_effects['hyped'] += (hazard.hp * 60) + 30
                print("Hyped for", self.status_effects['hyped'], "frames!")
                
            elif(hazard.player == self.player):
                self.status_effects['loaned'] += 1
                hazard.x_pos, hazard.y_pos = self.x_center - 20, self.y_center - 150
                if(self.kick_timer == 2):
                    hazard.hp += 1
                if(self.block_timer == 15):
                    hazard.hp += 1
                if(self.boost_timer == self.boost_duration):
                    hazard.hp += 1
                if(self.special_ability_cooldown == self.special_ability_cooldown_max):
                    hazard.hp += 1
        
        for hazard in environment['cactus_spike']:
            if(hazard.player != self.player and 'enemy' in hazard.affects and self.player not in hazard.affects):
                if(self.x_center - 130 <= hazard.x_pos <= self.x_center + 75 and self.y_center - 125 <= hazard.y_pos <= self.y_center + 50):
                    stun_amount = 30
                    if(self.block_timer):
                        stun_amount = 0
                    self.all_blobs[hazard.player].kick_cooldown -= 180 * Blob.timer_multiplier
                    self.take_damage(damage = 1, stun_amount = stun_amount, status_effects = [['nrg_fatigue', 300]])
                    hazard.affects.add(self.player)
                    if(self.status_effects['reflecting'] > 1):
                        self.all_blobs[hazard.player].take_damage(damage = 1, unblockable=True, unclankable=True)
                        self.status_effects['reflect_break'] = 68
                        self.special_ability_cooldown += 180 * Blob.timer_multiplier
        
        for hazard in environment['sharp_shadow']:
            if(hazard.player == self.player):
                hazard.x_pos = self.x_center - 20
                hazard.y_pos = self.y_center - 20
            
            if(hazard.player != self.player and self.player not in hazard.affects and self.x_center - 130 <= hazard.x_pos <= self.x_center + 75 and self.y_center - 125 <= hazard.y_pos <= self.y_center + 50):
                accumulated_damage = 3
                stun_amount = 120
                self.take_damage(damage=accumulated_damage, stun_amount=stun_amount if self.all_blobs[hazard.player].species == "merchant" else 0)
                hazard.affects.add(self.player)
                

    def take_damage(self, damage = 1, unblockable = False, unclankable = False, damage_flash_timer = 60, y_speed_mod = 0, x_speed_mod = 0,\
    stun_amount = 0, show_parry = True, status_effects = [], pierce = 0):
        damage_taken = False
        pierced = False
        if(self.status_effects['monado_effect'] == "SMASH"):
            pierce += 1
        def check_block():  # Returns true if the hit goes through
            if(self.block_timer):  # Blocking?
                if(show_parry):
                    if(self.block_timer >= self.block_timer_max - 3):
                        self.special_ability_meter += 300
                        if(self.special_ability_meter > self.special_ability_max):
                            self.special_ability_meter = self.special_ability_max
                        createSFXEvent('perfect_parry', volume_modifier=0.4)
                        self.perfect_parried = 2
                    else:
                        createSFXEvent('parry')
                        self.parried = 2
                    self.info['parries'] += 1
                    
                return False # We failed the block check, don't take damage
            else:
                
                return True # Return true if the block check passes, we can take damage (amd boogy woogy[quacknote])!

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
        
        if(not damage_taken and pierce):
            damage = pierce - bool(self.status_effects['monado_effect'] == "SMASH") - bool(self.status_effects['monado_effect'] == "SHIELD")
            damage_taken = True
            pierced = True

        if(damage_taken):
            # Increase damage by 1 if using hook
            # Decrease damage by 1 if using reflect
            # Increase damage by 1 if using SPEED
            # Increase damage by 2 if using SMASH
            # Decrease damage by 1 if using SHIELD
            # self.hp -= damage + bool(self.used_ability == "hook") - bool(self.status_effects['reflecting'] > 0)
            initial_hp = self.hp
            self.hp -= damage - bool(self.status_effects['reflecting'] > 0) + bool(self.status_effects['monado_effect'] == "SPEED") + (2 * bool(self.status_effects['monado_effect'] == "SMASH")) - bool(self.status_effects['monado_effect'] == "SHIELD") - bool(self.focusing and self.status_effects['shop']['focus_equip'] == 'baldur_shell')
            
            if(self.status_effects['shop']['focus_equip'] == 'baldur_shell' and self.focusing):
                self.status_effects['shop']['focus_durability'] -= 1
                self.focus_lock = 0
            self.damage_flash_timer = damage_flash_timer
            self.info['damage_taken'] += damage
            self.status_effects['stunned'] = stun_amount
            self.y_speed = y_speed_mod
            self.x_speed = x_speed_mod
            createSFXEvent('hit')
            if(not self.recharge_indicators['damage_flash']):  # If we're hit twice on the same frame, don't disable the flash!
                self.toggle_recharge_indicator('damage_flash')
            if(self.special_ability == "hook" and self.special_ability_timer and self.status_effects['silenced'] < 360):
                print(self.status_effects['silenced'], "BLOB")
                self.status_effects['silenced'] += 360

            for status_effect in status_effects:
                self.status_effects[status_effect[0]] += status_effect[1]
            self.special_ability_meter += 300 * Blob.nrg_multiplier * (initial_hp - self.hp) if self.status_effects['shop']['passive_equip'] == 'grub_song' else 0
            if(self.special_ability_meter > self.special_ability_max):
                self.special_ability_meter = self.special_ability_max
            return initial_hp - self.hp
        return 0

    def heal_hp(self, heal_amt = 1, overheal = False):
        if(heal_amt > 0):
            if overheal:
                self.hp += heal_amt
                self.toggle_recharge_indicator('heal_flash')
            else:
                self.hp += heal_amt
                if(self.hp >= self.max_hp):
                    self.hp = self.max_hp
                else:
                    self.toggle_recharge_indicator('heal_flash')

    def blob_ko(self):
        self.y_speed = 10
        if(self.y_pos < 2000):
            self.y_pos += self.y_speed

    def reset(self, ruleset):
        self.x_speed = 0
        self.y_speed = 0
        if(self.player == 1):
            self.x_pos = 100
            self.facing = 'right'
        else:
            self.x_pos = 1600
            self.facing = 'left'
        self.move([])
        self.y_pos = Blob.ground
        if(self.species == "quirkless" and self.boost_timer):
            self.special_ability_cooldown -= self.boost_timer
        self.boost_timer = 0
        self.focus_lock = 0
        self.kick_visualization = 0
        self.block_timer = 0
        self.focusing = False
        self.damage_flash_timer = 0
        self.image = species_to_image(self.species, self.costume)[0]
        self.special_ability_timer = 0
        self.used_ability = {}
        self.top_speed = self.base_top_speed
        self.friction = self.base_friction
        self.traction = self.base_traction
        self.impact_land_frames = 0
        self.movement_lock = 0
        self.wavedash_lock = 0
        self.ability_holding_timer = 0
        self.status_effects['hypothermia'] = 0
        self.status_effects['judged'] = 0
        self.status_effects['steroided'] = 0
        self.status_effects['taxed'] = 0
        self.status_effects['taxing'] = 0
        self.status_effects['loaned'] = 0
        self.status_effects['stunned'] = 0
        self.status_effects['reflecting'] = 0
        self.status_effects['reflect_break'] = 0
        #self.status_effects['overheat'] = 0
        self.set_base_stats(self.stars)
        #self.heal_hp(heal_amt=ruleset['hp_regen'])
        
    def move(self, pressed_buttons):
        pressed_conversions = player_to_controls(self.player)

        pressed = []
        for button in pressed_buttons:
            if(button in pressed_conversions):
                if(self.focusing and self.focus_lock):
                    if(pressed_conversions[button] == "down"):
                        pressed.append(pressed_conversions[button])
                    elif(pressed_conversions[button] == "up"):
                        pressed.append(pressed_conversions[button])
                        self.info['jump_cancelled_focuses'] += 1
                    else:
                        continue
                elif(self.focusing and not self.focus_lock):
                    if(pressed_conversions[button] == "down"):
                        pressed.append(pressed_conversions[button])
                    elif(pressed_conversions[button] == "up"):
                        pressed.append(pressed_conversions[button])
                        self.info['jump_cancelled_focuses'] += 1
                    elif(pressed_conversions[button] == "left" or pressed_conversions[button] == "right"):
                        pressed.append(pressed_conversions[button])
                        self.info['wavedashes'] += 1
                    else:
                        continue
                else:
                    pressed.append(pressed_conversions[button])
        
        if(self.movement_lock > 0 or self.status_effects['stunned']):
            pressed = []
        if(self.wavedash_lock):
            if('down' in pressed):
                pressed.remove('down')
        if(self.jump_lock):
            if('up' in pressed):
                pressed.remove('up')
        if(self.status_effects['judged']):
            if('kick' in pressed):
                pressed.remove('kick')
            if('block' in pressed):
                pressed.remove('block')
            if('boost' in pressed):
                pressed.remove('boost')
            if('ability' in pressed):
                pressed.remove('ability')
        if(self.status_effects['silenced']):
            if('ability' in pressed):
                pressed.remove('ability')

        #HORIZONTAL MOVEMENT
        blob_speed = self.top_speed
        blob_traction = self.traction
        blob_friction = self.friction
        if(self.status_effects['glued']):
            blob_speed = 5 + (3 * bool(self.boost_timer))
        if(self.status_effects['buttered']):
            blob_speed += 2
        if(self.status_effects['hypothermia']):
            blob_speed -= 3
        if(self.status_effects['monado_effect']):
            if(self.status_effects['monado_effect'] == "JUMP"):
                blob_friction += 3
            if(self.status_effects['monado_effect'] == "SPEED"):
                blob_speed += 5
                blob_traction += 1
                blob_friction += 1
            if(self.status_effects['monado_effect'] == "SHIELD"):
                blob_speed -= 3
        if(self.status_effects['shop']['passive_equip'] == "sprint_master"):
            blob_speed += 2
            blob_traction += 5
            blob_friction += 5
        wavedashed = False

        menu_open = self.status_effects['menu']['open']

        if(self.y_pos == Blob.ground): #Applies traction if grounded
            if('left' in pressed and not 'right' in pressed and not menu_open): #If holding left but not right
                if(not self.focusing):
                    self.facing = "left"
                    if(self.x_pos <= 0): #Are we in danger of going off screen?
                        self.x_speed = 0
                        self.x_pos = 0
                    else:
                        if(abs(self.x_speed) < blob_speed):
                            if(self.x_speed > 0):
                                self.x_speed -= 1.2 * blob_traction # Turn around faster by holding left
                            elif(abs(self.x_speed) > blob_speed + (blob_traction * 2)): # Ease back into top speed if we're above it
                                self.x_speed -= blob_traction
                            else:
                                self.x_speed -= blob_traction # Accelerate based off of traction
                        elif(abs(self.x_speed) > blob_speed + (blob_traction * 2)): # Ease back into top speed if we're above it
                            self.x_speed += blob_traction
                        else: # Snap back to top speed
                            prev_speed = self.x_speed
                            self.x_speed = -1*blob_speed #If at max speed, maintain it
                            if(round(prev_speed) == blob_speed):
                                self.info['wavebounces'] += 1
                                createSFXEvent('wavebounce')
                elif('down' in pressed):
                    self.wavedash_lock = 15
                    #self.collision_timer = 30
                    #self.x_speed = -1 * (15 + (10 * blob_traction))
                    self.x_speed = -30 if bool(self.status_effects['shop']['defense_equip'] == 'sharp_shadow') else -20
                    self.focusing = False
                    self.focus_lock = 0
                    wavedashed = True
                    createSFXEvent('wavedash')
            elif(not 'left' in pressed and 'right' in pressed and not menu_open): #If holding right but not left
                if(not self.focusing):
                    self.facing = 'right'
                    if(self.x_pos >= 1700): #Are we in danger of going off screen?
                        self.x_speed = 0
                        self.x_pos = 1700
                    else:
                        if(abs(self.x_speed) < blob_speed):
                            if(self.x_speed < 0):
                                self.x_speed += 1.2 * blob_traction # Turn around faster by holding left
                            elif(abs(self.x_speed) > blob_speed + (blob_traction * 2)):
                                self.x_speed += blob_traction
                            else:
                                self.x_speed += blob_traction # Accelerate based off of traction
                        elif(abs(self.x_speed) > blob_speed + (blob_traction * 2)): # Ease back into top speed if we're above it
                            self.x_speed -= blob_traction
                        else: # Snap back to top speed
                            prev_speed = self.x_speed
                            self.x_speed = blob_speed #If at max speed, maintain it
                            if(round(prev_speed) == -1 * blob_speed):
                                self.info['wavebounces'] += 1
                                createSFXEvent('wavebounce')
                elif('down' in pressed and not menu_open):
                    self.wavedash_lock = 15
                    #self.collision_timer = 30
                    #self.x_speed = 15 + (10 * blob_traction)
                    self.x_speed = 30 if bool(self.status_effects['shop']['defense_equip'] == 'sharp_shadow') else 20
                    self.focusing = False
                    wavedashed = True
                    createSFXEvent('wavedash')

            else: #We're either not holding anything, or pressing both at once
                if(self.x_speed < 0): #If we're going left, decelerate
                    if(self.x_speed + blob_traction) > 0:
                        self.x_speed = 0 #Ensures that we don't decelerate and start moving backwards
                    else:
                        self.x_speed += blob_traction #Normal deceleration
                elif(self.x_speed > 0):
                    if(self.x_speed - blob_traction) < 0:
                        self.x_speed = 0 #Ensures that we don't decelerate and start moving backwards
                    else:
                        self.x_speed -= blob_traction #Normal deceleration
        else: #Applies friction if airborne
            if('left' in pressed and not 'right' in pressed and not menu_open): #If holding left but not right
                self.facing = "left"
                if(self.x_pos <= 0): #Are we in danger of going off screen?
                    self.x_speed = 0
                    self.x_pos = 0
                else:
                    if(abs(self.x_speed) < blob_speed):
                        if(self.x_speed > 0):
                            self.x_speed -= 1.2 * blob_friction # Turn around faster by holding left
                        elif(abs(self.x_speed) > blob_speed + (blob_friction * 2)):
                            self.x_speed -= blob_friction
                        else:
                            self.x_speed -= blob_friction # Accelerate based off of friction
                    else:
                        prev_speed = self.x_speed
                        self.x_speed = -1*blob_speed #If at max speed, maintain it
                        if(round(prev_speed) == blob_speed):
                            self.info['wavebounces'] += 1
                            createSFXEvent('wavebounce')
            elif(not 'left' in pressed and 'right' in pressed and not menu_open): #If holding right but not left
                self.facing = 'right'
                if(self.x_pos >= 1700): #Are we in danger of going off screen?
                    self.x_speed = 0
                    self.x_pos = 1700
                else:
                    if(abs(self.x_speed) < blob_speed):
                        if(self.x_speed < 0):
                            self.x_speed += 1.2 * blob_friction # Turn around faster by holding left
                        elif(abs(self.x_speed) > blob_speed + (blob_friction * 2)):
                            self.x_speed -= blob_friction
                        else:
                            self.x_speed += blob_friction # Accelerate based off of friction
                    else:
                        prev_speed = self.x_speed
                        self.x_speed = blob_speed #If at max speed, maintain it
                        if(round(prev_speed) == -1 * blob_speed):
                            self.info['wavebounces'] += 1
                            createSFXEvent('wavebounce') 
            else: #We're either not holding anything, or pressing both at once
                if(self.x_speed < 0): #If we're going left, decelerate
                    if(self.x_speed + blob_friction) > 0:
                        self.x_speed = 0 #Ensures that we don't decelerate and start moving backwards
                    else:
                        self.x_speed += blob_friction #Normal deceleration
                elif(self.x_speed > 0):
                    if(self.x_speed - blob_friction) < 0:
                        self.x_speed = 0 #Ensures that we don't decelerate and start moving backwards
                    else:
                        self.x_speed -= blob_friction #Normal deceleration
        self.x_pos += self.x_speed #This ensures that we are always adjusting our position
        self.info['x_distance_moved'] += abs(self.x_speed)
        if(self.x_pos <= 0): #Don't move off screen!
            self.x_speed = 0
            self.x_pos = 0
        elif(self.x_pos >= 1700): #Don't move off screen!
            self.x_speed = 0
            self.x_pos = 1700
        
        if(wavedashed and self.status_effects['shop']['defense_equip'] == 'sharp_shadow'):
            create_environmental_modifier(player = self.player, species='sharp_shadow', affects={'enemy'}, lifetime=25, x_pos=self.x_center-20, y_pos=self.y_center-20)
            self.status_effects['shop']['defense_durability'] -= 1
        elif(wavedashed and self.species == "cactus" and self.special_ability_meter >= 200 * Blob.nrg_multiplier):
            create_environmental_modifier(player = self.player, species='sharp_shadow', affects={'enemy'}, lifetime=25, x_pos=self.x_center-20, y_pos=self.y_center-20)
            self.special_ability_meter -= 200 * Blob.nrg_multiplier
        elif(wavedashed and self.species == "glue" and self.special_ability_meter >= 300 * Blob.nrg_multiplier):
            x_mod = 1 if self.facing == 'left' else -1
            create_environmental_modifier(self.player, affects = {'enemy', 'self', 'ball'}, species = 'glue_shot', x_pos = self.x_center, y_pos = self.y_center - 10, x_speed = (3*self.x_speed/4) + (6*x_mod), y_speed = -1, gravity = 0.25, lifetime = 600)
            create_environmental_modifier(self.player, affects = {'enemy', 'self', 'ball'}, species = 'glue_shot', x_pos = self.x_center, y_pos = self.y_center - 10, x_speed = (5*self.x_speed/4) + (6*x_mod), y_speed = -1, gravity = 0.25, lifetime = 600)
            create_environmental_modifier(self.player, affects = {'enemy', 'self', 'ball'}, species = 'glue_shot', x_pos = self.x_center, y_pos = self.y_center - 10, x_speed = (7*self.x_speed/4) + (6*x_mod), y_speed = -1, gravity = 0.25, lifetime = 600)
            create_environmental_modifier(self.player, affects = {'enemy', 'self', 'ball'}, species = 'glue_shot', x_pos = self.x_center, y_pos = self.y_center - 10, x_speed = (9*self.x_speed/4) + (6*x_mod), y_speed = -1, gravity = 0.25, lifetime = 600)            
            create_environmental_modifier(self.player, affects = {'enemy', 'self', 'ball'}, species = 'glue_shot', x_pos = self.x_center, y_pos = self.y_center - 10, x_speed = (11*self.x_speed/4) + (6*x_mod), y_speed = -1, gravity = 0.25, lifetime = 600)
            self.special_ability_meter -= 300 * Blob.nrg_multiplier
        #VERTICAL MOVEMENT
        if('up' in pressed and self.y_pos == Blob.ground and not menu_open): #If you press jump while grounded, jump!
            self.y_speed = (-1 * self.jump_force) + (bool(self.status_effects['glued']) * 0.25 * self.jump_force) - (0.75 * bool(self.status_effects['monado_effect'] == "JUMP") * 0.5 * self.jump_force)
            self.focus_lock = 0
            self.wavedash_lock = 0
            self.focusing = False
            self.info['jumps'] += 1
        elif('up' in pressed and self.y_speed < 0 and not menu_open):
            self.shorthopping = False
        elif(('up' not in pressed or menu_open) and self.y_speed < 0):
            self.shorthopping = True
        
        if('down' in pressed and not menu_open):
            self.down_holding_timer += 1
            if(self.y_pos < Blob.ground): #If you are above ground and press down
                self.fastfalling = True #Fast fall, increasing your gravity by 3 stars
            else:
                if(not self.focusing and not self.impact_land_frames and not wavedashed):
                    self.focusing = True
                    self.focus_lock = self.focus_lock_max
                elif(self.focusing):
                    self.focusing = True
        else:
            self.down_holding_timer = 0

        if((not 'down' in pressed or menu_open) and self.focus_lock == 0 and self.focusing):
            #True if we're not holding down, focus lock is done and we're focusing
            self.focusing = False
        if(self.y_pos < Blob.ground): #Applies gravity while airborne, respecting fast fall status.
            self.info['time_airborne'] += 1
            self.info['time_airborne_seconds'] = round(self.info['time_airborne']/60, 2)
            if(self.y_speed < 0):
                if(self.shorthopping):
                    self.y_speed += self.gravity_stars * 2
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
            if(self.status_effects['monado_effect'] == "JUMP"):
                create_environmental_modifier(player = self.player, affects = {'enemy', 'ball'}, species = 'spire_glyph', lifetime = 30, y_pos = 700)
                createSFXEvent('glyph')
        
        #ABILITY
        if('ability' in pressed and not menu_open):
            self.ability()

        # BOOST
        if('boost' in pressed and not menu_open):
            self.boost()
        
        #Kick
        if('kick' in pressed and not menu_open):
            self.kick()
        elif('block' in pressed and not menu_open):
            self.block()
        if(menu_open):
            menu_direction = 'neutral'
            menu_action = 'neutral'
            if('up' in pressed):
                menu_direction = 'up'
            elif('down' in pressed):
                menu_direction = 'down'
            elif('left' in pressed):
                menu_direction = 'left'
            elif('right' in pressed):
                menu_direction = 'right'
            self.status_effects['menu']['direction'] = menu_direction
            
            
            if(self.status_effects['menu']['type'] == 'cardpack'):
                if('ability' in pressed):
                    menu_action = 'ability'
                elif('kick' in pressed):
                    menu_action = 'kick'
                elif('block' in pressed):
                    menu_action = 'block'
                elif('boost' in pressed):
                    menu_action = 'boost'
                
                selected_card = ''
                other_card_1 = ''
                other_card_2 = ''
                if(menu_direction == 'left'):
                    selected_card = self.status_effects['cards']['pulled'][0]
                    other_card_1 = self.status_effects['cards']['pulled'][1]
                    other_card_2 = self.status_effects['cards']['pulled'][2]
                elif(menu_direction == 'up'):
                    other_card_1 = self.status_effects['cards']['pulled'][0]
                    selected_card = self.status_effects['cards']['pulled'][1]
                    other_card_2 = self.status_effects['cards']['pulled'][2]
                elif(menu_direction == 'right'):
                    other_card_1 = self.status_effects['cards']['pulled'][0]
                    other_card_2 = self.status_effects['cards']['pulled'][1]
                    selected_card = self.status_effects['cards']['pulled'][2]

                self.status_effects['menu']['time'] += 1

                if(menu_action != 'neutral' and self.status_effects['menu']['time'] > 10 and menu_direction != 'neutral' and menu_direction != 'down'):
                    
                    if(self.status_effects['cards'][menu_action]):
                        self.status_effects['cards']['recharge'].add(self.status_effects['cards'][menu_action])
                        self.status_effects['cards']['equipped'].remove(self.status_effects['cards'][menu_action])

                    self.status_effects['cards'][menu_action] = selected_card
                    self.status_effects['cards']['equipped'].add(selected_card)
                    card_pos = (0, 0)
                    if(menu_direction == "left"):
                        card_pos = (self.x_pos - 105, self.y_pos - 25)
                    elif(menu_direction == "up"):
                        card_pos = (self.x_pos + 20, self.y_pos - 225)
                    elif(menu_direction == "right"):
                        card_pos = (self.x_pos + 160, self.y_pos - 25)
                    self.status_effects['cards']['joker_particle'] = (card_pos, selected_card)
                    self.status_effects['menu']['open'] = False
                    self.status_effects['cards']['recharge'].add(other_card_1)
                    self.status_effects['cards']['recharge'].add(other_card_2)
                    if(menu_action == 'ability'):
                        self.special_ability_cooldown = self.special_ability_cooldown_max
                    elif('kick' in pressed):
                        self.special_ability_cooldown = self.special_ability_cooldown_max
                        self.kick_cooldown += 60 * Blob.timer_multiplier
                    elif('block' in pressed):
                        self.special_ability_cooldown = self.special_ability_cooldown_max
                        self.block_cooldown += 60 * Blob.timer_multiplier
                    elif('boost' in pressed):
                        self.special_ability_cooldown = self.special_ability_cooldown_max
                        self.boost_cooldown_timer += 60 * Blob.timer_multiplier
                    if(menu_direction == "up"):
                        self.jump_lock = 15

                    self.recharge_indicators['ability_swap'] = True

                elif(menu_direction == 'down' and self.status_effects['menu']['time'] > 10):
                    self.status_effects['cards']['recharge'].add(self.status_effects['cards']['pulled'][0])
                    self.status_effects['cards']['recharge'].add(self.status_effects['cards']['pulled'][1])
                    self.status_effects['cards']['recharge'].add(self.status_effects['cards']['pulled'][2])
                    self.status_effects['menu']['open'] = False
                    self.wavedash_lock = 15
                    self.special_ability_cooldown = self.special_ability_cooldown_max/2

                    '''if(menu_action == 'ability'):
                        self.special_ability_cooldown += 60 * Blob.timer_multiplier
                    elif('kick' in pressed):
                        self.kick_cooldown += 60 * Blob.timer_multiplier
                    elif('block' in pressed):
                        self.block_cooldown += 60 * Blob.timer_multiplier
                    elif('boost' in pressed):
                        self.boost_cooldown_timer += 60 * Blob.timer_multiplier'''
            elif(self.status_effects['menu']['type'] == 'monado'):
                if('ability' in pressed or 'kick' in pressed or 'block' in pressed or 'boost' in pressed):
                    menu_action = 'ability'

                
                self.status_effects['menu']['time'] += 1
                selected_card = ''
                if(self.status_effects['menu']['time'] > 5 and menu_direction != 'neutral'):
                    monado_activated = False
                    if(menu_direction == "up" and self.status_effects['monado_jump_cooldown'] <= 0):
                        self.jump_lock = 15
                        self.status_effects['monado_effect'] = "JUMP"
                        self.status_effects['monado_jump_cooldown'] = 1080
                        monado_activated = True
                    elif(menu_direction == "down" and self.status_effects['monado_shield_cooldown'] <= 0):
                        self.wavedash_lock = 15
                        self.status_effects['monado_effect'] = "SHIELD"
                        self.status_effects['monado_shield_cooldown'] = 1080
                        monado_activated = True
                    elif(menu_direction == "left" and self.status_effects['monado_smash_cooldown'] <= 0):
                        self.status_effects['monado_effect'] = "SMASH"
                        self.status_effects['monado_smash_cooldown'] = 1080
                        monado_activated = True
                    elif(menu_direction == "right" and self.status_effects['monado_speed_cooldown'] <= 0):
                        self.status_effects['monado_effect'] = "SPEED"
                        self.status_effects['monado_speed_cooldown'] = 1380
                        monado_activated = True
                    
                    if(monado_activated):
                        createSFXEvent('crunch')
                        self.status_effects['menu']['open'] = False
                        self.status_effects['monado_timer'] = 300
                        if(self.status_effects['monado_effect'] == "SHIELD"):
                            self.status_effects['monado_timer'] = 420
                        self.movement_lock = 5
                        self.special_ability_timer = self.special_ability_cooldown
                        self.special_ability_meter -= self.special_ability_cost
                        self.special_ability_cooldown = self.special_ability_cooldown_max
                    
                elif(menu_direction == 'neutral' and menu_action == 'ability' and self.status_effects['menu']['time'] > 15):
                    self.status_effects['menu']['open'] = False
                    self.special_ability_cooldown = self.special_ability_cooldown_max/2
                
                '''if(not self.status_effects['menu']['open']):
                    if('ability' in pressed):
                        self.special_ability_cooldown += 60 * Blob.timer_multiplier
                    elif('kick' in pressed):
                        self.kick_cooldown += 60 * Blob.timer_multiplier
                    elif('block' in pressed):
                        self.block_cooldown += 60 * Blob.timer_multiplier
                    elif('boost' in pressed):
                        self.boost_cooldown_timer += 60 * Blob.timer_multiplier'''
            elif(self.status_effects['menu']['type'] == 'shop'):
                if('ability' in pressed or 'kick' in pressed or 'block' in pressed or 'boost' in pressed):
                    menu_action = 'ability'

                
                self.status_effects['menu']['time'] += 1
                selected_card = ''
                if(self.status_effects['menu']['time'] > 5 and menu_direction != 'neutral'):
                    monado_activated = False
                    if(menu_direction == "up"): # Passive
                        self.jump_lock = 15
                        monado_activated = True
                        if(self.status_effects['shop']['passive_sale'] == 'soul_catcher'):
                            self.status_effects['shop']['passive_sale'] = 'grub_song'
                            self.status_effects['shop']['passive_equip'] = 'soul_catcher'
                            self.status_effects['shop']['passive_durability'] = 600
                            self.status_effects['shop']['purchase_particle'] = 'soul_catcher'
                        elif(self.status_effects['shop']['passive_sale'] == 'grub_song'):
                            self.status_effects['shop']['passive_sale'] = 'sprint_master'
                            self.status_effects['shop']['passive_equip'] = 'grub_song'
                            self.status_effects['shop']['passive_durability'] = 600
                            self.status_effects['shop']['purchase_particle'] = 'grub_song'
                        elif(self.status_effects['shop']['passive_sale'] == 'sprint_master'):
                            self.status_effects['shop']['passive_sale'] = 'soul_catcher'
                            self.status_effects['shop']['passive_equip'] = 'sprint_master'
                            self.status_effects['shop']['passive_durability'] = 300
                            self.status_effects['shop']['purchase_particle'] = 'sprint_master'
                    elif(menu_direction == "down"): # Focus
                        self.wavedash_lock = 15
                        monado_activated = True
                        if(self.status_effects['shop']['focus_sale'] == 'baldur_shell'):
                            self.status_effects['shop']['focus_sale'] = 'explosive_focus'
                            self.status_effects['shop']['focus_equip'] = 'baldur_shell'
                            self.status_effects['shop']['focus_durability'] = 2
                            self.status_effects['shop']['purchase_particle'] = 'baldur_shell'
                        elif(self.status_effects['shop']['focus_sale'] == 'explosive_focus'):
                            self.status_effects['shop']['focus_sale'] = 'soul_focus'
                            self.status_effects['shop']['focus_equip'] = 'explosive_focus'
                            self.status_effects['shop']['focus_durability'] = 2
                            self.status_effects['shop']['purchase_particle'] = 'explosive_focus'
                        elif(self.status_effects['shop']['focus_sale'] == 'soul_focus'):
                            self.status_effects['shop']['focus_sale'] = 'baldur_shell'
                            self.status_effects['shop']['focus_equip'] = 'soul_focus'
                            self.status_effects['shop']['focus_durability'] = 2
                            self.status_effects['shop']['purchase_particle'] = 'soul_focus'
                    elif(menu_direction == "left"): # Defense
                        monado_activated = True
                        if(self.status_effects['shop']['defense_sale'] == 'sharp_shadow'):
                            self.status_effects['shop']['defense_sale'] = 'thorns_of_agony'
                            self.status_effects['shop']['defense_equip'] = 'sharp_shadow'
                            self.status_effects['shop']['defense_durability'] = 3
                            self.status_effects['shop']['purchase_particle'] = 'sharp_shadow'
                        elif(self.status_effects['shop']['defense_sale'] == 'thorns_of_agony'):
                            self.status_effects['shop']['defense_sale'] = 'izumi_tear'
                            self.status_effects['shop']['defense_equip'] = 'thorns_of_agony'
                            self.status_effects['shop']['defense_durability'] = 3
                            self.status_effects['shop']['purchase_particle'] = 'thorns_of_agony'
                        elif(self.status_effects['shop']['defense_sale'] == 'izumi_tear'):
                            self.status_effects['shop']['defense_sale'] = 'sharp_shadow'
                            self.status_effects['shop']['defense_equip'] = 'izumi_tear'
                            self.status_effects['shop']['defense_durability'] = 2
                            self.status_effects['shop']['purchase_particle'] = 'izumi_tear'
                    elif(menu_direction == "right"): # Offense
                        monado_activated = True
                        if(self.status_effects['shop']['offense_sale'] == 'dream_wielder'):
                            self.status_effects['shop']['offense_sale'] = 'nailmasters_glory'
                            self.status_effects['shop']['offense_equip'] = 'dream_wielder'
                            self.status_effects['shop']['offense_durability'] = 3
                            self.status_effects['shop']['purchase_particle'] = 'dream_wielder'
                        elif(self.status_effects['shop']['offense_sale'] == 'nailmasters_glory'):
                            self.status_effects['shop']['offense_sale'] = 'heavy_blow'
                            self.status_effects['shop']['offense_equip'] = 'nailmasters_glory'
                            self.status_effects['shop']['offense_durability'] = 3
                            self.status_effects['shop']['purchase_particle'] = 'nailmasters_glory'
                        elif(self.status_effects['shop']['offense_sale'] == 'heavy_blow'):
                            self.status_effects['shop']['offense_sale'] = 'dream_wielder'
                            self.status_effects['shop']['offense_equip'] = 'heavy_blow'
                            self.status_effects['shop']['offense_durability'] = 2
                            self.status_effects['shop']['purchase_particle'] = 'heavy_blow'
                    
                    if(monado_activated):
                        createSFXEvent('crunch')
                        self.status_effects['menu']['open'] = False
                        #self.status_effects['monado_timer'] = 300
                        #if(self.status_effects['monado_effect'] == "SHIELD"):
                        #    self.status_effects['monado_timer'] = 420
                        self.movement_lock = 5
                        self.special_ability_timer = self.special_ability_cooldown
                        self.special_ability_meter -= self.special_ability_cost
                        self.special_ability_cooldown = self.special_ability_cooldown_max
                    
                elif(menu_direction == 'neutral' and menu_action == 'ability' and self.status_effects['menu']['time'] > 15):
                    self.status_effects['menu']['open'] = False
                    self.special_ability_cooldown = self.special_ability_cooldown_max/2
                
                '''if(not self.status_effects['menu']['open']):
                    if('ability' in pressed):
                        self.special_ability_cooldown += 60 * Blob.timer_multiplier
                    elif('kick' in pressed):
                        self.kick_cooldown += 60 * Blob.timer_multiplier
                    elif('block' in pressed):
                        self.block_cooldown += 60 * Blob.timer_multiplier
                    elif('boost' in pressed):
                        self.boost_cooldown_timer += 60 * Blob.timer_multiplier'''
                


    
        self.x_center = self.x_pos + 83 #Rough estimate :)
        self.y_center = self.y_pos + 110 #Rough estimate :)

        return pressed
    
    def tutorial_move(self, pressed_buttons, tutorial_slide):
        pressed = merge_inputs(pressed_buttons, override=True)
        # TODO: Filter out inputs based on the tutorial_slide
        self.move(pressed)

    def set_base_stats(self, stars):
        self.top_speed = 10+(1*stars['top_speed'])
        self.base_top_speed = self.top_speed
        self.traction = 0.2 + (stars['traction'] * 0.15) #Each star increases traction
        self.friction = 0.2 + (stars['friction'] * 0.15) #Each star increases friction
        self.base_traction = self.traction #Non-boosted
        self.base_friction = self.friction #No boost
        self.gravity_stars = round(.3 + (stars['gravity'] * .15), 3) #Each star increases gravity
        self.gravity_mod = self.gravity_stars * 3 #Fastfalling increases gravity
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