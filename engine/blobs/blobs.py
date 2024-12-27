#from resources.sound_engine.sfx_event import createSFXEvent
#from engine.blob_stats import species_to_stars
import pygame as pg
from json import loads
from resources.sound_engine.sfx_event import createSFXEvent
import math
from resources.graphics_engine.display_particles import draw_teleportation_pfx
from engine.environmental_modifiers import create_environmental_modifier

default_stars = { #Gets many values for each blob
    'max_hp': 3,
    'top_speed': 3,
    'traction': 3,
    'friction': 3,
    'gravity': 3,
    'kick_cooldown_rate': 3,
    'block_cooldown_rate': 3,
    'boost_cost': 600,
    'boost_cooldown_max': 3,
    'boost_duration': 3,

    'special_ability': 'boost',
    'special_ability_category': 'instant',
    'special_ability_cost': 600,
    'special_ability_maintenance': 3,
    'special_ability_max': 1800,
    'special_ability_cooldown': 300,
    'special_ability_delay': 10,
    'special_ability_duration': 60,
}

player_controls = {
    1:  {
            'p1_up': 'up',
            'p1_down': 'down',
            'p1_left': 'left',
            'p1_right': 'right',
            'p1_ability': 'ability',
            'p1_kick': 'kick',
            'p1_block': 'block',
            'p1_boost': 'boost'
        },
    2:  {
            'p2_up': 'up',
            'p2_down': 'down',
            'p2_left': 'left',
            'p2_right': 'right',
            'p2_ability': 'ability',
            'p2_kick': 'kick',
            'p2_block': 'block',
            'p2_boost': 'boost'
        },
    3:  {
            'p3_up': 'up',
            'p3_down': 'down',
            'p3_left': 'left',
            'p3_right': 'right',
            'p3_ability': 'ability',
            'p3_kick': 'kick',
            'p3_block': 'block',
            'p3_boost': 'boost'
        },
    4:  {
            'p4_up': 'up',
            'p4_down': 'down',
            'p4_left': 'left',
            'p4_right': 'right',
            'p4_ability': 'ability',
            'p4_kick': 'kick',
            'p4_block': 'block',
            'p4_boost': 'boost'
        },
}

