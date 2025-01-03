from engine.blobs.blobs import Blob
import random
from engine.environmental_modifiers import create_environmental_modifier
class Arcade(Blob):
    default_stats = {"hp": 8}
    def __init__(self, x_pos = 50, y_pos = 1200, facing = 'left', player = 1, 
    special_ability_charge_base = 1, costume = 0, danger_zone_enabled = True, is_cpu = False, stat_overrides = [], match_state = None):
        super().__init__(x_pos, y_pos, facing, player, special_ability_charge_base, costume, 
        danger_zone_enabled, is_cpu, stat_overrides, match_state, __file__)
        self.species = "arcade"
        self.load_init_blob(__file__)

    def ability(self):
        if(self.special_ability_meter >= self.special_ability_cost and self.special_ability_cooldown <= 0):
            #Spire activation
            Blob.create_blob_sfx('glyph')
            #self.used_ability = "spire_wait"
            self.special_ability_cooldown = self.special_ability_cooldown_max
            self.special_ability_meter -= self.special_ability_cost #Remove some SA meter
            if(self.facing == 'left'):
                x_mod = -1
            else:
                x_mod = 1
            create_environmental_modifier(self.player, affects = {'self'}, species = 'cartridge', lifetime = 600, hp = 1, x_pos = self.x_center, y_pos = self.y_center - 10, x_speed = (3*self.x_speed/4) + (4*x_mod), y_speed = (self.y_speed/2) - 12, gravity = 0.4, random_image = self.status_effects['teleporter'][0])
            self.status_effects['teleporter'][0] += 1
            if(self.status_effects['teleporter'][0]) > 3:
                self.status_effects['teleporter'][0] = 1
    
    def apply_boost_kick_effect(self, blob):
        if not blob.block_timer and not blob.kick_timer:
            create_environmental_modifier(blob.player, affects = {'self'}, species = 'console', lifetime = 360, hp = 1, x_pos = self.x_center, y_pos = self.y_center - 20, gravity = 0.5)
            
    def reset(self):
        super().reset()