from engine.blobs.blobs import Blob
import random
from engine.environmental_modifiers import create_environmental_modifier
class Mirror(Blob):
    default_stats = {"hp": 8}
    def __init__(self, x_pos = 50, y_pos = 1200, facing = 'left', player = 1, 
    special_ability_charge_base = 1, costume = 0, danger_zone_enabled = True, is_cpu = False, stat_overrides = [], match_state = None):
        super().__init__(x_pos, y_pos, facing, player, special_ability_charge_base, costume, 
        danger_zone_enabled, is_cpu, stat_overrides, match_state, __file__)
        self.species = "mirror"
        self.load_init_blob(__file__)

    def ability(self):
        if(self.special_ability_meter >= self.special_ability_cost and self.special_ability_cooldown <= 0):
            self.used_ability["mirror"] = 2
            self.apply_status_effect("reflecting", duration = self.special_ability_duration)
            self.special_ability_cooldown = self.special_ability_cooldown_max
            self.special_ability_meter -= self.special_ability_cost
            self.kick_cooldown += 60 * Blob.timer_multiplier
            self.block_cooldown += 60 * Blob.timer_multiplier
            self.boost_cooldown_timer += 60 * Blob.timer_multiplier
            Blob.create_blob_sfx('chime_progress')

    def reset(self):
        super().reset()
        self.special_ability_cooldown = self.boost_cooldown_timer