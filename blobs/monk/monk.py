from engine.blobs.blobs import Blob
import random
from engine.environmental_modifiers import create_environmental_modifier
from copy import copy
from resources.graphics_engine.display_particles import draw_monk_upgrade_pfx
class Monk(Blob):
    default_stats = {"hp": 8}
    species = "monk"
    def __init__(self, x_pos = 50, y_pos = 1200, facing = 'left', player = 1, 
    special_ability_charge_base = 1, costume = 0, danger_zone_enabled = True, is_cpu = False, stat_overrides = [], match_state = None):
        super().__init__(x_pos, y_pos, facing, player, special_ability_charge_base, costume, 
        danger_zone_enabled, is_cpu, stat_overrides, match_state, __file__)
        self.upgrade_level = 0
        self.sprites_initialized = False
        self.sprite_dict = {}
        self.lv7_timer = 0
        self.load_init_blob(__file__)
    
    def cooldown(self):
        super().cooldown()
        if(self.lv7_timer):
            self.lv7_timer -= 1
            if(not self.lv7_timer):
                self.upgrade_level = 6

    def calculate_monk_stats(self):
        true_stars = copy(self.return_stars())
        true_stars['top_speed'] += self.upgrade_level
        true_stars['traction'] += self.upgrade_level
        true_stars['friction'] += self.upgrade_level
        return true_stars

    def ability(self):
        if(self.special_ability_meter >= self.special_ability_cost and self.special_ability_cooldown <= 0):
            
            # Upgrade the character's stats
            self.special_ability_cooldown = self.special_ability_cooldown_max
            self.special_ability_timer = self.special_ability_cooldown
            self.special_ability_meter -= self.special_ability_cost
            self.upgrade_level += 1
            if(self.upgrade_level >= 7):
                self.upgrade_level = 7 # This ensures that we don't open the forbidden 8th gate
                self.lv7_timer = 180
            true_stars = self.calculate_monk_stats()
            self.set_base_stats(true_stars, set_hp=False)

            # Shoot a hadoukatamari. The power of this projectile varies based on the upgrade level - it applies increasing levels of overheat, and at levels A, S and X it does 1 damage
            if(self.facing == 'left'):
                x_mod = -1
            else:
                x_mod = 1
            create_environmental_modifier(self.player, affects = {'enemy'}, species = 'hadoukatamari', hp = 0 if self.upgrade_level < 5 else 1, x_pos = self.x_center, y_pos = self.y_center - 10, x_speed = (3*self.x_speed/4) + (6*x_mod), gravity = self.upgrade_level * 30, lifetime = 600, special_functions = [create_environmental_modifier])
            draw_monk_upgrade_pfx([self.x_pos, self.y_pos], self.upgrade_level)
            Blob.create_blob_sfx('hadoukatamari')
        else:
            return

    def apply_boost_kick_effect(self, blob):
        return -30 - (5 * (blob.gravity_mod - 1.05))
            
    
    def check_blob_collision_default(self, blob):
        hit_dict = super().check_blob_collision_default(blob)
        if(self.boost_timer > 0):
            hit_dict["y_speed_mod"] = self.apply_boost_kick_effect(blob)
        return hit_dict
    

    def initialize_blob_sprites(self):
        temp_dict = super().initialize_blob_sprites()
        blob_height = round(temp_dict['alive'].get_height() * 0.6)
        import pygame as pg
        # gotta loop through this - I'm not stupid
        sprite_tuple = (self.species, self.costume)
        for costume_id in ('lv1', 'lv2', 'lv3', 'lv4', 'lv5', 'lv6', 'lv7'):
            self.blob_images[f'{costume_id}_left'] = pg.transform.scale(temp_dict[f'{costume_id}'].convert_alpha(), (120, blob_height))
            self.blob_images[f'{costume_id}_right'] = pg.transform.flip(self.blob_images[f'{costume_id}_left'], True, False)
            self.blob_images[f'{costume_id}_damage_left'] = self.blob_images[f'{costume_id}_left'].copy()
            self.blob_images[f'{costume_id}_damage_left'].set_alpha(100)
            self.blob_images[f'{costume_id}_damage_right'] = self.blob_images[f'{costume_id}_right'].copy()
            self.blob_images[f'{costume_id}_damage_right'].set_alpha(100)
        
            if(sprite_tuple in self.sprite_collisions):
                match self.sprite_collisions[sprite_tuple]:
                    case 2:
                        self.blob_images[f'{costume_id}_left'].fill((150, 150, 150, 255), special_flags=pg.BLEND_RGBA_MULT)
                        self.blob_images[f'{costume_id}_right'].fill((150, 150, 150, 255), special_flags=pg.BLEND_RGBA_MULT)
                        self.blob_images[f'{costume_id}_damage_left'].fill((150, 150, 150, 255), special_flags=pg.BLEND_RGBA_MULT)
                        self.blob_images[f'{costume_id}_damage_right'].fill((150, 150, 150, 255), special_flags=pg.BLEND_RGBA_MULT)
                    case 3:
                        self.blob_images[f'{costume_id}_left'].fill((255, 255, 255, 255), special_flags=pg.BLEND_RGBA_MULT)
                        self.blob_images[f'{costume_id}_right'].fill((255, 255, 255, 255), special_flags=pg.BLEND_RGBA_MULT)
                        self.blob_images[f'{costume_id}_damage_left'].fill((255, 255, 255, 255), special_flags=pg.BLEND_RGBA_MULT)
                        self.blob_images[f'{costume_id}_damage_right'].fill((255, 255, 255, 255), special_flags=pg.BLEND_RGBA_MULT)
                    case 4:
                        self.blob_images[f'{costume_id}_left'].fill((100, 100, 100, 255), special_flags=pg.BLEND_RGBA_MULT)
                        self.blob_images[f'{costume_id}_right'].fill((100, 100, 100, 255), special_flags=pg.BLEND_RGBA_MULT)
                        self.blob_images[f'{costume_id}_damage_left'].fill((100, 100, 100, 255), special_flags=pg.BLEND_RGBA_MULT)
                        self.blob_images[f'{costume_id}_damage_right'].fill((100, 100, 100, 255), special_flags=pg.BLEND_RGBA_MULT)

    def build_sprite_dict(self):
        self.sprite_dict = {
            ("right", 0, 0): self.blob_images["blob_right"],
            ("left", 0, 0): self.blob_images["blob_left"],
            ("right", 1, 0): self.blob_images["damage_right"],
            ("left", 1, 0): self.blob_images["damage_left"],
            ("right", 2, 0): self.blob_images["dead_right"],
            ("left", 2, 0): self.blob_images["dead_left"],
        }

        for costume_id in range(1, 8):
            self.sprite_dict[("right", 0, costume_id)] = self.blob_images[f'lv{costume_id}_right'] 
            self.sprite_dict[("left", 0, costume_id)] = self.blob_images[f'lv{costume_id}_left']
            self.sprite_dict[("right", 1, costume_id)] = self.blob_images[f'lv{costume_id}_damage_right'] 
            self.sprite_dict[("left", 1, costume_id)] = self.blob_images[f'lv{costume_id}_damage_left'] 
            self.sprite_dict[("right", 2, costume_id)] = self.blob_images[f'dead_right'] 
            self.sprite_dict[("left", 2, costume_id)] = self.blob_images[f'dead_left'] 

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
        
        if not(self.sprites_initialized):
            self.build_sprite_dict()

        blob_status = 2 if self.hp <= 0 else 1 if (self.damage_flash_timer//10) % 2 == 1 else 0
        blob_image = self.sprite_dict[(self.facing, blob_status, self.upgrade_level)]
        
        blob_y_pos = self.y_pos - (blob_image.get_height() - 66)
        game_display.blit(blob_image, (self.x_pos*(1000/1366), (blob_y_pos*(400/768))))

    def reset(self):
        super().reset()
        self.set_base_stats(self.calculate_monk_stats(), set_hp = False)
    
    def blob_ko(self):
        super().blob_ko()
        self.upgrade_level = 0