class Blob:
    ground = 1200
    ceiling = 200
    timer_multiplier = 2
    nrg_multiplier = 5
    all_blobs = {}
    sprite_collisions = {}

    def __init__(self, x_pos = 50, y_pos = 1200, facing = 'left', player = 1, 
    special_ability_charge_base = 1, costume = 0, danger_zone_enabled = True, is_cpu = False, stat_overrides = {}, match_state = None, init_blob_path = __file__):
        self.init_json = self.load_init_blob(init_blob_path)
        self.species = "base"
        self.player = player #Player 1 or 2
        if(player == 1):
            self.danger_zone = 225
        else:
            self.danger_zone = 1475
        self.is_cpu = is_cpu
        self.cpu_memory = {'press_queue': [], 'game_state': '', 'current_play': ''}
        self.costume = costume
        self.blob_images = {}
        self.ability_icons = {}
        self.stars = self.init_json["stars"]
        self.x_speed = 0
        self.x_kb = 0
        self.y_speed = 0
        self.x_pos = x_pos #Where the blob is on the X axis
        self.y_pos = y_pos #Where the blob is on the Y axis, 1200 is grounded
        self.x_center = x_pos + 83
        self.y_center = y_pos + 110
        self.facing = facing #Where the blob is currently facing
        self.fastfalling = False
        self.shorthopping = False
        
        self.kick_cooldown_rate = 2 # Each star reduces kick cooldown
        self.kick_cooldown = 0 #Cooldown timer between kicks
        self.kick_timer = 0 #Active frames of kick
        self.kick_visualization = 0
        self.kick_visualization_max = 15

        self.block_cooldown_rate = 2 #Each star reduces block cooldown
        self.block_cooldown = 0 #Block cooldown timer
        self.block_timer = 0 #How much time is left in the current block
        self.block_timer_max = 15 #How many frames a block lasts.

        self.block_outer = 150
        self.block_inner = -25
        self.block_upper = -200
        self.block_lower = 200

        self.boost_cooldown_rate = 2
        self.boost_cooldown_timer = 0 #Timer that measures between boosts
        self.boost_timer = 0 #How much time is left in the current boost

        self.down_holding_timer = 0
        self.focus_lock = 0 #Timer that locks movement when a blob is focusing
        self.focus_lock_max = 60
        self.focusing = False
        self.impact_land_frames = 0 #Locks the player from focusing after landing (fastfall leniency)

        self.special_ability_charge = 1 * Blob.nrg_multiplier # Charge rate. Each frame increases the SA meter by 1 point, or more if focusing
        self.special_ability_meter = 0 #Amount of SA charge stored up
        self.special_ability_timer = 0 #Timer that counts down between uses of an SA
        self.special_ability_duration = 0 #Time that a SA is active
        self.special_ability_cooldown = 0 #Cooldown between uses
        self.special_ability_charge_base = special_ability_charge_base * Blob.nrg_multiplier
        self.special_ability_cooldown_rate = 2
        self.used_ability = {}
        self.ability_holding_timer = 0 # Used for held abilities

        self.apply_stat_overrides(stat_overrides)
        self.set_base_stats(self.stars)

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
            "shop": {'heart_lvl': 0, 'spring_lvl': 0, 'sprint_lvl': 0, 'shadow_lvl': 0, 'purchase_particle': None},

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
        # TODO: Add image initialization
        self.initialize_blob_sprites()

    def load_init_blob(self, blob_path=""):
        init_path = blob_path.rsplit("\\", 1)
        #print(init_path)
        try:
            with open(init_path[0]+"\\init.blob", "r") as f:
                init_file = f.read()
        except Exception as ex:
            print("EXCEPTION CAUGHT")
            print(ex)
            init_file = {
                "stars": {
                    "max_hp": 3,
                    "top_speed": 3,
                    "traction": 3,
                    "friction": 3,
                    "gravity": 3,
                    "kick_cooldown_rate": 3,
                    "block_cooldown_rate": 3,
                    "boost_cost": 600,
                    "boost_cooldown_max": 3,
                    "boost_duration": 3,
                    "special_ability": "boost",
                    "special_ability_category": "instant",
                    "special_ability_cost": 600,
                    "special_ability_maintenance": 3,
                    "special_ability_max": 1800,
                    "special_ability_cooldown": 300,
                    "special_ability_delay": 10,
                    "special_ability_duration": 60
                },
                "descriptors": {
                    "species": "quirkless",
                    "path": "quirkless"
                },
                "costumes": {
                    "0": {
                        "alive": "quirkless_blob.png", 
                        "dead": "quirkless_blob_-1.png",
                        "ability": "boost_icon.png"
                    }
                }
            }
            return init_file
        #print(init_file)
        return loads(init_file)
    
    def apply_status_effect(self, effect = "reflecting", duration = 60, limit = 600, method = "add"):
        '''
        Applies a status effect to a Blob
        Inputs:
            - effect (string): Refers to a key within the blob dictionary
            - duration (int): Duration in frames
            - limit (int): If you are adding to this status effect, this is the limit that you can't go over
            - method (str): Should either be "add" (adds duration to current status value, but makes sure that the initial duration is 0 or greater), "true_add" (adds duration to the current value, no questions asked) or "set" (sets the duration ignoring everything else)
        '''
        if(method == "set" or (method == "add" )):
            self.status_effects[effect] = duration
        elif(method == "add"):
            old_duration = self.status_effects[effect]
            if(self.status_effects[effect] < 0):
                self.status_effects[effect] = duration
            else:
                self.status_effects[effect] += duration
            if(self.status_effects[effect] > limit and old_duration < limit): 
                self.status_effects[effect] = limit
            elif(self.status_effects[effect] > limit and old_duration >= limit):
                self.status_effects[effect] = old_duration
        elif(method == "true_add"):
            self.status_effects[effect] += duration
            if(self.status_effects[effect] > limit): 
                self.status_effects[effect] = limit

    def cooldown_status_effects(self):
        # TODO: Figure this out
        special_ability_cooldown_rate = Blob.timer_multiplier
        kick_cooldown_rate = Blob.timer_multiplier
        block_cooldown_rate = Blob.timer_multiplier
        boost_cooldown_rate = Blob.timer_multiplier
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
                        kick_cooldown_rate = 1
                        block_cooldown_rate = 1
                        special_ability_cooldown_rate = 1
                        boost_cooldown_rate = 1
                        if(self.status_effects['overheat'] == 0):
                            special_ability_cooldown_rate = Blob.timer_multiplier
                            kick_cooldown_rate = Blob.timer_multiplier
                            block_cooldown_rate = Blob.timer_multiplier
                            boost_cooldown_rate = Blob.timer_multiplier
                    if(effect == 'loaned'):
                        kick_cooldown_rate += 4
                        block_cooldown_rate += 4
                        special_ability_cooldown_rate += 4
                        boost_cooldown_rate += 4
                    if(effect == 'hyped'):
                        kick_cooldown_rate += 1
                        block_cooldown_rate += 1
                        special_ability_cooldown_rate += 1
                        boost_cooldown_rate += 1
                    if(effect == 'monado_timer' and self.status_effects[effect] == 1):
                        self.status_effects['monado_effect'] = None
                    if(effect == 'monado_timer' and self.status_effects[effect] > 1 and self.status_effects['monado_effect'] == "JUMP"):
                        '''self.kick_cooldown_rate += 1
                        self.block_cooldown_rate += 1
                        self.special_ability_cooldown_rate += 1
                        self.boost_cooldown_rate += 1'''
                    
                    if(effect == 'monado_timer' and self.status_effects[effect] > 1 and self.status_effects['monado_effect'] == "SHIELD"):
                        block_cooldown_rate += 5
                    
                    if(effect == 'monado_timer' and self.status_effects[effect] > 1 and self.status_effects['monado_effect'] == "SMASH"):
                        kick_cooldown_rate += 3

                    self.kick_cooldown_rate = kick_cooldown_rate
                    self.block_cooldown_rate = block_cooldown_rate
                    self.special_ability_cooldown_rate = special_ability_cooldown_rate
                    self.boost_cooldown_rate = boost_cooldown_rate
                except:
                    pass # Typically pass for strings, like current pill
    
    def cooldown_default(self):
        if(self.focusing):
            self.special_ability_charge = (self.special_ability_charge_base - (bool(self.status_effects["nrg_fatigue"]) * 3)) * 5
            self.info['time_focused'] += 1
            self.info['time_focused_seconds'] = round(self.info['time_focused']/60, 2)
            if(self.y_pos < Blob.ground):
                self.focusing = False
                self.focus_lock = 0
        else:
            self.special_ability_charge = self.special_ability_charge_base - (bool(self.status_effects["nrg_fatigue"]) * 3) + self.status_effects["shop"]["heart_lvl"]

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
        
        if(self.special_ability_timer > 0):
            self.special_ability_timer -= 1
        
        new_dict = {}

        for ability in self.used_ability:
            if(self.used_ability[ability] > 0):
                new_dict[ability] = self.used_ability[ability] - 1
            
            self.used_ability = new_dict
        self.cooldown_status_effects()

        if(self.impact_land_frames):
            self.impact_land_frames -= 1

        if(self.movement_lock > 0):
            self.movement_lock -= 1

        if(self.jump_lock > 0):
            self.jump_lock -= 1

        if(self.focus_lock > 0):
            self.focus_lock -= 1
        
        if(self.wavedash_lock > 0):
            self.wavedash_lock -= 1

        if(self.parried):
            self.parried -= 1
        
        if(self.perfect_parried):
            self.perfect_parried -= 1

        if(self.clanked):
            self.clanked -= 1

        self.ability_cooldown_visualization = Blob.create_visualization(self.special_ability_cooldown/Blob.timer_multiplier)
        self.ability_cooldown_percentage = self.special_ability_cooldown/self.special_ability_cooldown_max
        self.kick_cooldown_visualization = Blob.create_visualization(self.kick_cooldown/self.kick_cooldown_rate)
        self.kick_cooldown_percentage = self.kick_cooldown/self.kick_cooldown_max
        self.block_cooldown_visualization = Blob.create_visualization(self.block_cooldown/self.block_cooldown_rate)
        self.block_cooldown_percentage = self.block_cooldown/self.block_cooldown_max
        self.boost_cooldown_visualization = Blob.create_visualization(self.boost_cooldown_timer/Blob.timer_multiplier)
        self.boost_cooldown_percentage = self.boost_cooldown_timer/self.boost_cooldown_max
        self.boost_timer_visualization = Blob.create_visualization(self.boost_timer)
        self.boost_timer_percentage = self.boost_timer/self.boost_duration

        if(self.collision_timer > 0):
            self.collision_timer -=1 

        if(self.damage_flash_timer):
            self.damage_flash_timer -= 1

    def create_visualization(number):
        return math.ceil(number/6)/10

    def cooldown(self):
        # Used by all blobs
        self.cooldown_default()

    def check_cooldown_completion(self, updatedAbility = True, updatedKick = True, updatedBlock = True, updatedBoost = True):
        # Used by Doctor and King blobs
        if(self.special_ability_cooldown <= 0 and updatedAbility):
            self.toggle_recharge_indicator('ability', 2)
        if(self.kick_cooldown <= 0 and updatedKick):
            self.toggle_recharge_indicator('kick', 2)
        if(self.block_cooldown <= 0 and updatedBlock):
            self.toggle_recharge_indicator('block', 2)
        if(self.boost_cooldown_timer <= 0 and updatedBoost):
            self.toggle_recharge_indicator('boost', 2)

    def update_ability_icon(self, icon):
        # Used by Doctor and possibly Joker Blobs
        self.ability_icons['default'] = self.ability_icons[icon]
        self.recharge_indicators['ability_swap'] = True

    def ability(self):
        # Used by all blobs
        pass

    def kick(self, ignore_cooldown = False):
        # Used by all blobs. Merchant and Joker blobs have notable variants
        # Boost kicks?
        if(self.kick_cooldown <= 0 or ignore_cooldown):
            createSFXEvent('kick')
            self.block_cooldown += 5 * (self.block_cooldown_rate)
            self.kick_timer = 2
            self.kick_cooldown = self.kick_cooldown_max
            #self.collision_timer = 0
            self.collision_distance = 175
            self.kick_visualization = self.kick_visualization_max
            self.info['kick_count'] += 1

    def block(self, ignore_cooldown = False):
        # Used by all blobs. Merchant and Joker blobs have notable variants
        if(self.block_cooldown <= 0 or ignore_cooldown):
            createSFXEvent('block')
            self.kick_cooldown += 5 * (self.kick_cooldown_rate)
            self.block_cooldown = self.block_cooldown_max #Set block cooldown
            self.block_timer = self.block_timer_max #Set active block timer
            self.movement_lock = 10
            self.x_speed = 0
            if(self.y_speed < 0): #If we are moving upwards, halt your momentum!
                self.y_speed = 0
            self.info['block_count'] += 1

    def add_boost(self, boost_duration):
        '''
        Directly adds boost_duration to the blob's boost_timer - super useful for things like Lightning Blob's Thunderbolt or Doctor Blob's Steroid Pill
        '''
        createSFXEvent('boost')
        self.boost_timer += boost_duration
        self.top_speed = self.boost_top_speed
        self.traction = self.boost_traction
        self.friction = self.boost_friction
        self.info['boost_count'] += 1

    def boost(self, ignore_cooldown = False):
        # Used by all blobs
        if(self.special_ability_meter >= self.boost_cost and self.boost_cooldown_timer <= 0 or ignore_cooldown):
            self.special_ability_meter -= self.boost_cost # Remove some SA meter
            self.boost_cooldown_timer += self.boost_cooldown_max
            self.add_boost(self.boost_duration)

    def apply_boost_kick_effect(self, blob):
        pass

    def check_blob_collision_default(self, blob):
        hit_dict = {
            "accumulated_damage": 0,
            "status_effects": [],
            "pierce": 0,
            "x_speed_mod": 0,
            "hit_registered": False
        }
        if(self.x_center - (1.5 * self.collision_distance) <= blob.x_center <= self.x_center + (1.5 * self.collision_distance)):
            if(self.y_center - (1.1 * self.collision_distance) <= blob.y_center <= self.y_center + (self.collision_distance)):
                hit_dict["hit_registered"] = True
                hit_dict["accumulated_damage"] = 2
                hit_dict["pierce"] = 0
                hit_dict["x_speed_mod"] = 0
                if(self.boost_timer > 0):  # Take additional damage if the enemy is boosting
                    hit_dict["accumulated_damage"] += 1
                    self.apply_boost_kick_effect(blob)
                if(((blob.player == 2 and blob.x_pos >= blob.danger_zone) or (blob.player == 1 and blob.x_pos <= blob.danger_zone)) and blob.danger_zone_enabled):
                    #Take additional damage from kicks if you are hiding by your goal
                    hit_dict["accumulated_damage"] += 1
                if(self.status_effects['steroided']):
                    hit_dict["pierce"] += 1
        return hit_dict
                

    def check_blob_collision(self, blob):
        # Used by all blobs
        hit_dict = self.check_blob_collision_default(blob)
        if(hit_dict["hit_registered"]):
            blob.take_damage(hit_dict["accumulated_damage"], source = self, status_effects = hit_dict["status_effects"], pierce = hit_dict["pierce"], x_speed_mod = hit_dict["x_speed_mod"])

    def check_ability_collision(self, blob):
        # Used by all blobs
        if(("gale" in self.used_ability) or \
            ("gale" in blob.used_ability)):
            if blob.y_pos != blob.ground and not blob.block_timer: #Gale Affecting the opponent
                if(self.player == 1 and "gale" in self.used_ability): #Airborne
                    blob.x_pos += 7
                elif(self.player == 2 and "gale" in self.used_ability):
                    blob.x_pos -= 7
        if("c&d" in self.used_ability):
            blob.apply_status_effect("judged", duration = self.special_ability_duration)
            if(self.species != "judge"):
                blob.apply_status_effect("judged", duration = 90)
        if("stoplight" in self.used_ability):
            blob.apply_status_effect("stoplit", duration = 30)
        if("tax" in self.used_ability):
            
            self.status_effects['taxing'] = self.special_ability_duration
            blob.status_effects['taxed'] = self.special_ability_duration
            print(self.status_effects['taxing'])
            if(self.species != "king"):
                self.status_effects['taxing'] = 240
                blob.status_effects['taxed'] = 240
            self.set_base_stats(blob.return_stars())
            blob.set_base_stats(self.return_stars())

    def check_environmental_collisions(self, environment):
        # Used by all blobs, but it could be refactored
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
                    self.take_damage(source = self.all_blobs[hazard.player], y_speed_mod = -40 - (5 * (self.gravity_mod - 1.05)), status_effects=[["stunned", 20, 30, "add"]])
                    # TODO: Reflection
                else:
                    self.take_damage(damage=0)
                    self.block_cooldown += 30 * Blob.timer_multiplier
        
        for hazard in environment['thunder_bolt']:
            if(hazard.player == self.player and hazard.lifetime == hazard.max_lifetime - 1 and 'self' in hazard.affects and hazard.x_pos - 110 <= self.x_center <= hazard.x_pos + 240):
                self.add_boost(120)
            
            if(hazard.player != self.player and hazard.lifetime == hazard.max_lifetime - 1 and 'enemy' in hazard.affects and hazard.x_pos - 80 <= self.x_center <= hazard.x_pos + 215):
                self.take_damage(source = self.all_blobs[hazard.player],)

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
                    self.take_damage(damage = accumulated_damage, source = self.all_blobs[hazard.player], unblockable=True, unclankable=True, status_effects=[["stunned", 20, 30, "add"]])
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
                self.kick(ignore_cooldown=True)
                createSFXEvent('teleport')
                draw_teleportation_pfx([self.x_pos, self.y_pos])
                #print("teleported to", hazard.x_pos, hazard.y_pos, hazard.species)
            elif(hazard.player != self.player):
                if(self.x_center - 130 <= hazard.x_pos <= self.x_center + 75 and self.y_center - 125 <= hazard.y_pos <= self.y_center + 50):
                    if(self.status_effects['judged'] < 60):
                        self.status_effects['judged'] = 60
                    if(self.status_effects['hypothermia'] < 60):
                        self.status_effects['hypothermia'] = 60#
                    #self.take_damage(damage = 0, unblockable=True, unclankable=True, status_effects=[['judged', 60], ['hypothermia', 60]])
        
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
                    self.take_damage(damage = 1, source = self.all_blobs[hazard.player], status_effects = [["stunned", 20, 30, "add"], ['nrg_fatigue', 300, 300,"add"]])
                    hazard.affects.add(self.player)
        
        for hazard in environment['sharp_shadow']:
            if(hazard.player == self.player):
                hazard.x_pos = self.x_center - 20
                hazard.y_pos = self.y_center - 20
            
            if(hazard.player != self.player and self.player not in hazard.affects and self.x_center - 130 <= hazard.x_pos <= self.x_center + 75 and\
                self.y_center - 185 <= hazard.y_pos <= self.y_center + 175):
                stun_amount = 120
                self.take_damage(damage=hazard.hp, source = self.all_blobs[hazard.player])
                hazard.affects.add(self.player)
                
    
    def check_block(self, show_parry):
        """
        
        """
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
        
    def check_clank(self):
        if(self.kick_timer == 1):  # Kicking?
            self.clanked = 2
            self.info['clanks'] += 1
            createSFXEvent('clank')
            return False # We failed the clank check, don't take damage
        else:
            return True # Return true if the clank check passes
        
    def calculate_damage(self, damage):
        return damage - bool(self.status_effects['reflecting'] > 0) # Damage is reduced by 1 if we are reflecting

    def handle_post_damage(self, source=None):
        # Used for Mirror Blob's reflect, etc.
        if(self.status_effects["reflecting"]):
            if(source):
                source.take_damage(damage=1, unblockable = True, unclankable = True)
            #print(source)
            self.apply_status_effect("reflect_break", duration = 68, method = "set")
            self.special_ability_cooldown += 180 * Blob.timer_multiplier
        

    def take_damage(self, damage = 1, source = None, unblockable = False, unclankable = False, damage_flash_timer = 60, y_speed_mod = 0, x_speed_mod = 0,\
    show_parry = True, status_effects = [], pierce = 0):
        # Used by all blobs, but it could be refactored
        """
        Set damage_taken and pierced flags to False
        Check for Monado Effect "SMASH" (we should check for "JUMP" and "SPEED" as well, no?)
        If Else:
            - Unblockable and Unclankable --> Check block and always set damage_taken to true (Why, exactly? It's so we can check for Perfect Parries)
            - Unclankable only --> Check block and conditionally set damage_taken to true
            - Unblockable only --> Check clank and conditionally set damage_taken to true
            - Neither --> Check block, then clank, and conditionally set damage_taken to true
        If damage is not taken but we have pierce --> Set damage to pierce value but then reduce damage if using SMASH or SHIELD Monado (This is counterintuitive - SMASH should increase Pierce damage)
        If damage_taken == False --> Return 0
        Else: 
            - Set initial_hp to current blob HP
            - Reduce HP
                - Start with damage taken
                - Reduce Damage: Reflecting, SHIELD Monado, Focusing + Baldur Shell (Which I think is getting reworked)
                - Increase Damage: SPEED Monado, 2xSMASH Monado,
            - Reduce Baldur Shell durability if conditions are met
            - Set: blob's damage flash timer, blob info "damage_taken", blob status "stunned" (this should be changed), blob y_speed (think knockback), blob x_kb
            - Play Hit SFX
            - Toggle damage_flash (for what purpose?)
            - For Fisher Blob, apply silence conditionally
            - Loop through status effects and apply them (this should be its own function)
            - Return initial hp - current blob hp
        """
        damage_taken = False
        pierced = False
        if(unblockable and unclankable):
            # If this attack can't be blocked, parried, or clanked check for a perfect parry anyway for energy gain, but let the game know that you've taken damage
            self.check_block(show_parry)
            damage_taken = True
        elif(unclankable):
            # If this attack can't be clanked with, check to see if it was blocked instead
            damage_taken = self.check_block(show_parry)
        elif(unblockable):
            # If this attack can't be blocked, but can be clanked (what kind of scenario is this??)
            damage_taken = self.check_clank()
        else:
            # If the attack can be blocked and clanked with as normal, check for those
            damage_taken = self.check_block(show_parry) and self.check_clank()
        
        if(not damage_taken and pierce):
            # If we have a pierce value, we will use that instead of the default damage
            damage_taken = True
            damage = pierce

        if(damage_taken):
            # Triggers assuming we got past blocks, clanks, parries, and lack of pierce
            initial_hp = self.hp
            self.hp -= self.calculate_damage(damage)
            self.damage_flash_timer = damage_flash_timer
            self.info['damage_taken'] += damage
            self.y_speed = y_speed_mod
            self.x_kb = x_speed_mod   
            createSFXEvent('hit')
            if(not self.recharge_indicators['damage_flash']):  # If we're hit twice on the same frame, don't disable the flash!
                self.toggle_recharge_indicator('damage_flash')     
            for status_effect in status_effects:
                self.apply_status_effect(status_effect[0], status_effect[1], status_effect[2], status_effect[3])
                self.status_effects[status_effect[0]] += status_effect[1]
            self.handle_post_damage(source)
            return initial_hp - self.hp
        return 0

    def heal_hp(self, heal_amt = 1, overheal = False):
        # Used by all blobs
        old_hp = self.hp
        self.hp += heal_amt
        if not overheal and self.hp > self.max_hp:
            self.hp = self.max_hp
        if(old_hp < self.hp):
            self.toggle_recharge_indicator('heal_flash')

    def blob_ko(self):
        # Used by all blobs
        # TODO: Rewrite this for a more interesting KO!
        self.y_speed = 10
        if(self.y_pos < 2000):
            self.y_pos += self.y_speed

    def reset(self):
        # Used by all blobs, but it could be refactored
        self.x_speed = 0
        self.y_speed = 0
        self.x_kb = 0
        if(self.player == 1):
            self.x_pos = 100
            self.facing = 'right'
        else:
            self.x_pos = 1600
            self.facing = 'left'
        self.move([])
        self.y_pos = Blob.ground
        self.boost_timer = 0
        self.focus_lock = 0
        self.kick_visualization = 0
        self.block_timer = 0
        self.focusing = False
        self.damage_flash_timer = 0
        #self.image = species_to_image(self.species, self.costume)[0]
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
        self.set_base_stats(self.stars, set_hp = False)
        #self.heal_hp(heal_amt=ruleset['hp_regen'])

    def cpu_logic(self):
        # Used by all blobs, but each blob would have a different version
        pass

    def convert_inputs(self, pressed_buttons: list):
        '''
        Takes the pressed array (which is an array of up to 32 keys) and turns them into generic inputs
        Inputs:
            - pressed_buttons (list): Could look something like ['p1_ability', 'p2_kick']
            - self.player (int): Used to determine which inputs are used for movement
        Outputs:
            - pressed (list): Generic list that looks something like ['right', 'ability']
        '''
        pressed_conversions = player_controls[self.player]

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
        return pressed

    def drop_inputs(self, pressed):
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
        return pressed

    def set_maximum_speeds(self):
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
        if(self.status_effects['shop']['sprint_lvl'] == 1):
            blob_speed += 1
            blob_traction += 3
            blob_friction += 3
        elif(self.status_effects['shop']['sprint_lvl'] == 2):
            blob_speed += 2
            blob_traction += 5
            blob_friction += 5
        return {"blob_speed": blob_speed, "blob_traction": blob_traction, "blob_friction": blob_friction, "wavedashed": False}

    def calculate_horizontal_speed(self, pressed, frame_stats):
        if(self.y_pos == Blob.ground): #Applies traction if grounded
            if('left' in pressed and not 'right' in pressed and not self.status_effects['menu']['open']): #If holding left but not right
                if(not self.focusing):
                    self.facing = "left"
                    if(abs(self.x_speed) < frame_stats['blob_speed']):
                        if(self.x_speed > 0):
                            self.x_speed -= 1.2 * frame_stats['blob_traction'] # Turn around faster by holding left
                        elif(abs(self.x_speed) > frame_stats['blob_speed'] + (frame_stats['blob_traction'] * 2)): # Ease back into top speed if we're above it
                            self.x_speed -= frame_stats['blob_traction']
                        else:
                            self.x_speed -= frame_stats['blob_traction'] # Accelerate based off of traction
                    elif(abs(self.x_speed) > frame_stats['blob_speed'] + (frame_stats['blob_traction'] * 2)): # Ease back into top speed if we're above it
                        self.x_speed += frame_stats['blob_traction']
                    else: # Snap back to top speed
                        prev_speed = self.x_speed
                        self.x_speed = -1*frame_stats['blob_speed'] #If at max speed, maintain it
                        if(round(prev_speed) == frame_stats['blob_speed']):
                            self.info['wavebounces'] += 1
                            createSFXEvent('wavebounce')
                elif('down' in pressed):
                    self.wavedash_lock = 15
                    #self.collision_timer = 30
                    #self.x_speed = -1 * (15 + (10 * frame_stats['blob_traction']))
                    self.x_speed = -30 if bool(self.status_effects['shop']['shadow_lvl']) else -20
                    self.focusing = False
                    self.focus_lock = 0
                    frame_stats['wavedashed'] = True
                    createSFXEvent('wavedash')
            elif(not 'left' in pressed and 'right' in pressed and not self.status_effects['menu']['open']): #If holding right but not left
                if(not self.focusing):
                    self.facing = 'right'
                    if(abs(self.x_speed) < frame_stats['blob_speed']):
                        if(self.x_speed < 0):
                            self.x_speed += 1.2 * frame_stats['blob_traction'] # Turn around faster by holding left
                        elif(abs(self.x_speed) > frame_stats['blob_speed'] + (frame_stats['blob_traction'] * 2)):
                            self.x_speed += frame_stats['blob_traction']
                        else:
                            self.x_speed += frame_stats['blob_traction'] # Accelerate based off of traction
                    elif(abs(self.x_speed) > frame_stats['blob_speed'] + (frame_stats['blob_traction'] * 2)): # Ease back into top speed if we're above it
                        self.x_speed -= frame_stats['blob_traction']
                    else: # Snap back to top speed
                        prev_speed = self.x_speed
                        self.x_speed = frame_stats['blob_speed'] #If at max speed, maintain it
                        if(round(prev_speed) == -1 * frame_stats['blob_speed']):
                            self.info['wavebounces'] += 1
                            createSFXEvent('wavebounce')
                elif('down' in pressed):
                    self.wavedash_lock = 15
                    #self.collision_timer = 30
                    #self.x_speed = 15 + (10 * frame_stats['blob_traction'])
                    self.x_speed = 30 if bool(self.status_effects['shop']['shadow_lvl']) else 20
                    self.focusing = False
                    frame_stats['wavedashed'] = True
                    createSFXEvent('wavedash')

            else: #We're either not holding anything, or pressing both at once
                if(self.x_speed < 0): #If we're going left, decelerate
                    if(self.x_speed + frame_stats['blob_traction']) > 0:
                        self.x_speed = 0 #Ensures that we don't decelerate and start moving backwards
                    else:
                        self.x_speed += frame_stats['blob_traction'] #Normal deceleration
                elif(self.x_speed > 0):
                    if(self.x_speed - frame_stats['blob_traction']) < 0:
                        self.x_speed = 0 #Ensures that we don't decelerate and start moving backwards
                    else:
                        self.x_speed -= frame_stats['blob_traction'] #Normal deceleration
        else: #Applies friction if airborne
            if('left' in pressed and not 'right' in pressed and not self.status_effects['menu']['open']): #If holding left but not right
                self.facing = "left"
                if(self.x_pos <= 0): #Are we in danger of going off screen?
                    self.x_speed = 0
                    self.x_pos = 0
                else:
                    if(abs(self.x_speed) < frame_stats['blob_speed']):
                        if(self.x_speed > 0):
                            self.x_speed -= 1.2 * frame_stats['blob_friction'] # Turn around faster by holding left
                        elif(abs(self.x_speed) > frame_stats['blob_speed'] + (frame_stats['blob_friction'] * 2)):
                            self.x_speed -= frame_stats['blob_friction']
                        else:
                            self.x_speed -= frame_stats['blob_friction'] # Accelerate based off of friction
                    else:
                        prev_speed = self.x_speed
                        self.x_speed = -1*frame_stats['blob_speed'] #If at max speed, maintain it
                        if(round(prev_speed) == frame_stats['blob_speed']):
                            self.info['wavebounces'] += 1
                            #createSFXEvent('wavebounce')
            elif(not 'left' in pressed and 'right' in pressed and not self.status_effects['menu']['open']): #If holding right but not left
                self.facing = 'right'
                if(self.x_pos >= 1700): #Are we in danger of going off screen?
                    self.x_speed = 0
                    self.x_pos = 1700
                else:
                    if(abs(self.x_speed) < frame_stats['blob_speed']):
                        if(self.x_speed < 0):
                            self.x_speed += 1.2 * frame_stats['blob_friction'] # Turn around faster by holding left
                        elif(abs(self.x_speed) > frame_stats['blob_speed'] + (frame_stats['blob_friction'] * 2)):
                            self.x_speed -= frame_stats['blob_friction']
                        else:
                            self.x_speed += frame_stats['blob_friction'] # Accelerate based off of friction
                    else:
                        prev_speed = self.x_speed
                        self.x_speed = frame_stats['blob_speed'] #If at max speed, maintain it
                        if(round(prev_speed) == -1 * frame_stats['blob_speed']):
                            self.info['wavebounces'] += 1
                            #createSFXEvent('wavebounce') 
            else: #We're either not holding anything, or pressing both at once
                if(self.x_speed < 0): #If we're going left, decelerate
                    if(self.x_speed + frame_stats['blob_friction']) > 0:
                        self.x_speed = 0 #Ensures that we don't decelerate and start moving backwards
                    else:
                        self.x_speed += frame_stats['blob_friction'] #Normal deceleration
                elif(self.x_speed > 0):
                    if(self.x_speed - frame_stats['blob_friction']) < 0:
                        self.x_speed = 0 #Ensures that we don't decelerate and start moving backwards
                    else:
                        self.x_speed -= frame_stats['blob_friction'] #Normal deceleration

    def apply_wavedash_abilities(self, pressed, frame_stats):
        pass

    def handle_down_press(self, pressed, frame_stats):
        if('down' in pressed):
            self.down_holding_timer += 1
            if(self.y_pos < Blob.ground): #If you are above ground and press down
                self.fastfalling = True #Fast fall, increasing your gravity by 3 stars
            else:
                if(not self.focusing and not self.impact_land_frames and not frame_stats['wavedashed']):
                    self.focusing = True
                    self.focus_lock = self.focus_lock_max
                elif(self.focusing):
                    self.focusing = True
        else:
            self.down_holding_timer = 0

        if((not 'down' in pressed) and self.focus_lock == 0 and self.focusing):
            #True if we're not holding down, focus lock is done and we're focusing
            self.focusing = False

    def calculate_vertical_speed(self, pressed):
        if('up' in pressed and self.y_pos == Blob.ground and not self.status_effects['menu']['open']): #If you press jump while grounded, jump!
            self.y_speed = (-1 * self.jump_force) + (bool(self.status_effects['glued']) * 0.25 * self.jump_force) - (0.75 * bool(self.status_effects['monado_effect'] == "JUMP") * 0.5 * self.jump_force)
            self.focus_lock = 0
            self.wavedash_lock = 0
            self.focusing = False
            self.info['jumps'] += 1
        elif('up' in pressed and self.y_speed < 0):
            self.shorthopping = False
        elif(('up' not in pressed) and self.y_speed < 0):
            self.shorthopping = True

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

    def apply_speed(self, frame_stats):
        if(not self.x_kb):
            self.x_pos += self.x_speed #This ensures that we are always adjusting our position
        else:
            self.x_pos += self.x_kb
            self.x_speed = 0
            if(self.x_kb > 1 and self.y_pos == Blob.ground):
                self.x_kb -= frame_stats['blob_traction']
            elif(self.x_kb > 1 and self.y_pos != Blob.ground):
                self.x_kb -= frame_stats['blob_friction']
            elif(self.x_kb < -1 and self.y_pos == Blob.ground):
                self.x_kb += frame_stats['blob_traction']
            elif(self.x_kb < -1 and self.y_pos != Blob.ground):
                self.x_kb += frame_stats['blob_friction']
            else:
                self.x_kb = 0
        self.info['x_distance_moved'] += abs(self.x_speed)
        self.y_pos += self.y_speed #This ensures that we are always adjusting our position

    def check_boundary_collision(self):
        """
        Handles collisions for floor, ceiling and walls
        Also updates blob x/y center
        """
        # X
        if(self.x_pos <= 0): #Are we in danger of going off screen?
            self.x_speed = 0
            self.x_pos = 0
            self.x_kb /= 2

        if(self.x_pos >= 1700): #Are we in danger of going off screen?
            self.x_speed = 0
            self.x_pos = 1700
            self.x_kb /= 2

        # Y
        if(self.y_pos < Blob.ceiling): #How did we get here?
            self.y_pos = Blob.ceiling
            self.y_speed = 0
        if(self.y_pos > Blob.ground): #Don't go under the floor!
            self.y_speed = 0
            self.y_pos = Blob.ground
            self.impact_land_frames = 10
            self.fastfalling = False
            self.shorthopping = False
            if(self.status_effects['monado_effect'] == "JUMP"):
                create_environmental_modifier(player = self.player, affects = {'enemy', 'ball'}, species = 'spire_glyph', lifetime = 30, y_pos = 700, special_functions = [create_environmental_modifier])
                createSFXEvent('glyph')

        self.x_center = self.x_pos + 83
        self.y_center = self.y_pos + 110

    def handle_special_inputs(self, pressed):
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

    def handle_menu(self, pressed):
        # Special things go last
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

        if('ability' in pressed or 'kick' in pressed or 'block' in pressed or 'boost' in pressed):
            menu_action = 'ability'
        
        self.status_effects['menu']['time'] += 1
        return {"menu_direction": menu_direction, "menu_action": menu_action}

    def move(self, pressed_buttons):
        # Used by all blobs, but it could be refactored for blobs with menus
        pressed = self.convert_inputs(pressed_buttons)
        pressed = self.drop_inputs(pressed)
        frame_stats = self.set_maximum_speeds()

        # Are these interchangeable?
        self.calculate_horizontal_speed(pressed, frame_stats)
        self.calculate_vertical_speed(pressed)
        self.apply_speed(frame_stats)
        if not(self.status_effects['menu']['open']):
            self.handle_down_press(pressed, frame_stats)
            self.apply_wavedash_abilities(pressed, frame_stats)

        # Do this last
        self.check_boundary_collision()

        # Special things go last
        if not(self.status_effects['menu']['open']):
            #print(self.status_effects['menu'])
            self.handle_special_inputs(pressed)
        
        return pressed

    def tutorial_move(self):
        # Can technically be used by all blobs
        pass

    def apply_stat_overrides(self, stat_overrides):
        for key in stat_overrides:
            if stat_overrides[key] is not None:
                if(key == "max_hp"):
                    if(stat_overrides[key] == 1):
                        self.stars[key] = -2.5
                    elif(stat_overrides[key] == 3):
                        self.stars[key] = -1.5
                    else:
                        self.stars[key] = (stat_overrides[key] - 6)//2
                else:
                    self.stars[key] = stat_overrides[key]
                    print(self.stars)
        return self.stars

    def set_base_stats(self, stars, set_hp = True, set_ability = True):
        # Used by all blobs when the Taxation effect is active
        if(set_hp):
            self.max_hp = int(2 * (self.stars['max_hp'] + 3)) # Each star adds an additional HP.
            self.hp = self.max_hp
        self.top_speed = 10+(1*stars['top_speed']) # Each star adds some speed
        self.base_top_speed = self.top_speed # Non-boosted speed
        self.traction = 0.2 + (stars['traction'] * 0.15) # Each star increases traction
        self.friction = 0.2 + (stars['friction'] * 0.15) # Each star increases friction
        self.base_traction = self.traction # Non-boosted
        self.base_friction = self.friction # No boost
        self.gravity_stars = round(.3 + (stars['gravity'] * .15), 3) # Each star increases gravity
        self.gravity_mod = self.gravity_stars * 3 # Fastfalling increases gravity
        self.jump_force = 14.5 + (stars['gravity'] * 2) # Initial velocity is based off of gravity
        self.boost_top_speed = 10+(1*stars['top_speed'] + 3) #This stat is increased by 3 stars
        self.boost_traction = 0.2 + ((stars['traction'] + 5) * 0.15) # These stats are increased by 5 stars
        self.boost_friction = 0.2 + ((stars['friction'] + 5) * 0.15) # These stats are increased by 5 stars

        self.kick_cooldown_max = (300 + 15 * (5 - self.stars['kick_cooldown_rate'])) * Blob.timer_multiplier # Higher stars means lower cooldown
        self.block_cooldown_max = (360 + 15 * (5 - self.stars['block_cooldown_rate'])) * Blob.timer_multiplier # How long the block cooldown lasts
        self.boost_cost = self.stars['boost_cost'] * Blob.nrg_multiplier # How much SA meter must be spent to boost
        self.boost_cooldown_max = (300 + 30 *  (5 - self.stars['boost_cooldown_max'])) * Blob.timer_multiplier # Each star reduces boost cooldown
        self.boost_duration = 60 + (30 * self.stars['boost_duration']) # Each star increases boost duration by half a second
        if(set_ability):
            self.special_ability = self.stars['special_ability'] # Special Ability of a Blob
            self.ability_classification = self.stars['special_ability_category']
            self.special_ability_max = self.stars['special_ability_max'] * Blob.nrg_multiplier # Highest that the SA gauge can go
            self.special_ability_cost = self.stars['special_ability_cost'] * Blob.nrg_multiplier # Price to activate SA
            self.special_ability_maintenance = self.stars['special_ability_maintenance'] * Blob.nrg_multiplier # Price to maintain SA
            self.special_ability_cooldown_max = self.stars['special_ability_cooldown'] * Blob.timer_multiplier
            self.special_ability_duration = self.stars['special_ability_duration']
            self.special_ability_delay = self.stars['special_ability_delay']
        if(self.boost_timer > 0):
            self.top_speed = self.boost_top_speed
            self.traction = self.boost_traction
            self.friction = self.boost_friction

    def get_ability_visuals(self):
        # Used by all blobs
        return self.ability_cooldown_percentage, self.ability_cooldown_visualization

    def get_kick_visuals(self):
        # Used by all blobs
        return self.kick_cooldown_percentage, self.kick_cooldown_visualization

    def get_block_visuals(self):
        # Used by all blobs
        return self.block_cooldown_percentage, self.block_cooldown_visualization

    def get_boost_timer_visuals(self):
        # Used by all blobs
        return self.boost_timer_percentage, self.boost_timer_visualization

    def get_boost_cooldown_visuals(self):
        # Used by all blobs
        return self.boost_cooldown_percentage, self.boost_cooldown_visualization

    def toggle_recharge_indicator(self, indicator, set_indicator = 1):
        # Used by all blobs
        indicator_state = self.recharge_indicators[indicator]
        if indicator_state == 2:
            indicator_state = 1
        elif(indicator_state == 1):
            indicator_state = 0
        else:
            indicator_state = set_indicator
        self.recharge_indicators[indicator] = indicator_state

    def __str__(self):
        # Used by all blobs
        return f"Player {self.player}: {self.species}."

    def return_stars(self):
        # Used by all blobs
        return self.stars

    def return_sprite_paths(self):
        blob_cwd = '/resources/images/blobs/'
        ability_cwd = "/resources/images/ability_icons/"
        #print(self.init_json)
        blob_cwd = f'blobs/{self.init_json["descriptors"]["path"]}/'
        #icon_cwd = "/resources/images/ui_icons/"
        path_dict = {}
        for key, value in self.init_json["costumes"].items():
            path_dict[int(key)] = {}
            for sprite_id, sprite_path in value.items():
                if sprite_id != "ability":
                    path_dict[int(key)][sprite_id] = blob_cwd + sprite_path
                else:
                    path_dict[int(key)][sprite_id] = blob_cwd + sprite_path
        '''path_dict = { # Dictionary of tuples. Key is costume ID. Tuple[0] is basic alive sprite. Tuple[1] is basic dead sprite. Can fit more sprites as necessary.
            0: {
                "alive": blob_cwd + "quirkless_blob.png", 
                "dead": blob_cwd + "quirkless_blob_-1.png",
                "ability": icon_cwd + "boost_icon.png",
            },
            1: {
                "alive": blob_cwd + "quirkless_blob_1.png", 
                "dead": blob_cwd + "quirkless_blob_-1.png", 
                "ability": icon_cwd + "boost_icon.png",
            },
            2: {
                "alive": blob_cwd + "shadow_blob.png", 
                "dead": blob_cwd + "quirkless_blob_-1.png", 
                "ability": icon_cwd + "boost_icon.png",
            }
        }'''
        return path_dict

    def initialize_blob_sprites(self):

        # Steps for initialization
        # Get blob costume to identify which sprites to load in
        # Load in the sprites
        # Apply Clone Filter as necessary
        # Keep track of clones somehow
        # Load in ability icons

        
        temp_dict = {}
        path_dict = self.return_sprite_paths()
        #print(path_dict)
        for sprite_path in path_dict[self.costume]:
            temp_dict[sprite_path] = pg.image.load(path_dict[self.costume][sprite_path]).convert_alpha()
            #print(sprite_path)
        blob_height = round(temp_dict['alive'].get_height() * 0.6)
        self.blob_images['blob_left'] = pg.transform.scale(temp_dict['alive'].convert_alpha(), (120, blob_height))
        self.blob_images['blob_right'] = pg.transform.flip(self.blob_images['blob_left'], True, False)
        self.blob_images['dead_left'] = pg.transform.scale(temp_dict['dead'].convert_alpha(), (120, blob_height))
        self.blob_images['dead_right'] = pg.transform.flip(self.blob_images['dead_left'], True, False)
        self.blob_images['damage_left'] = self.blob_images['blob_left'].copy()
        self.blob_images['damage_left'].set_alpha(100)
        self.blob_images['damage_right'] = self.blob_images['blob_right'].copy()
        self.blob_images['damage_right'].set_alpha(100)
        sprite_tuple = (self.species, self.costume)
        if(sprite_tuple in self.sprite_collisions):
            print(self.sprite_collisions)
            match self.sprite_collisions[sprite_tuple]:
                case 1:
                    self.blob_images['blob_left'].fill((150, 150, 150, 255), special_flags=pg.BLEND_RGBA_MULT)
                    self.blob_images['blob_right'].fill((150, 150, 150, 255), special_flags=pg.BLEND_RGBA_MULT)
                    self.blob_images['damage_left'].fill((150, 150, 150, 255), special_flags=pg.BLEND_RGBA_MULT)
                    self.blob_images['damage_right'].fill((150, 150, 150, 255), special_flags=pg.BLEND_RGBA_MULT)
                case 2:
                    self.blob_images['blob_left'].fill((255, 255, 255, 255), special_flags=pg.BLEND_RGBA_MULT)
                    self.blob_images['blob_right'].fill((255, 255, 255, 255), special_flags=pg.BLEND_RGBA_MULT)
                    self.blob_images['damage_left'].fill((255, 255, 255, 255), special_flags=pg.BLEND_RGBA_MULT)
                    self.blob_images['damage_right'].fill((255, 255, 255, 255), special_flags=pg.BLEND_RGBA_MULT)
                case 3:
                    self.blob_images['blob_left'].fill((100, 100, 100, 255), special_flags=pg.BLEND_RGBA_MULT)
                    self.blob_images['blob_right'].fill((100, 100, 100, 255), special_flags=pg.BLEND_RGBA_MULT)
                    self.blob_images['damage_left'].fill((100, 100, 100, 255), special_flags=pg.BLEND_RGBA_MULT)
                    self.blob_images['damage_right'].fill((100, 100, 100, 255), special_flags=pg.BLEND_RGBA_MULT)
            self.sprite_collisions[sprite_tuple] += 1
        else:
            self.sprite_collisions[sprite_tuple] = 1

        self.ability_icons['default'] = pg.transform.scale(temp_dict['ability'].convert_alpha(), (70, 70))
        return temp_dict

    def draw(self, game_display):
        # Separate Chunk        
        #pname = "p" + str(self.player) + "_"
        #if self.recharge_indicators['ability_swap_b']:
        #    try:
        #        self.blob_images[pname + 'ability_icon'] = pg.transform.scale(pg.image.load(self.ability_icon).convert_alpha(), (70, 70))
        #    except:
        #        self.blob_images[pname + 'ability_icon'] = pg.transform.scale(pg.image.load("/resources/images/ui_icons/404.png").convert_alpha(), (70, 70))
        #    self.blob_images['ui_initialized'] = False
        #
        #if not (blob.image == self.blob_images['blob_clone']):
        #    blob_height = round(pg.image.load(blob.image).get_height()*0.6)
        #    self.blob_images['blob'] = pg.transform.scale(pg.image.load(blob.image).convert_alpha(), (120, blob_height))
        #    self.blob_images['blob_clone'] = blob.image
        # Tuple structure: Direction facing ("left", "right"), Blob Status (0 is normal, 1 is hurt, 2 is dead)
        sprite_dict = {
            ("right", 0): self.blob_images["blob_right"],
            ("left", 0): self.blob_images["blob_left"],
            ("right", 1): self.blob_images["damage_right"],
            ("left", 1): self.blob_images["damage_left"],
            ("right", 2): self.blob_images["dead_right"],
            ("left", 2): self.blob_images["dead_left"],
        }
        blob_status = 2 if self.hp <= 0 else 1 if (self.damage_flash_timer//10) % 2 == 1 else 0
        blob_image = sprite_dict[(self.facing, blob_status)]
        
        blob_y_pos = self.y_pos - (blob_image.get_height() - 66)
        game_display.blit(blob_image, (self.x_pos*(1000/1366), (blob_y_pos*(400/768))))

        #draw_blob_special(blob, game_display)
        #draw_blob_particles(game_display, blobs.values()) # TODO: Fix this!

        if(self.status_effects['menu']['open']):
            self.draw_menu(game_display)
    
    def draw_menu(self, game_display):
        pass

    def create_blob_sfx(sfx):
        createSFXEvent(sfx)