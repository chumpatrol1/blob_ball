import pygame as pg
import sys
import engine.handle_input
import engine.blobs
import engine.ball
import time
from json import dumps, loads
from engine.endgame import update_game_stats, update_mu_chart
import engine.cpu_logic

def initialize_players(p1_selected, p2_selected, ruleset, settings, p1_is_cpu, p2_is_cpu):
    global goal_limit
    global time_limit
    global time_bonus
    p1_blob = engine.blobs.Blob(species = p1_selected, player = 1, x_pos = 100, facing = 'right', special_ability_charge_base = ruleset['special_ability_charge_base'], danger_zone_enabled = ruleset['danger_zone_enabled'], is_cpu = p1_is_cpu)
    p2_blob = engine.blobs.Blob(species = p2_selected, player = 2, x_pos = 1600, facing = 'left', special_ability_charge_base = ruleset['special_ability_charge_base'], danger_zone_enabled = ruleset['danger_zone_enabled'], is_cpu = p2_is_cpu)
    ball = engine.ball.Ball()
    goal_limit = ruleset['goal_limit']
    if(ruleset['time_limit'] == 0):
        time_limit = "NO LIMIT"
    else:
        time_limit = ruleset['time_limit']
    time_bonus = ruleset['time_bonus']
    return p1_blob, p2_blob, ball

initialized = False
p1_blob = None
p2_blob = None
ball = None
game_score = [0, 0]
timer = 180
countdown = 0
p1_ko = False
p2_ko = False
goal_scored = False
goal_scorer = None
#goal_limit = 5 #Defaults to 5 goals
#time_limit = 3600 #Defaults to 3600, or 1 minute
#time_bonus = 600 #Defaults to 600, or 10 seconds
game_info = {
        'game_score': game_score,
        'time': 0,
        'time_seconds': 0,
        'avg_collisions_per_goal': 0,
        }

def reset_round():
    global p1_blob
    global p2_blob
    global ball
    global p1_ko
    global p2_ko
    p1_blob.reset(1)
    p2_blob.reset(2)
    ball.reset()
    p1_ko = False
    p2_ko = False

def score_goal(winner, goal_limit):
    global timer
    global time_limit
    global time_bonus
    if not time_limit == "NO LIMIT":
        time_limit += time_bonus
    game_score[winner] += 1
    timer = 60
    if(game_score[winner] >= goal_limit):
        return "casual_win", (winner + 1)
    reset_round()
    return "casual_match", 0
    

