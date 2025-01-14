from engine.blobs.blobs import Blob
import random
from json import loads, dumps

class Water(Blob):
    default_stats = {"hp": 8}
    species = "water"
    def __init__(self, x_pos = 50, y_pos = 1200, facing = 'left', player = 1, 
    special_ability_charge_base = 1, costume = 0, danger_zone_enabled = True, is_cpu = False, stat_overrides = [], match_state = None):
        super().__init__(x_pos, y_pos, facing, player, special_ability_charge_base, costume, 
        danger_zone_enabled, is_cpu, stat_overrides, match_state, __file__)
        self.load_init_blob(__file__)

    def apply_boost_kick_effect(self, blob):
        #blob.apply_status_effect(effect = "hypothermia", duration = 180)
        pass
    
    def cooldown(self):
        super().cooldown()
        if(self.special_ability_timer > 0 and self.ability_holding_timer % 20 == 19):
            Blob.create_blob_sfx('water')

    def ability(self):
        if('geyser' in self.used_ability and self.special_ability_meter > self.special_ability_maintenance):
            #If we were holding down the button before
            self.used_ability["geyser"] += 1
            self.special_ability_timer = self.special_ability_cooldown #Set the cooldown between uses timer
            self.special_ability_meter -= self.special_ability_maintenance #Remove some SA meter
            self.ability_holding_timer += 1

        elif(self.special_ability_meter > self.special_ability_cost):
            #If we ignite the ball
            self.used_ability["geyser"] = 1
            self.special_ability_timer = self.special_ability_cooldown_max #Set the cooldown between uses timer
            self.special_ability_meter -= self.special_ability_cost #Remove some SA meter
            self.ability_holding_timer = 0
            Blob.create_blob_sfx('water')
