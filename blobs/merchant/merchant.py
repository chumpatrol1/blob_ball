from engine.blobs.blobs import Blob
import random
from engine.environmental_modifiers import create_environmental_modifier
class Merchant(Blob):
    default_stats = {"hp": 8}
    def __init__(self, x_pos = 50, y_pos = 1200, facing = 'left', player = 1, 
    special_ability_charge_base = 1, costume = 0, danger_zone_enabled = True, is_cpu = False, stat_overrides = [], match_state = None):
        super().__init__(x_pos, y_pos, facing, player, special_ability_charge_base, costume, 
        danger_zone_enabled, is_cpu, stat_overrides, match_state, __file__)
        self.species = "merchant"
        self.load_init_blob(__file__)

    def ability(self):
        if(self.special_ability_meter >= self.special_ability_cost and self.special_ability_cooldown <= 0 and not self.status_effects['menu']['open']):
            self.status_effects['menu']['open'] = True
            self.status_effects['menu']['type'] = 'shop'
            self.status_effects['menu']['time'] = 0
        else:
            return

    def blob_ko(self):
        super().blob_ko()
        self.status_effects['shop']['spring_lvl'] = 0
        self.status_effects['shop']['sprint_lvl'] = 0
        self.status_effects['shop']['heart_lvl'] = 0
        self.status_effects['shop']['shadow_lvl'] = 0

    def apply_boost_kick_effect(self, blob):
        x_speed_mod = 0
        if(self.status_effects['shop']['spring_lvl']):
            if(self.x_pos < blob.x_pos):
                x_speed_mod = 45
            elif(self.x_pos > blob.x_pos):
                x_speed_mod = -45
            elif(self.x_pos < 902):
                x_speed_mod = 45
            else:
                x_speed_mod = -45
        return x_speed_mod

    def check_blob_collision_default(self, blob):
        hit_dict = super().check_blob_collision_default(blob)
        if(self.status_effects['shop']['spring_lvl'] >= 2):
            if(self.x_pos > blob.x_pos):
                hit_dict["x_speed_mod"] = -15
            elif(self.x_pos < blob.x_pos):
                hit_dict["x_speed_mod"] = 15
            else:
                hit_dict["x_speed_mod"] = -15 if blob.x_pos > 902 else 15
        if(self.boost_timer > 0):
            hit_dict["x_speed_mod"] = self.apply_boost_kick_effect(blob)
        return hit_dict

    def handle_down_press(self, pressed, frame_stats):
        super().handle_down_press(pressed, frame_stats)
        if(self.down_holding_timer % 150 == 0 and self.down_holding_timer and self.status_effects['shop']['heart_lvl']):
            self.heal_hp()

    def apply_wavedash_abilities(self, pressed, frame_stats):
        if(frame_stats["wavedashed"] and self.status_effects['shop']['shadow_lvl'] >= 2):
            create_environmental_modifier(player = self.player, species='sharp_shadow', affects={'enemy'}, lifetime=25, x_pos=self.x_center-20, y_pos=self.y_center-20, hp = 1, special_functions = [create_environmental_modifier])
    

    def handle_menu(self, pressed):
        menu_dict = super().handle_menu(pressed)
        menu_direction = menu_dict["menu_direction"]
        menu_action = menu_dict["menu_action"]
        #selected_card = ''
        if(self.status_effects['menu']['time'] > 5 and menu_direction != 'neutral'):
            monado_activated = False
            if(menu_direction == "up"): # Rainbow Heart
                # Rainbow Heart - Lv1 passively regain 1 extra NRG and heal after focusing. Lv2 passively regain 2 extra NRG. Lv3 instantly regains 1 HP
                self.jump_lock = 15 # Prevents the player from jumping immediately after a purchase
                monado_activated = True
                self.status_effects['shop']['purchase_particle'] = f"rainbow_heart_{self.status_effects['shop']['heart_lvl']}"
                self.status_effects['shop']['heart_lvl'] += 1
                if(self.status_effects['shop']['heart_lvl'] == 3):
                    self.heal_hp()
                    self.status_effects['shop']['heart_lvl'] = 2
                
            elif(menu_direction == "down"): # Sprint Master
                # Sprintmaster - Lv1 is minor speed boost. Lv2 is major speed boost. Lv3 gives hot sauce effect
                self.wavedash_lock = 15
                monado_activated = True
                self.status_effects['shop']['purchase_particle'] = f"sprint_master_{self.status_effects['shop']['sprint_lvl']}"
                self.status_effects['shop']['sprint_lvl'] += 1
                if(self.status_effects['shop']['sprint_lvl'] == 3):
                    self.apply_status_effect("monado_effect", duration = "SPEED", method = "set")
                    self.apply_status_effect("monado_timer", duration = 300)
                    self.status_effects['shop']['sprint_lvl'] = 2
                #"shop": {'heart_lvl': 0, 'spring_lvl': 0, 'sprint_lvl': 0, 'sh
            elif(menu_direction == "left"): # Sharp Shadow
                # Sharp Shadow - Lv1 Makes your wavedash longer. Lv2 creates a Sharp Shadow hitbox. Lv3 instantly creates a SS hitbox
                monado_activated = True
                self.status_effects['shop']['purchase_particle'] = f"sharp_shadow_{self.status_effects['shop']['shadow_lvl']}"
                self.status_effects['shop']['shadow_lvl'] += 1
                if(self.status_effects['shop']['shadow_lvl'] == 3):
                    create_environmental_modifier(player = self.player, species='sharp_shadow', affects={'enemy'}, lifetime=60, x_pos=self.x_center-20, y_pos=self.y_center-20, hp = 1, special_functions = [create_environmental_modifier])
                    self.status_effects['shop']['shadow_lvl'] = 2
            elif(menu_direction == "right"): # Spring Kick
                # Spring Kick - Lv1 makes Boost Kick do KB. Lv2 increases KB and extends functionality to regular kick as well. Lv3 adds steroids for 3 seconds
                monado_activated = True
                self.status_effects['shop']['purchase_particle'] = f"spring_kick_{self.status_effects['shop']['spring_lvl']}"
                self.status_effects['shop']['spring_lvl'] += 1
                if(self.status_effects['shop']['spring_lvl'] == 3):
                    self.apply_status_effect("steroided", 180, 180, "add")
                    self.status_effects['shop']['spring_lvl'] = 2
                
                #"shop": {'heart_lvl': 0, 'spring_lvl': 0, 'sprint_lvl': 0, 'shadow_lvl': 0},
            
            if(monado_activated):
                Blob.create_blob_sfx('crunch')
                self.status_effects['menu']['open'] = False
                #self.status_effects['monado_timer'] = 300
                #if(self.status_effects['monado_effect'] == "SHIELD"):
                #    self.status_effects['monado_timer'] = 420
                self.movement_lock = 5
                self.special_ability_timer = self.special_ability_cooldown
                self.special_ability_meter -= self.special_ability_cost
                self.special_ability_cooldown = self.special_ability_cooldown_max
            
        elif(menu_direction == 'neutral' and menu_action == 'ability' and self.status_effects['menu']['time'] > 15):
            self.status_effects['menu']['open'] = False
            self.special_ability_cooldown = self.special_ability_cooldown_max/2

    def move(self, pressed_buttons):
        
        pressed = super().move(pressed_buttons)
        
        if(self.status_effects['menu']["open"]):
            self.handle_menu(pressed)
        return pressed
    
    def initialize_blob_sprites(self):
        temp_dict = super().initialize_blob_sprites()
        self.ability_icons['shop_ui'] = temp_dict['menu']
        blob_height = round(temp_dict['alive'].get_height() * 0.6)
        import pygame as pg
        self.blob_images['shop_left'] = pg.transform.scale(temp_dict['shopping'].convert_alpha(), (120, blob_height))
        self.blob_images['shop_right'] = pg.transform.flip(self.blob_images['shop_left'], True, False)
        self.blob_images['shop_damage_left'] = self.blob_images['shop_left'].copy()
        self.blob_images['shop_damage_left'].set_alpha(100)
        self.blob_images['shop_damage_right'] = self.blob_images['shop_right'].copy()
        self.blob_images['shop_damage_right'].set_alpha(100)
        sprite_tuple = (self.species, self.costume)
        if(sprite_tuple in self.sprite_collisions):
            match self.sprite_collisions[sprite_tuple]:
                case 2:
                    self.blob_images['shop_left'].fill((150, 150, 150, 255), special_flags=pg.BLEND_RGBA_MULT)
                    self.blob_images['shop_right'].fill((150, 150, 150, 255), special_flags=pg.BLEND_RGBA_MULT)
                    self.blob_images['shop_damage_left'].fill((150, 150, 150, 255), special_flags=pg.BLEND_RGBA_MULT)
                    self.blob_images['shop_damage_right'].fill((150, 150, 150, 255), special_flags=pg.BLEND_RGBA_MULT)
                case 3:
                    self.blob_images['shop_left'].fill((255, 255, 255, 255), special_flags=pg.BLEND_RGBA_MULT)
                    self.blob_images['shop_right'].fill((255, 255, 255, 255), special_flags=pg.BLEND_RGBA_MULT)
                    self.blob_images['shop_damage_left'].fill((255, 255, 255, 255), special_flags=pg.BLEND_RGBA_MULT)
                    self.blob_images['shop_damage_right'].fill((255, 255, 255, 255), special_flags=pg.BLEND_RGBA_MULT)
                case 4:
                    self.blob_images['shop_left'].fill((100, 100, 100, 255), special_flags=pg.BLEND_RGBA_MULT)
                    self.blob_images['shop_right'].fill((100, 100, 100, 255), special_flags=pg.BLEND_RGBA_MULT)
                    self.blob_images['shop_damage_left'].fill((100, 100, 100, 255), special_flags=pg.BLEND_RGBA_MULT)
                    self.blob_images['shop_damage_right'].fill((100, 100, 100, 255), special_flags=pg.BLEND_RGBA_MULT)

    def draw(self, game_display):
        # Separate Chunk        
        #pname = "p" + str(self.player) + "_"
        #if self.recharge_indicators['ability_swap_b']:
        #    try:
        #        self.blob_images[pname + 'ability_icon'] = pg.transform.scale(pg.image.load(self.ability_icon).convert_alpha(), (70, 70))
        #    except:
        #        self.blob_images[pname + 'ability_icon'] = pg.transform.scale(pg.image.load("/resources/images/ui_icons/404.png").convert_alpha(), (70, 70))
        #    self.blob_images['ui_initialized'] = False
        #
        #if not (blob.image == self.blob_images['blob_clone']):
        #    blob_height = round(pg.image.load(blob.image).get_height()*0.6)
        #    self.blob_images['blob'] = pg.transform.scale(pg.image.load(blob.image).convert_alpha(), (120, blob_height))
        #    self.blob_images['blob_clone'] = blob.image
        # Tuple structure: Direction facing ("left", "right"), Blob Status (0 is normal, 1 is hurt, 2 is dead)
        sprite_dict = {
            ("right", 0, False): self.blob_images["blob_right"],
            ("left", 0, False): self.blob_images["blob_left"],
            ("right", 1, False): self.blob_images["damage_right"],
            ("left", 1, False): self.blob_images["damage_left"],
            ("right", 2, False): self.blob_images["dead_right"],
            ("left", 2, False): self.blob_images["dead_left"],
            ("right", 0, True): self.blob_images["shop_right"],
            ("left", 0, True): self.blob_images["shop_left"],
            ("right", 1, True): self.blob_images["shop_damage_right"],
            ("left", 1, True): self.blob_images["shop_damage_left"],
            ("right", 2, True): self.blob_images["dead_right"],
            ("left", 2, True): self.blob_images["dead_left"],
        }
        blob_status = 2 if self.hp <= 0 else 1 if (self.damage_flash_timer//10) % 2 == 1 else 0
        blob_image = sprite_dict[(self.facing, blob_status, self.status_effects['menu']['open'])]
        
        blob_y_pos = self.y_pos - (blob_image.get_height() - 66)
        game_display.blit(blob_image, (self.x_pos*(1000/1366), (blob_y_pos*(400/768))))

        #draw_blob_special(blob, game_display)
        #draw_blob_particles(game_display, blobs.values()) # TODO: Fix this!

        if(self.status_effects['menu']['open']):
            self.draw_menu(game_display)

    def draw_menu(self, game_display):
        # Up/Rainbow Heart
        if(self.status_effects['shop']['heart_lvl'] == 0):
            cropRect = (0, 60, 60, 60)
            game_display.blit(self.ability_icons['shop_ui'], ((self.x_pos + 25) * (1000/1366), ((self.y_pos-180)*(382/768))), area = cropRect)
        elif(self.status_effects['shop']['heart_lvl'] == 1):
            cropRect = (60, 60, 60, 60)
            game_display.blit(self.ability_icons['shop_ui'], ((self.x_pos + 25) * (1000/1366), ((self.y_pos-180)*(382/768))), area = cropRect)
        elif(self.status_effects['shop']['heart_lvl'] == 2):
            cropRect = (120, 60, 60, 60)
            game_display.blit(self.ability_icons['shop_ui'], ((self.x_pos + 25) * (1000/1366), ((self.y_pos-180)*(382/768))), area = cropRect)

        # Left/Sharp Shadow
        if(self.status_effects['shop']['shadow_lvl'] == 0):
            cropRect = (180, 60, 60, 60)
            game_display.blit(self.ability_icons['shop_ui'], ((self.x_pos - 100) * (1000/1366), ((self.y_pos-10)*(382/768))), area = cropRect)
        elif(self.status_effects['shop']['shadow_lvl'] == 1):
            cropRect = (240, 60, 60, 60)
            game_display.blit(self.ability_icons['shop_ui'], ((self.x_pos - 100) * (1000/1366), ((self.y_pos-10)*(382/768))), area = cropRect)
        elif(self.status_effects['shop']['shadow_lvl'] == 2):
            cropRect = (300, 60, 60, 60)
            game_display.blit(self.ability_icons['shop_ui'], ((self.x_pos - 100) * (1000/1366), ((self.y_pos-10)*(382/768))), area = cropRect)
        
        # Right/Spring Kick
        if(self.status_effects['shop']['spring_lvl'] == 0):
            cropRect = (0, 0, 60, 60)
            game_display.blit(self.ability_icons['shop_ui'], ((self.x_pos + 165) * (1000/1366), ((self.y_pos-20)*(382/768))), area = cropRect)
        elif(self.status_effects['shop']['spring_lvl'] == 1):
            cropRect = (60, 0, 60, 60)
            game_display.blit(self.ability_icons['shop_ui'], ((self.x_pos + 165) * (1000/1366), ((self.y_pos-20)*(382/768))), area = cropRect)
        elif(self.status_effects['shop']['spring_lvl'] == 2):
            cropRect = (120, 0, 60, 60)
            game_display.blit(self.ability_icons['shop_ui'], ((self.x_pos + 165) * (1000/1366), ((self.y_pos-20)*(382/768))), area = cropRect)
        
        # Down/Sprintmaster
        if(self.status_effects['shop']['sprint_lvl'] == 0):
            cropRect = (180, 0, 60, 60)
            game_display.blit(self.ability_icons['shop_ui'], ((self.x_pos + 25) * (1000/1366), ((self.y_pos+185)*(382/768))), area = cropRect)
        elif(self.status_effects['shop']['sprint_lvl'] == 1):
            cropRect = (240, 0, 60, 60)
            game_display.blit(self.ability_icons['shop_ui'], ((self.x_pos + 25) * (1000/1366), ((self.y_pos+175)*(382/768))), area = cropRect)
        elif(self.status_effects['shop']['sprint_lvl'] == 2):
            cropRect = (300, 0, 60, 60)
            game_display.blit(self.ability_icons['shop_ui'], ((self.x_pos + 25) * (1000/1366), ((self.y_pos+175)*(382/768))), area = cropRect)