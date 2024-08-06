from engine.blobs.blobs import Blob
import random
from json import loads, dumps

class Wind(Blob):
    default_stats = {"hp": 8}
    def __init__(self, x_pos = 50, y_pos = 1200, facing = 'left', player = 1, 
    special_ability_charge_base = 1, costume = 0, danger_zone_enabled = True, is_cpu = False, stat_overrides = [], match_state = None):
        super().__init__(x_pos, y_pos, facing, player, special_ability_charge_base, costume, 
        danger_zone_enabled, is_cpu, stat_overrides, match_state, __file__)
        self.species = "wind"
        self.load_init_blob(__file__)

    def apply_boost_kick_effect(self, blob):
        #blob.apply_status_effect(effect = "overheat", duration = 300)
        if(self.x_pos < blob.x_pos):
            x_speed_mod = 40
        elif(self.x_pos > blob.x_pos):
            x_speed_mod = -40
        elif(self.x_pos < 902):
            x_speed_mod = 40
        else:
            x_speed_mod = -40
        return x_speed_mod
        #blob.take_damage(damage = 0, unblockable = True, unclankable = True, damage_flash_timer = 0, y_speed_mod = 0, x_speed_mod = x_speed_mod,\
        #show_parry = False, status_effects = [], pierce = 0)
    def check_blob_collision_default(self, blob):
        hit_dict = {
            "accumulated_damage": 0,
            "status_effects": [],
            "pierce": 0,
            "x_speed_mod": 0,
            "hit_registered": False
        }
        if(self.x_center - (1.5 * self.collision_distance) <= blob.x_center <= self.x_center + (1.5 * self.collision_distance)):
            if(self.y_center - (1.1 * self.collision_distance) <= blob.y_center <= self.y_center + (self.collision_distance)):
                hit_dict["hit_registered"] = True
                hit_dict["accumulated_damage"] = 2
                hit_dict["pierce"] = 0
                hit_dict["x_speed_mod"] = 0
                if(self.boost_timer > 0):  # Take additional damage if the enemy is boosting
                    hit_dict["accumulated_damage"] += 1
                    hit_dict["x_speed_mod"] = self.apply_boost_kick_effect(blob)
                if(((blob.player == 2 and blob.x_pos >= blob.danger_zone) or (blob.player == 1 and blob.x_pos <= blob.danger_zone)) and blob.danger_zone_enabled):
                    #Take additional damage from kicks if you are hiding by your goal
                    hit_dict["accumulated_damage"] += 1
                if(self.status_effects['steroided']):
                    hit_dict["pierce"] += 1
        return hit_dict

    def cooldown(self):
        super().cooldown()
        if(self.special_ability_timer > 0 and self.ability_holding_timer % 18 == 17):
            Blob.create_blob_sfx('Wind')

    def ability(self):
        if('gale' in self.used_ability and self.special_ability_meter > self.special_ability_maintenance):
            #If we were holding down the button before
            self.used_ability["gale"] += 1
            self.special_ability_timer = self.special_ability_cooldown #Set the cooldown between uses timer
            self.special_ability_meter -= self.special_ability_maintenance #Remove some SA meter
            self.ability_holding_timer += 1
        elif(self.special_ability_meter > self.special_ability_cost):
            #If we ignite the ball
            self.used_ability["gale"] = 1
            self.special_ability_timer = self.special_ability_cooldown_max #Set the cooldown between uses timer
            self.special_ability_meter -= self.special_ability_cost #Remove some SA meter
            self.ability_holding_timer = 0
            Blob.create_blob_sfx('gale')
