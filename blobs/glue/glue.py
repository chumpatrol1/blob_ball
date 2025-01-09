from engine.blobs.blobs import Blob
import random
from json import loads, dumps
from engine.environmental_modifiers import create_environmental_modifier

class Glue(Blob):
    default_stats = {"hp": 8}
    species = "glue"
    def __init__(self, x_pos = 50, y_pos = 1200, facing = 'left', player = 1, 
    special_ability_charge_base = 1, costume = 0, danger_zone_enabled = True, is_cpu = False, stat_overrides = [], match_state = None):
        super().__init__(x_pos, y_pos, facing, player, special_ability_charge_base, costume, 
        danger_zone_enabled, is_cpu, stat_overrides, match_state, __file__)
        self.load_init_blob(__file__)

    def ability(self):
        if('gluegun' in self.used_ability and self.special_ability_meter > self.special_ability_maintenance):
            #If we were holding down the button before
            self.used_ability["gluegun"] += 1
            self.special_ability_timer = self.special_ability_cooldown_max #Set the cooldown between uses timer
            self.special_ability_meter -= self.special_ability_maintenance #Remove some SA meter
            self.ability_holding_timer += 1
        elif(self.special_ability_meter > self.special_ability_cost):
            #If we ignite the ball
            self.used_ability["gluegun"] = 1
            self.special_ability_timer = self.special_ability_cooldown_max #Set the cooldown between uses timer
            self.special_ability_meter -= self.special_ability_cost #Remove some SA meter
            self.ability_holding_timer = 0
        else:
            return
        if(self.facing == 'left'):
            x_mod = -1
        else:
            x_mod = 1
        if(not (self.ability_holding_timer % 4)):
            create_environmental_modifier(self.player, affects = {'enemy', 'self', 'ball'}, species = 'glue_shot', x_pos = self.x_center, y_pos = self.y_center - 10, x_speed = (3*self.x_speed/4) + (6*x_mod), y_speed = (self.y_speed/2) - 7, gravity = 0.25, lifetime = 600, special_functions = [create_environmental_modifier])
                
    def apply_wavedash_abilities(self, pressed, frame_stats):
        if(frame_stats["wavedashed"] and self.special_ability_meter >= 300 * Blob.nrg_multiplier):
            x_mod = 1 if self.facing == 'left' else -1
            create_environmental_modifier(self.player, affects = {'enemy', 'self', 'ball'}, species = 'glue_shot', x_pos = self.x_center, y_pos = self.y_center - 10, x_speed = (3*self.x_speed/4) + (6*x_mod), y_speed = -1, gravity = 0.25, lifetime = 600, special_functions = [create_environmental_modifier])
            create_environmental_modifier(self.player, affects = {'enemy', 'self', 'ball'}, species = 'glue_shot', x_pos = self.x_center, y_pos = self.y_center - 10, x_speed = (5*self.x_speed/4) + (6*x_mod), y_speed = -1, gravity = 0.25, lifetime = 600, special_functions = [create_environmental_modifier])
            create_environmental_modifier(self.player, affects = {'enemy', 'self', 'ball'}, species = 'glue_shot', x_pos = self.x_center, y_pos = self.y_center - 10, x_speed = (7*self.x_speed/4) + (6*x_mod), y_speed = -1, gravity = 0.25, lifetime = 600, special_functions = [create_environmental_modifier])
            create_environmental_modifier(self.player, affects = {'enemy', 'self', 'ball'}, species = 'glue_shot', x_pos = self.x_center, y_pos = self.y_center - 10, x_speed = (9*self.x_speed/4) + (6*x_mod), y_speed = -1, gravity = 0.25, lifetime = 600, special_functions = [create_environmental_modifier])            
            create_environmental_modifier(self.player, affects = {'enemy', 'self', 'ball'}, species = 'glue_shot', x_pos = self.x_center, y_pos = self.y_center - 10, x_speed = (11*self.x_speed/4) + (6*x_mod), y_speed = -1, gravity = 0.25, lifetime = 600, special_functions = [create_environmental_modifier])
            self.special_ability_meter -= 300 * Blob.nrg_multiplier
        return super().apply_wavedash_abilities(pressed, frame_stats)         