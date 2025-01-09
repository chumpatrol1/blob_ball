from engine.blobs.blobs import Blob
import random
from json import loads, dumps

class Fisher(Blob):
    default_stats = {"hp": 8}
    species = "fisher"
    def __init__(self, x_pos = 50, y_pos = 1200, facing = 'left', player = 1, 
    special_ability_charge_base = 1, costume = 0, danger_zone_enabled = True, is_cpu = False, stat_overrides = [], match_state = None):
        super().__init__(x_pos, y_pos, facing, player, special_ability_charge_base, costume, 
        danger_zone_enabled, is_cpu, stat_overrides, match_state, __file__)
        self.load_init_blob(__file__)
    
    def calculate_damage(self, damage):
        return damage - bool(self.status_effects['reflecting'] > 0) + bool("hook" in self.used_ability and self.used_ability["hook"]) # Damage is reduced by 1 if we are reflecting
    
    def handle_post_damage(self, source=None):
        super().handle_post_damage(source)
        # Used for Mirror Blob's reflect, etc.
        if("hook" in self.used_ability and self.used_ability["hook"]):
            self.apply_status_effect("silenced", 360, 600, "add")

    def ability(self):
        if('hook' in self.used_ability and self.special_ability_meter > self.special_ability_maintenance):
            #If we were holding down the button before
            self.used_ability["hook"] += 1
            self.special_ability_timer = self.special_ability_cooldown #Set the cooldown between uses timer
            self.special_ability_meter -= self.special_ability_maintenance #Remove some SA meter
            self.ability_holding_timer += 1
        elif(self.special_ability_meter > self.special_ability_cost):
            #If we ignite the ball
            self.used_ability["hook"] = 1
            self.special_ability_timer = self.special_ability_cooldown_max #Set the cooldown between uses timer
            self.special_ability_meter -= self.special_ability_cost #Remove some SA meter
            self.ability_holding_timer = 0