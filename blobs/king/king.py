from engine.blobs.blobs import Blob
import random
from engine.environmental_modifiers import create_environmental_modifier
class King(Blob):
    default_stats = {"hp": 8}
    def __init__(self, x_pos = 50, y_pos = 1200, facing = 'left', player = 1, 
    special_ability_charge_base = 1, costume = 0, danger_zone_enabled = True, is_cpu = False, stat_overrides = [], match_state = None):
        super().__init__(x_pos, y_pos, facing, player, special_ability_charge_base, costume, 
        danger_zone_enabled, is_cpu, stat_overrides, match_state, __file__)
        self.species = "king"
        self.load_init_blob(__file__)

    def ability(self):
        if(self.special_ability_meter >= self.special_ability_cost and self.special_ability_cooldown <= 0):
            self.used_ability["tax"] = 2
            self.special_ability_cooldown = self.special_ability_cooldown_max
            self.special_ability_timer = self.special_ability_cooldown
            self.special_ability_meter -= self.special_ability_cost
            skc = bool(self.kick_cooldown > 0)
            slc = bool(self.block_cooldown > 0)
            sbc = bool(self.boost_cooldown_timer > 0)
            self.kick_cooldown -= 30 * Blob.timer_multiplier
            self.block_cooldown -= 30 * Blob.timer_multiplier
            if(self.boost_cooldown_timer > 0):
                self.boost_cooldown_timer -= 30 * Blob.timer_multiplier
            self.check_cooldown_completion(updatedKick=skc, updatedBlock=slc, updatedBoost=sbc)

            Blob.create_blob_sfx('chime_progress')
        else:
            return

    def apply_boost_kick_effect(self, blob):
        if not blob.block_timer and not blob.kick_timer:
            create_environmental_modifier(blob.player, affects = {'self'}, species = 'royal_loan', lifetime = 360, hp = 0, x_pos = self.x_center - 20, y_pos = self.y_center - 150, gravity = 0, random_image=self.player)
    
    def reset(self):
        super().reset()