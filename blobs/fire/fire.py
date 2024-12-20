from engine.blobs.blobs import Blob
import random
from json import loads, dumps

class Fire(Blob):
    default_stats = {"hp": 8}
    def __init__(self, x_pos = 50, y_pos = 1200, facing = 'left', player = 1, 
    special_ability_charge_base = 1, costume = 0, danger_zone_enabled = True, is_cpu = False, stat_overrides = [], match_state = None):
        super().__init__(x_pos, y_pos, facing, player, special_ability_charge_base, costume, 
        danger_zone_enabled, is_cpu, stat_overrides, match_state, __file__)
        self.species = "fire"
        self.load_init_blob(__file__)

    def calculate_damage(self, damage):
        return damage - bool(self.status_effects['reflecting'] > 0) + bool(self.status_effects['monado_effect'] == "SPEED") # Damage is reduced by 1 if we are reflecting
        # Damage is increased by 1 if we are using Hot Sauce
    

    def apply_boost_kick_effect(self, blob):
        blob.apply_status_effect(effect = "overheat", duration = 300)
    
    def cooldown(self):
        super().cooldown()
        if(self.special_ability_timer > 0 and self.ability_holding_timer % 18 == 17):
            Blob.create_blob_sfx('fire')

    def ability(self):
        if('fireball' in self.used_ability and self.special_ability_meter > self.special_ability_maintenance):
            #If we were holding down the button before
            self.used_ability["fireball"] += 1
            self.special_ability_timer = self.special_ability_cooldown #Set the cooldown between uses timer
            self.special_ability_meter -= self.special_ability_maintenance #Remove some SA meter
            self.ability_holding_timer += 1
            if(self.ability_holding_timer % 45 == 0):
                self.apply_status_effect("monado_effect", duration = "SPEED", method = "set")
                self.apply_status_effect("monado_timer", duration = 300)
        elif(self.special_ability_meter > self.special_ability_cost):
            #If we ignite the ball
            self.used_ability["fireball"] = 1
            self.special_ability_timer = self.special_ability_cooldown_max #Set the cooldown between uses timer
            self.special_ability_meter -= self.special_ability_cost #Remove some SA meter
            self.ability_holding_timer = 0
            Blob.create_blob_sfx('fire')
