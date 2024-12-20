from engine.blobs.blobs import Blob
import random
from engine.environmental_modifiers import create_environmental_modifier
import pygame as pg
class Taco(Blob):
    default_stats = {"hp": 8}
    def __init__(self, x_pos = 50, y_pos = 1200, facing = 'left', player = 1, 
    special_ability_charge_base = 1, costume = 0, danger_zone_enabled = True, is_cpu = False, stat_overrides = [], match_state = None):
        super().__init__(x_pos, y_pos, facing, player, special_ability_charge_base, costume, 
        danger_zone_enabled, is_cpu, stat_overrides, match_state, __file__)
        self.species = "taco"
        self.load_init_blob(__file__)

    def check_blob_collision_default(self, blob):
        hit_dict = super().check_blob_collision_default(blob)
        if self.status_effects['monado_effect'] == "SMASH":
            hit_dict["pierce"] += 1
            hit_dict["accumulated_damage"] += 1
        return hit_dict

    def calculate_damage(self, damage):
        return damage - bool(self.status_effects['reflecting'] > 0) + 2 * bool(self.status_effects['monado_effect'] == "SMASH") + bool(self.status_effects['monado_effect'] == "JUMP") + bool(self.status_effects['monado_effect'] == "SPEED") - bool(self.status_effects['monado_effect'] == "SHIELD") # Damage is reduced by 1 if we are reflecting
        # Damage is increased by 1 if we are using Meat, Hot Sauce, or Jump and decreased by 1 for Vegan Crunch
    
    def ability(self):
        if(self.special_ability_meter >= self.special_ability_cost and self.special_ability_cooldown <= 0 and not self.status_effects['menu']['open']):
            self.status_effects['menu']['open'] = True
            self.status_effects['menu']['type'] = 'monado'
            self.status_effects['menu']['time'] = 0
        else:
            return

    def handle_menu(self, pressed):
        menu_dict = super().handle_menu(pressed)
        menu_direction = menu_dict["menu_direction"]
        menu_action = menu_dict["menu_action"]
        #selected_card = ''
        if(self.status_effects['menu']['time'] > 5 and menu_direction != 'neutral'):
            monado_activated = False
            if(menu_direction == "up" and self.status_effects['monado_jump_cooldown'] <= 0):
                self.jump_lock = 15
                self.status_effects['monado_effect'] = "JUMP"
                self.status_effects['monado_jump_cooldown'] = 1080
                monado_activated = True
            elif(menu_direction == "down" and self.status_effects['monado_shield_cooldown'] <= 0):
                self.wavedash_lock = 15
                self.status_effects['monado_effect'] = "SHIELD"
                self.status_effects['monado_shield_cooldown'] = 1080
                monado_activated = True
            elif(menu_direction == "left" and self.status_effects['monado_smash_cooldown'] <= 0):
                self.status_effects['monado_effect'] = "SMASH"
                self.status_effects['monado_smash_cooldown'] = 1080
                monado_activated = True
            elif(menu_direction == "right" and self.status_effects['monado_speed_cooldown'] <= 0):
                self.status_effects['monado_effect'] = "SPEED"
                self.status_effects['monado_speed_cooldown'] = 1380
                monado_activated = True
                
                #"shop": {'heart_lvl': 0, 'spring_lvl': 0, 'sprint_lvl': 0, 'shadow_lvl': 0},
            
            if(monado_activated):
                Blob.create_blob_sfx('crunch')
                self.status_effects['menu']['open'] = False
                #self.status_effects['monado_timer'] = 300
                #if(self.status_effects['monado_effect'] == "SHIELD"):
                #    self.status_effects['monado_timer'] = 420
                self.status_effects['monado_timer'] = 300
                if(self.status_effects['monado_effect'] == "SHIELD"):
                    self.status_effects['monado_timer'] = 420
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
        self.ability_icons['cheese'] = temp_dict['cheese']
        self.ability_icons['hot_sauce'] = temp_dict['hot_sauce']
        self.ability_icons['meat'] = temp_dict['meat']
        self.ability_icons['vegan_crunch'] = temp_dict['vegan_crunch']

    def draw_menu(self, game_display):
        if(self.status_effects['menu']['direction'] == 'left' and self.status_effects['monado_smash_cooldown'] <= 0):
            #game_display.blit(self.ability_icons['joker_card'], ((self.x_pos - 105) * (1000/1366), ((self.y_pos - 25)*(382/768))))
            game_display.blit(self.ability_icons["meat"], ((self.x_pos - 100) * (1000/1366), ((self.y_pos - 10) *(382/768))))
        elif(self.status_effects['monado_smash_cooldown'] <= 0):
            #game_display.blit(self.ability_icons['joker_card'], ((self.x_pos - 105) * (1000/1366), ((self.y_pos - 5)*(382/768))))
            game_display.blit(self.ability_icons["meat"], ((self.x_pos - 100) * (1000/1366), ((self.y_pos+10)*(382/768))))
        else:
            pg.draw.rect(game_display, (124, 124, 124), ((self.x_pos - 105) * (1000/1366), ((self.y_pos + 55)*(382/768)), 80, 20))
            pg.draw.rect(game_display, (200, 200, 200), ((self.x_pos - 105) * (1000/1366), ((self.y_pos + 55)*(382/768)), 80*(self.status_effects['monado_smash_cooldown']/900), 20))
        #print("3", self.status_effects['cards']['pulled'][2])
        if(self.status_effects['menu']['direction'] == 'up' and self.status_effects['monado_jump_cooldown'] <= 0):
            #game_display.blit(self.ability_icons['joker_card'], ((self.x_pos + 20) * (1000/1366), ((self.y_pos - 225) *(382/768))))
            game_display.blit(self.ability_icons["cheese"], ((self.x_pos + 25) * (1000/1366), ((self.y_pos - 180) *(382/768))))
        elif(self.status_effects['monado_jump_cooldown'] <= 0):
            #game_display.blit(self.ability_icons['joker_card'], ((self.x_pos + 20) * (1000/1366), ((self.y_pos - 205) *(382/768))))
            game_display.blit(self.ability_icons["cheese"], ((self.x_pos + 25) * (1000/1366), ((self.y_pos - 160) *(382/768))))
        else:
            pg.draw.rect(game_display, (124, 124, 124), ((self.x_pos + 20) * (1000/1366), ((self.y_pos - 95)*(382/768)), 80, 20))
            pg.draw.rect(game_display, (200, 200, 200), ((self.x_pos + 20) * (1000/1366), ((self.y_pos - 95)*(382/768)), 80*(self.status_effects['monado_jump_cooldown']/900), 20))
        #print("2", self.status_effects['cards']['pulled'][1])
        if(self.status_effects['menu']['direction'] == 'right' and self.status_effects['monado_speed_cooldown'] <= 0):
            #game_display.blit(self.ability_icons['joker_card'], ((self.x_pos + 160) * (1000/1366), ((self.y_pos - 25)*(382/768))))
            game_display.blit(self.ability_icons["hot_sauce"], ((self.x_pos + 165) * (1000/1366), ((self.y_pos-20)*(382/768))))
        elif(self.status_effects['monado_speed_cooldown'] <= 0):
            #game_display.blit(self.ability_icons['joker_card'], ((self.x_pos + 160) * (1000/1366), ((self.y_pos - 5)*(382/768))))
            game_display.blit(self.ability_icons["hot_sauce"], ((self.x_pos + 165) * (1000/1366), (self.y_pos*(382/768))))
        else:
            pg.draw.rect(game_display, (124, 124, 124), ((self.x_pos + 160) * (1000/1366), ((self.y_pos + 55)*(382/768)), 80, 20))
            pg.draw.rect(game_display, (200, 200, 200), ((self.x_pos + 160) * (1000/1366), ((self.y_pos + 55)*(382/768)), 80*(self.status_effects['monado_speed_cooldown']/1200), 20))
        if(self.status_effects['menu']['direction'] == 'down' and self.status_effects['monado_shield_cooldown'] <= 0):
            #game_display.blit(self.ability_icons['joker_card'], ((self.x_pos + 20) * (1000/1366), ((self.y_pos + 185) *(382/768))))
            game_display.blit(self.ability_icons["vegan_crunch"], ((self.x_pos + 25) * (1000/1366), ((self.y_pos+175)*(382/768))))
        elif(self.status_effects['monado_shield_cooldown'] <= 0):
            #game_display.blit(self.ability_icons['joker_card'], ((self.x_pos + 20) * (1000/1366), ((self.y_pos + 205) *(382/768))))
            game_display.blit(self.ability_icons["vegan_crunch"], ((self.x_pos + 25) * (1000/1366), ((self.y_pos+195)*(382/768))))
        else:
            pg.draw.rect(game_display, (124, 124, 124), ((self.x_pos + 20) * (1000/1366), ((self.y_pos + 240)*(382/768)), 80, 20))
            pg.draw.rect(game_display, (200, 200, 200), ((self.x_pos + 20) * (1000/1366), ((self.y_pos + 240)*(382/768)), 80*(self.status_effects['monado_shield_cooldown']/900), 20))