def handle_gameplay(p1_selected, p2_selected, ruleset, settings, p1_is_cpu, p2_is_cpu):
    pressed = engine.handle_input.gameplay_input()
    global initialized
    global p1_blob
    global p2_blob
    global ball
    global game_score
    global timer
    global p1_ko
    global p2_ko
    global countdown
    global goal_scorer
    global goal_scored
    global score_goal
    global goal_limit
    global time_limit
    
    game_state = "casual_match"

    def blob_ko(blob):
        blob.blob_ko()


    if not initialized:
        blobs = initialize_players(p1_selected, p2_selected, ruleset, settings, p1_is_cpu, p2_is_cpu)
        p1_blob = blobs[0]
        p2_blob = blobs[1]
        ball = blobs[2]
        
        initialized = True
    else:
        if(timer == 0):
            if(p1_blob.is_cpu):
                cpu_logic, cpu_memory = engine.cpu_logic.handle_logic(p1_blob, p2_blob, ball, game_score, timer)
                p1_blob.cpu_memory = cpu_memory
                p1_blob.move(cpu_logic)
            else:
                p1_blob.move(pressed)
            if(p2_blob.is_cpu):
                cpu_logic, cpu_memory = engine.cpu_logic.handle_logic(p2_blob, p1_blob, ball, game_score, timer)
                p2_blob.cpu_memory = cpu_memory
                p2_blob.move(cpu_logic)
            else:
                p2_blob.move(pressed)
            p1_blob, p2_blob = ball.check_block_collisions(p1_blob, p2_blob)
            p2_blob, p1_blob = ball.check_block_collisions(p2_blob, p1_blob)
            ball.check_blob_ability(p1_blob)
            ball.check_blob_ability(p2_blob)
            if(p1_blob.kick_timer == 1):
                p1_blob.check_blob_collision(p2_blob)
                   
            if(p2_blob.kick_timer == 1):
                p2_blob.check_blob_collision(p1_blob)

            p1_blob.check_ability_collision(p2_blob, ball)
            p2_blob.check_ability_collision(p1_blob, ball)

            if(p2_blob.hp <= 0):
                    timer = 120
                    p2_ko = True
                    p1_blob.cooldown()
                    p1_blob.info['points_from_kos'] += 1
                    p2_blob.damage_flash_timer = 0
            
            if(p1_blob.hp <= 0):
                    timer = 120
                    p1_ko = True
                    p2_blob.cooldown()
                    p2_blob.info['points_from_kos'] += 1
                    p1_blob.damage_flash_timer = 0


            p1_blob.cooldown()
            p2_blob.cooldown()
            ball.move(p1_blob, p2_blob)
            p1_blob = ball.check_blob_collisions(p1_blob)
            p2_blob = ball.check_blob_collisions(p2_blob)
            if(ball.x_pos < 60 and ball.y_pos > 925): #Left Goal
                goal_scorer = 1
                goal_scored = True
                countdown = 60
                timer = 60
                p2_blob.info['points_from_goals'] += 1
                
            elif(ball.x_pos > 1745 and ball.y_pos > 925): #Right Goal
                goal_scorer = 0
                goal_scored = True
                countdown = 60
                timer = 60
                p1_blob.info['points_from_goals'] += 1
            if not (ruleset['time_limit'] == 0):
                time_limit -= 1
                if(time_limit <= 0):
                    print("TIME UP?!")
                    if(game_score[0] > game_score[1]):
                        winner_info = 1
                    elif(game_score[0] < game_score[1]):
                        winner_info = 2
                    else:
                        winner_info = 3
                    game_state = "casual_win"
            game_info['time'] += 1

        else:
            if(p1_ko):
                blob_ko(p1_blob)
                if(p1_blob.y_pos >= 1800):
                    game_state, winner_info = score_goal(1, goal_limit)
                    p1_ko = False
                    p1_blob.hp = p1_blob.max_hp
                    reset_round()
            if(p2_ko):
                blob_ko(p2_blob)
                if(p2_blob.y_pos >= 1800):
                    game_state, winner_info = score_goal(0, goal_limit)
                    p2_blob.hp = p2_blob.max_hp
                    p2_ko = False
                    reset_round()
            if(goal_scored):
                ball.image = engine.ball.type_to_image("goal_ball")
                ball.special_timer = 2
                ball.move(p1_blob, p2_blob)
                p1_blob.move([])
                p2_blob.move([])
                p1_blob.impact_land_frames = 0
                p2_blob.impact_land_frames = 0
                p1_blob.used_ability = ""
                p2_blob.used_ability = ""
                countdown -= 1
                if(countdown == 0):
                    game_state, winner_info = score_goal(goal_scorer, goal_limit)
                    goal_scored = False
                    goal_scorer = None
                    reset_round()
            timer -= 1

        if(game_state == "casual_win"):
            game_info["game_score"] = game_score
            game_info["time_seconds"] = round(game_info['time']/60, 2)
            try:
                game_info["avg_goal_time"] = round(game_info['time']/(game_score[0] + game_score[1]), 2)
                game_info["avg_goal_time_seconds"] = round(game_info['time_seconds']/(game_score[0] + game_score[1]) , 2)
            except:
                game_info['avg_goal_time'] = 0
                game_info['avg_goal_time_seconds'] = 0
            try:
                game_info['avg_collisions_per_goal'] = (ball.info['blob_standard_collisions'] + ball.info['blob_reflect_collisions'] + ball.info['blob_warp_collisions']) / (p1_blob.info['points_from_goals'] + p2_blob.info['points_from_goals'])
            except:
                game_info['avg_collisions_per_goal'] = 0
            with open('blob_ball_results.txt', 'a') as bbr:
                bbr.write("MATCH COMPLETED: " + time.ctime(time.time()))
                bbr.write("\n")
                bbr.write("RULESET: " + dumps(ruleset))
                bbr.write("\n")
                bbr.write("GENERAL INFO: " + dumps(game_info))
                bbr.write("\n")
                bbr.write("PLAYER 1: " + dumps(p1_blob.info))
                bbr.write("\n")
                bbr.write("PLAYER 2: " + dumps(p2_blob.info))
                bbr.write("\n")
                bbr.write("BALL: " + dumps(ball.info))
                bbr.write("\n")
                bbr.write("\n")
            
            update_game_stats(game_info, p1_blob, p2_blob, ball)
            update_mu_chart(game_score, p1_blob, p2_blob)
            print("Match end", time_limit, ruleset['time_limit'])
            return p1_blob, p2_blob, ball, game_score, timer, game_state, (winner_info, p1_blob, p2_blob, ball, game_score, game_info['time_seconds'])
    return p1_blob, p2_blob, ball, game_score, timer, game_state, time_limit

def clear_info_cache():
    global game_score
    global timer
    global countdown
    global time_limit
    global game_info
    global initialized
    global p1_blob
    global p2_blob
    global ball
    game_score = [0, 0]
    timer = 180
    countdown = 0
    time_limit = 3600
    game_info['time'] = 0
    initialized = False
    p1_blob = None
    p2_blob = None
    ball = None