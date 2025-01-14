from engine.blobs.blobs import Blob
import random
from engine.environmental_modifiers import create_environmental_modifier
import pygame as pg
class Doctor(Blob):
    default_stats = {"hp": 8}
    species = "doctor"
    def __init__(self, x_pos = 50, y_pos = 1200, facing = 'left', player = 1, 
    special_ability_charge_base = 1, costume = 0, danger_zone_enabled = True, is_cpu = False, stat_overrides = [], match_state = None):
        super().__init__(x_pos, y_pos, facing, player, special_ability_charge_base, costume, 
        danger_zone_enabled, is_cpu, stat_overrides, match_state, __file__)
        self.load_init_blob(__file__)
        random_number = random.randint(0,1)
        if(random_number):
            self.status_effects['pill'] = 'pill_boost'
            self.update_ability_icon('pill_boost')
        else:
            self.status_effects['pill'] = 'pill_cooldown'
            self.update_ability_icon('pill_cooldown')

    def ability(self):
        if(self.special_ability_meter >= self.special_ability_cost and self.special_ability_cooldown <= 0):
                self.used_ability["pill"] = 1
                #self.used_ability = "starpunch_wait"
                self.special_ability_cooldown = self.special_ability_cooldown_max
                self.special_ability_timer = self.special_ability_cooldown
                self.special_ability_meter -= self.special_ability_cost
                #self.kick_cooldown += 120
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
                    self.add_boost(180)

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
                
                #print("~~~~~~~~~~~~~~~~~~~~~~~~~~")

                self.update_ability_icon(self.status_effects['pill'])
                Blob.create_blob_sfx('crunch')
        else:
            return

    def apply_boost_kick_effect(self, blob):
        pass

    def reset(self):
        super().reset()
    
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

        self.ability_icons['pill_boost'] = pg.transform.scale(temp_dict['ability_1'].convert_alpha(), (70, 70))
        self.ability_icons['pill_cooldown'] = pg.transform.scale(temp_dict['ability_2'].convert_alpha(), (70, 70))
        self.ability_icons['pill_heal'] = pg.transform.scale(temp_dict['ability_3'].convert_alpha(), (70, 70))

    