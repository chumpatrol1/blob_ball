from engine.blobs.blobs import Blob
import random
from engine.environmental_modifiers import create_environmental_modifier
class Boxer(Blob):
    default_stats = {"hp": 8}
    def __init__(self, x_pos = 50, y_pos = 1200, facing = 'left', player = 1, 
    special_ability_charge_base = 1, costume = 0, danger_zone_enabled = True, is_cpu = False, stat_overrides = [], match_state = None):
        super().__init__(x_pos, y_pos, facing, player, special_ability_charge_base, costume, 
        danger_zone_enabled, is_cpu, stat_overrides, match_state, __file__)
        self.species = "boxer"
        self.load_init_blob(__file__)

    def ability(self):
        if(self.special_ability_meter >= self.special_ability_cost and self.special_ability_cooldown <= 0):
                #self.used_ability = "starpunch_wait"
                self.special_ability_cooldown = self.special_ability_cooldown_max
                self.special_ability_timer = self.special_ability_cooldown
                self.special_ability_meter -= self.special_ability_cost
                #self.kick_cooldown += 120
                create_environmental_modifier(player = self.player, affects = {'enemy'}, species = 'starpunch_wait', lifetime = self.special_ability_delay, y_pos = self.y_center, special_functions = [create_environmental_modifier])
                Blob.create_blob_sfx('boxing_bell')

    def apply_boost_kick_effect(self, blob):
        self.special_ability_cooldown -= 120 * Blob.timer_multiplier
        if(self.special_ability_cooldown < 0):
            self.special_ability_cooldown = 0
    
    def reset(self):
        super().reset()