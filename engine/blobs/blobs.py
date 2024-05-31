#from resources.sound_engine.sfx_event import createSFXEvent
#from engine.blob_stats import species_to_stars
import pygame as pg
from json import loads

default_stars = { #Gets many values for each blob
    'max_hp': 3,
    'top_speed': 3,
    'traction': 3,
    'friction': 3,
    'gravity': 3,
    'kick_cooldown_rate': 3,
    'block_cooldown_rate': 3,
    'boost_cost': 3,
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

class Blob:
    ground = 1200
    ceiling = 200
    timer_multiplier = 2
    nrg_multiplier = 5
    all_blobs = {}
    sprite_collisions = {}

    def __init__(self, x_pos = 50, y_pos = 1200, facing = 'left', player = 1, 
    special_ability_charge_base = 1, costume = 0, danger_zone_enabled = True, is_cpu = False, stat_overrides = [], match_state = None, init_blob_path = __file__):
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
        self.set_base_stats(self.stars)

        self.down_holding_timer = 0
        self.focus_lock = 0 #Timer that locks movement when a blob is focusing
        self.focus_lock_max = 60
        self.focusing = False
        self.impact_land_frames = 0 #Locks the player from focusing after landing (fastfall leniency)

        self.special_ability_charge = 1 * Blob.nrg_multiplier #Charge rate. Each frame increases the SA meter by 1 point, or more if focusing
        self.special_ability_meter = 0 #Amount of SA charge stored up
        self.special_ability_timer = 0 #Timer that counts down between uses of an SA
        self.special_ability_duration = 0 #Time that a SA is active
        self.special_ability_cooldown = 0 #Cooldown between uses
        self.special_ability_charge_base = special_ability_charge_base * Blob.nrg_multiplier
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
        # TODO: Add image initialization
        self.initialize_blob_sprites()

    def load_init_blob(self, blob_path=""):
        init_path = blob_path.rsplit("\\", 1)
        print(init_path)
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
                    "boost_cost": 3,
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
        print(init_file)
        return loads(init_file)
        
    def cooldown(self):
        # Used by all blobs
        pass

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
        self.ability_icon = icon
        self.recharge_indicators['ability_swap'] = True

    def ability(self):
        # Used by all blobs
        pass

    def kick(self, ignore_cooldown = False):
        # Used by all blobs. Merchant and Joker blobs have notable variants
        # Boost kicks?
        if(self.kick_cooldown <= 0 or ignore_cooldown):
            #createSFXEvent('kick')
            self.block_cooldown += 5 * (self.block_cooldown_rate)
            self.kick_timer = 2
            self.kick_cooldown = self.kick_cooldown_max
            #self.collision_timer = 0
            self.collision_distance = 175
            self.kick_visualization = self.kick_visualization_max
            self.info['kick_count'] += 1

    def block(self):
        # Used by all blobs. Merchant and Joker blobs have notable variants
        if(self.block_cooldown <= 0):
            #createSFXEvent('block')
            self.kick_cooldown += 5 * (self.kick_cooldown_rate)
            self.block_cooldown = self.block_cooldown_max #Set block cooldown
            self.block_timer = self.block_timer_max #Set active block timer
            self.movement_lock = 30
            self.x_speed = 0
            if(self.y_speed < 0): #If we are moving upwards, halt your momentum!
                self.y_speed = 0
            self.info['block_count'] += 1

    def boost(self):
        # Used by all blobs
        pass

    def check_blob_collision(self):
        # Used by all blobs
        pass

    def check_ability_collision(self, blob):
        # Used by all blobs
        pass

    def check_environmental_collisions(self, environment):
        # Used by all blobs, but it could be refactored
        pass

    def take_damage(self):
        # Used by all blobs, but it could be refactored
        pass

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
        pass

    def reset(self):
        # Used by all blobs, but it could be refactored
        pass

    def cpu_logic(self):
        # Used by all blobs, but each blob would have a different version
        pass

    def move(self, pressed):
        # Used by all blobs, but it could be refactored for blobs with menus
        return pressed

    def tutorial_move(self):
        # Can technically be used by all blobs
        pass

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
        pass

    def get_kick_visuals(self):
        # Used by all blobs
        pass

    def get_block_visuals(self):
        # Used by all blobs
        pass

    def get_boost_timer_visuals(self):
        # Used by all blobs
        pass

    def get_boost_cooldown_visuals(self):
        # Used by all blobs
        pass

    def toggle_recharge_indicator(self):
        # Used by all blobs
        pass

    def __str__(self):
        # Used by all blobs
        pass

    def return_stars(self):
        # Used by all blobs
        pass

    def return_sprite_paths(self):
        blob_cwd = '/resources/images/blobs/'
        ability_cwd = "/resources/images/ability_icons/"
        print(self.init_json)
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
        print(path_dict)
        for sprite_path in path_dict[self.costume]:
            temp_dict[sprite_path] = pg.image.load(path_dict[self.costume][sprite_path]).convert_alpha()
            print(sprite_path)
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
        blob_image = self.blob_images['blob_right']
        blob_y_pos = self.y_pos - (self.blob_images['blob_right'].get_height() - 66)
        #if not("invisible" in blob.image):
        #    if(self.facing == "right"):
        #        if(self.hp > 0):
        #            game_display.blit(self.blob_images['blob_right'], (self.x_pos*(1000/1366), (blob_y_pos*(400/768))))
        #        else:
        #            game_display.blit(self.blob_images['dead_right'], (self.x_pos*(1000/1366), (blob_y_pos*(400/768))))
        #    else:
        #        if(self.hp > 0):
        #            game_display.blit(self.blob_images['blob_left'], (self.x_pos*(1000/1366), (blob_y_pos*(400/768))))
        #        else:
        #            game_display.blit(self.blob_images['dead_left'], (self.x_pos*(1000/1366), (blob_y_pos*(400/768))))
        #else:
        #    if(self.facing == "right"):
        #        game_display.blit(self.blob_images['damage_right'], (self.x_pos*(1000/1366), (blob_y_pos*(400/768))))
        #    else:
        #        game_display.blit(self.blob_images['damage_left'], (self.x_pos*(1000/1366), (blob_y_pos*(400/768))))
        game_display.blit(blob_image, (self.x_pos*(1000/1366), (blob_y_pos*(400/768))))

        #draw_blob_special(blob, game_display)
        #draw_blob_particles(game_display, blobs.values()) # TODO: Fix this!

        #if(self.status_effects['menu']['open']):
        #    draw_menu(game_display, self)
