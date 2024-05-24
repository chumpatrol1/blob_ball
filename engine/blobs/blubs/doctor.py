from .blobs import Blob
import random
class Doctor(Blob):
    def __init__(self, x_pos = 50, y_pos = 1200, facing = 'left', player = 1, 
    special_ability_charge_base = 1, costume = 0, danger_zone_enabled = True, is_cpu = False, stat_overrides = [], match_state = None):
        super().__init__(x_pos, y_pos, facing, player, special_ability_charge_base, costume, 
        danger_zone_enabled, is_cpu, stat_overrides, match_state)
        random_number = random.randint(0,1)
        if(random_number):
            self.status_effects['pill'] = 'pill_boost'
            self.update_ability_icon(cwd + "/resources/images/ability_icons/{}.png".format(self.status_effects['pill']))
        else:
            self.status_effects['pill'] = 'pill_cooldown'
            cwd + "/resources/images/ability_icons/{}.png".format(self.status_effects['pill'])
            self.update_ability_icon(cwd + "/resources/images/ability_icons/{}.png".format(self.status_effects['pill']))