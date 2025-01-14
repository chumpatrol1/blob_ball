from engine.blobs.blobs import Blob
import random
from engine.environmental_modifiers import create_environmental_modifier
class Joker(Blob):
    default_stats = {"hp": 8}
    species = "joker"
    def __init__(self, x_pos = 50, y_pos = 1200, facing = 'left', player = 1, 
    special_ability_charge_base = 1, costume = 0, danger_zone_enabled = True, is_cpu = False, stat_overrides = [], match_state = None):
        super().__init__(x_pos, y_pos, facing, player, special_ability_charge_base, costume, 
        danger_zone_enabled, is_cpu, stat_overrides, match_state, __file__)
        self.load_init_blob(__file__)

    def ability(self, card = None):
        if(self.special_ability_meter >= self.special_ability_cost and self.special_ability_cooldown <= 0 and not self.status_effects['menu']['open'] and not self.status_effects['cards']['ability']):
            self.special_ability_timer = self.special_ability_cooldown
            self.special_ability_meter -= self.special_ability_cost
            self.status_effects['menu']['open'] = True
            self.status_effects['menu']['type'] = 'cardpack'
            self.status_effects['menu']['time'] = 0

            #print("RECHARGE", self.status_effects['cards']['recharge'])

            self.status_effects['cards']['pulled'] = random.sample(sorted(self.status_effects['cards']['pool']), 3)
            for card in self.status_effects['cards']['pulled']:
                self.status_effects['cards']['pool'].remove(card)
            for card in self.status_effects['cards']['recharge']:
                self.status_effects['cards']['pool'].add(card)
            self.status_effects['cards']['recharge'] = set()
        elif self.status_effects['cards']['ability'] and self.special_ability_cooldown <= 0:
            self.special_ability_cooldown = self.special_ability_cooldown_max
            self.use_card(self.status_effects['cards']['ability'])
            self.status_effects['cards']['equipped'].remove(self.status_effects['cards']['ability'])
            self.status_effects['cards']['recharge'].add(self.status_effects['cards']['ability'])
            self.status_effects['cards']['ability'] = None
            self.recharge_indicators['ability_swap'] = True

        else:
            return
    
    def use_card(self, card):
        # TODO:
        match card:
            case 'c&d':
                self.used_ability["c&d"] = 2
            case 'pill':
                if(self.status_effects['pill'] == 'pill_heal'):
                    if(self.hp != self.max_hp):
                        self.heal_hp(heal_amt = 1)
                    sac = bool(self.special_ability_cooldown > 0)
                    skc = bool(self.kick_cooldown > 0)
                    slc = bool(self.block_cooldown > 0)
                    sbc = bool(self.boost_cooldown_timer > 0)
                    self.special_ability_cooldown -= 30 * Blob.timer_multiplier
                    self.kick_cooldown -= 30 * Blob.timer_multiplier
                    self.block_cooldown -= 30 * Blob.timer_multiplier
                    if(self.boost_cooldown_timer > 0):
                        self.boost_cooldown_timer -= 30 * Blob.timer_multiplier
                    self.check_cooldown_completion(sac, skc, slc, sbc)
                elif(self.status_effects['pill'] == 'pill_cooldown'):
                    sac = bool(self.special_ability_cooldown > 0)
                    skc = bool(self.kick_cooldown > 0)
                    slc = bool(self.block_cooldown > 0)
                    sbc = bool(self.boost_cooldown_timer > 0)
                    #self.special_ability_cooldown -= 90 * Blob.timer_multiplier
                    self.kick_cooldown -= 90 * Blob.timer_multiplier
                    self.block_cooldown -= 90 * Blob.timer_multiplier
                    if(self.boost_cooldown_timer > 0):
                        self.boost_cooldown_timer -= 90 * Blob.timer_multiplier
                    self.check_cooldown_completion(sac, skc, slc, sbc)

                else:
                    self.status_effects['steroided'] += 180
                    self.boost(boost_cost = 0, boost_duration=180, boost_cooldown=0, ignore_cooldown=True)

                if(self.hp <= self.max_hp//2):
                        self.status_effects['pill'] = 'pill_heal'
                else:
                    if(self.status_effects['pill'] == 'pill_cooldown'):
                        self.status_effects['pill'] = 'pill_boost'
                    elif(self.status_effects['pill'] == 'pill_boost'):
                        self.status_effects['pill'] = 'pill_heal'
                    else:
                        self.status_effects['pill'] = 'pill_cooldown'
            case 'tax':
                self.used_ability["tax"] = 2
                skc = bool(self.kick_cooldown > 0)
                slc = bool(self.block_cooldown > 0)
                sbc = bool(self.boost_cooldown_timer > 0)
                self.kick_cooldown -= 30 * Blob.timer_multiplier
                self.block_cooldown -= 30 * Blob.timer_multiplier
                if(self.boost_cooldown_timer > 0):
                    self.boost_cooldown_timer -= 30 * Blob.timer_multiplier
                self.check_cooldown_completion(updatedKick=skc, updatedBlock=slc, updatedBoost=sbc)
                Blob.create_blob_sfx('chime_progress')
            case 'stoplight':
                self.used_ability["stoplight"] = 1
                Blob.create_blob_sfx("whistle")
            case 'mirror':
                self.used_ability["mirror"] = 2
                self.apply_status_effect("reflecting", duration = self.special_ability_duration)
                self.kick_cooldown += 60 * Blob.timer_multiplier
                self.block_cooldown += 60 * Blob.timer_multiplier
                self.boost_cooldown_timer += 60 * Blob.timer_multiplier
                Blob.create_blob_sfx('chime_progress')
            case 'teleport':
                if(self.facing == 'left'):
                    x_mod = -1
                else:
                    x_mod = 1
                create_environmental_modifier(self.player, affects = {'self'}, species = 'cartridge', lifetime = 600, hp = 1, x_pos = self.x_center, y_pos = self.y_center - 10, x_speed = (3*self.x_speed/4) + (4*x_mod), y_speed = (self.y_speed/2) - 12, gravity = 0.4, random_image = self.status_effects['teleporter'][0])
                self.status_effects['teleporter'][0] += 1
                if(self.status_effects['teleporter'][0]) > 3:
                    self.status_effects['teleporter'][0] = 1
            case 'spire':
                Blob.create_blob_sfx('glyph')
                create_environmental_modifier(player = self.player, affects = {'enemy', 'ball'}, species = 'spire_glyph', lifetime = 30, y_pos = 700, special_functions = [create_environmental_modifier])
            case 'thunderbolt':
                create_environmental_modifier(player = self.player, affects = {'self', 'enemy', 'ball'}, species = 'thunder_glyph', lifetime = 10, y_pos = 700, special_functions = [create_environmental_modifier])
            case 'starpunch':
                create_environmental_modifier(player = self.player, affects = {'enemy'}, species = 'starpunch_wait', lifetime = 25, y_pos = self.y_center, special_functions = [create_environmental_modifier])
                Blob.create_blob_sfx('boxing_bell')

    def kick(self, ignore_cooldown = False):
        if(not self.status_effects['cards']['kick']):
                super().kick(ignore_cooldown)   
        elif((self.kick_cooldown <= 0 or ignore_cooldown) and self.status_effects['cards']['kick']):
            self.use_card(card = self.status_effects['cards']['kick'])
            
            self.kick_cooldown = self.kick_cooldown_max//2
            if(self.special_ability_cooldown < 10 * Blob.timer_multiplier):
                self.special_ability_cooldown = 10 * Blob.timer_multiplier
            if(self.block_cooldown < 10 * Blob.timer_multiplier):
                self.block_cooldown = 10 * Blob.timer_multiplier
            if(self.boost_cooldown_timer < 10 * Blob.timer_multiplier):
                self.boost_cooldown_timer = 10 * Blob.timer_multiplier
            #print(self.status_effects['cards']['kick'])
            self.status_effects['cards']['equipped'].remove(self.status_effects['cards']['kick'])
            self.status_effects['cards']['recharge'].add(self.status_effects['cards']['kick'])
            self.status_effects['cards']['kick'] = None
            self.recharge_indicators['ability_swap'] = True

    def block(self, ignore_cooldown = False):
        if(not self.status_effects['cards']['block']):
                super().block(ignore_cooldown)   
        elif((self.block_cooldown <= 0 or ignore_cooldown) and self.status_effects['cards']['block']):
            self.use_card(card = self.status_effects['cards']['block'])
            self.block_cooldown = self.block_cooldown_max//2 #Set block cooldown
            if(self.special_ability_cooldown < 10 * Blob.timer_multiplier):
                self.special_ability_cooldown = 10 * Blob.timer_multiplier
            if(self.kick_cooldown < 10 * Blob.timer_multiplier):
                self.kick_cooldown = 10 * Blob.timer_multiplier
            if(self.boost_cooldown_timer < 10 * Blob.timer_multiplier):
                self.boost_cooldown_timer = 10 * Blob.timer_multiplier
            #print(self.status_effects['cards']['block'])
            self.status_effects['cards']['equipped'].remove(self.status_effects['cards']['block'])
            self.status_effects['cards']['recharge'].add(self.status_effects['cards']['block'])
            self.status_effects['cards']['block'] = None
            self.recharge_indicators['ability_swap'] = True

    def boost(self, ignore_cooldown = False):
        if(not self.status_effects['cards']['boost']):
                super().boost(ignore_cooldown)   
        elif((self.boost_cooldown_timer <= 0 or ignore_cooldown) and self.status_effects['cards']['boost']):
            self.use_card(card = self.status_effects['cards']['boost'])
            if(self.special_ability_cooldown < 10 * Blob.timer_multiplier):
                self.special_ability_cooldown = 10 * Blob.timer_multiplier
            if(self.kick_cooldown < 10 * Blob.timer_multiplier):
                self.kick_cooldown = 10 * Blob.timer_multiplier
            if(self.block_cooldown < 10 * Blob.timer_multiplier):
                self.boost_cooldown = 10 * Blob.timer_multiplier
            self.boost_cooldown_timer = self.boost_cooldown_max//2
            #print(self.status_effects['cards']['boost'])
            try:
                self.status_effects['cards']['equipped'].remove(self.status_effects['cards']['boost'])
                self.status_effects['cards']['recharge'].add(self.status_effects['cards']['boost'])
            except Exception as ex:
                print("Tried to remove", ex, "from lineup")

            self.status_effects['cards']['boost'] = None
            self.recharge_indicators['ability_swap'] = True

    def handle_menu(self, pressed):
        menu_dict = super().handle_menu(pressed)
        menu_direction = menu_dict["menu_direction"]
        menu_action = menu_dict["menu_action"]
        if('ability' in pressed):
            menu_action = 'ability'
        elif('kick' in pressed):
            menu_action = 'kick'
        elif('block' in pressed):
            menu_action = 'block'
        elif('boost' in pressed):
            menu_action = 'boost'
        selected_card = ''
        other_card_1 = ''
        other_card_2 = ''
        if(menu_direction == 'left'):
            selected_card = self.status_effects['cards']['pulled'][0]
            other_card_1 = self.status_effects['cards']['pulled'][1]
            other_card_2 = self.status_effects['cards']['pulled'][2]
        elif(menu_direction == 'up'):
            other_card_1 = self.status_effects['cards']['pulled'][0]
            selected_card = self.status_effects['cards']['pulled'][1]
            other_card_2 = self.status_effects['cards']['pulled'][2]
        elif(menu_direction == 'right'):
            other_card_1 = self.status_effects['cards']['pulled'][0]
            other_card_2 = self.status_effects['cards']['pulled'][1]
            selected_card = self.status_effects['cards']['pulled'][2]
        if(menu_action != 'neutral' and self.status_effects['menu']['time'] > 10 and menu_direction != 'neutral' and menu_direction != 'down'):
            if(self.status_effects['cards'][menu_action]):
                self.status_effects['cards']['recharge'].add(self.status_effects['cards'][menu_action])
                self.status_effects['cards']['equipped'].remove(self.status_effects['cards'][menu_action])

            # THIS IS THE LINE
            self.status_effects['cards'][menu_action] = selected_card
            self.status_effects['cards']['equipped'].add(selected_card)
            card_pos = (0, 0)
            if(menu_direction == "left"):
                card_pos = (self.x_pos - 105, self.y_pos - 25)
            elif(menu_direction == "up"):
                card_pos = (self.x_pos + 20, self.y_pos - 225)
            elif(menu_direction == "right"):
                card_pos = (self.x_pos + 160, self.y_pos - 25)
            self.status_effects['cards']['joker_particle'] = (card_pos, selected_card)
            self.status_effects['menu']['open'] = False
            self.status_effects['cards']['recharge'].add(other_card_1)
            self.status_effects['cards']['recharge'].add(other_card_2)
            if(menu_action == 'ability'):
                self.special_ability_cooldown = self.special_ability_cooldown_max
            elif('kick' in pressed):
                self.special_ability_cooldown = self.special_ability_cooldown_max
                self.kick_cooldown += 60 * Blob.timer_multiplier
            elif('block' in pressed):
                self.special_ability_cooldown = self.special_ability_cooldown_max
                self.block_cooldown += 60 * Blob.timer_multiplier
            elif('boost' in pressed):
                self.special_ability_cooldown = self.special_ability_cooldown_max
                self.boost_cooldown_timer += 60 * Blob.timer_multiplier
            if(menu_direction == "up"):
                self.jump_lock = 15

            self.recharge_indicators['ability_swap'] = True

        elif(menu_direction == 'down' and self.status_effects['menu']['time'] > 10):
            self.status_effects['cards']['recharge'].add(self.status_effects['cards']['pulled'][0])
            self.status_effects['cards']['recharge'].add(self.status_effects['cards']['pulled'][1])
            self.status_effects['cards']['recharge'].add(self.status_effects['cards']['pulled'][2])
            self.status_effects['menu']['open'] = False
            self.wavedash_lock = 15
            self.special_ability_cooldown = self.special_ability_cooldown_max/2


    def move(self, pressed_buttons):
        
        pressed = super().move(pressed_buttons)
        
        if(self.status_effects['menu']["open"]):
            self.handle_menu(pressed)
        return pressed
    
    def initialize_blob_sprites(self):
        temp_dict = super().initialize_blob_sprites()
        self.ability_icons['joker_card'] = temp_dict['menu']
        self.ability_icons['c&d'] = temp_dict['cnd']
        self.ability_icons['pill'] = temp_dict['pill']
        self.ability_icons['tax'] = temp_dict['tax']
        self.ability_icons['stoplight'] = temp_dict['block']
        self.ability_icons['mirror'] = temp_dict['mirror']
        self.ability_icons['teleport'] = temp_dict['teleport']
        self.ability_icons['spire'] = temp_dict['spire']
        self.ability_icons['thunderbolt'] = temp_dict['thunderbolt']
        self.ability_icons['starpunch'] = temp_dict['starpunch']

    def draw_menu(self, game_display):
        if(self.status_effects['menu']['direction'] == 'left'):
            game_display.blit(self.ability_icons['joker_card'], ((self.x_pos - 105) * (1000/1366), ((self.y_pos - 25)*(382/768))))
            game_display.blit(self.ability_icons[self.status_effects['cards']['pulled'][0]], ((self.x_pos - 100) * (1000/1366), ((self.y_pos - 20) *(382/768))))
        else:
            game_display.blit(self.ability_icons['joker_card'], ((self.x_pos - 105) * (1000/1366), ((self.y_pos - 5)*(382/768))))
            game_display.blit(self.ability_icons[self.status_effects['cards']['pulled'][0]], ((self.x_pos - 100) * (1000/1366), (self.y_pos*(382/768))))
        #print("3", self.status_effects['cards']['pulled'][2])
        if(self.status_effects['menu']['direction'] == 'up'):
            game_display.blit(self.ability_icons['joker_card'], ((self.x_pos + 20) * (1000/1366), ((self.y_pos - 225) *(382/768))))
            game_display.blit(self.ability_icons[self.status_effects['cards']['pulled'][1]], ((self.x_pos + 25) * (1000/1366), ((self.y_pos - 220) *(382/768))))
        else:
            game_display.blit(self.ability_icons['joker_card'], ((self.x_pos + 20) * (1000/1366), ((self.y_pos - 205) *(382/768))))
            game_display.blit(self.ability_icons[self.status_effects['cards']['pulled'][1]], ((self.x_pos + 25) * (1000/1366), ((self.y_pos - 200) *(382/768))))
        #print("2", self.status_effects['cards']['pulled'][1])
        if(self.status_effects['menu']['direction'] == 'right'):
            game_display.blit(self.ability_icons['joker_card'], ((self.x_pos + 160) * (1000/1366), ((self.y_pos - 25)*(382/768))))
            game_display.blit(self.ability_icons[self.status_effects['cards']['pulled'][2]], ((self.x_pos + 165) * (1000/1366), ((self.y_pos-20)*(382/768))))
        else:
            game_display.blit(self.ability_icons['joker_card'], ((self.x_pos + 160) * (1000/1366), ((self.y_pos - 5)*(382/768))))
            game_display.blit(self.ability_icons[self.status_effects['cards']['pulled'][2]], ((self.x_pos + 165) * (1000/1366), (self.y_pos*(382/768))))