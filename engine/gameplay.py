import pygame as pg
import sys
import engine.handle_input
import engine.blobs
import engine.ball
import time
from json import dumps, loads
from os import getcwd
cwd = getcwd()

def initialize_players(p1_selected, p2_selected, ruleset, settings):
    global goal_limit
    global time_limit
    global time_bonus
    p1_blob = engine.blobs.blob(species = p1_selected, player = 1, x_pos = 100, facing = 'right', special_ability_charge_base = ruleset['special_ability_charge_base'], danger_zone_enabled = ruleset['danger_zone_enabled'])
    p2_blob = engine.blobs.blob(species = p2_selected, player = 2, x_pos = 1600, facing = 'left', special_ability_charge_base = ruleset['special_ability_charge_base'], danger_zone_enabled = ruleset['danger_zone_enabled'])
    ball = engine.ball.ball()
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
    

def handle_gameplay(p1_selected, p2_selected, ruleset, settings):
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
        blobs = initialize_players(p1_selected, p2_selected, ruleset, settings)
        p1_blob = blobs[0]
        p2_blob = blobs[1]
        ball = blobs[2]
        
        initialized = True
    else:
        if(timer == 0):
            p1_blob.move(pressed)
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

            with open(cwd+'/saves/game_stats.txt', 'r') as statsdoc:
                game_stats = loads(statsdoc.readline())
            with open(cwd+'/saves/game_stats.txt', 'w') as statsdoc:
                game_stats['matches_played'] += 1
                game_stats['points_scored'] = game_stats['points_scored'] + game_info['game_score'][0] + game_info['game_score'][1]
                game_stats['points_from_goals'] = game_stats['points_from_goals'] + p1_blob.info['points_from_goals'] + p2_blob.info['points_from_goals']
                game_stats['points_from_kos'] = game_stats['points_from_kos'] + p1_blob.info['points_from_kos'] + p2_blob.info['points_from_kos']
                game_stats['damage_dealt'] = game_stats['damage_dealt'] + p1_blob.info['damage_taken'] + p2_blob.info['damage_taken']
                game_stats['kick_count'] = game_stats['kick_count'] + p1_blob.info['kick_count'] + p2_blob.info['kick_count']
                game_stats['block_count'] = game_stats['block_count'] + p1_blob.info['block_count'] + p2_blob.info['block_count']
                game_stats['boost_count'] = game_stats['boost_count'] + p1_blob.info['boost_count'] + p2_blob.info['boost_count']
                game_stats['parries'] = game_stats['parries'] + p1_blob.info['parries'] + p2_blob.info['parries']
                game_stats['clanks'] = game_stats['clanks'] + p1_blob.info['clanks'] + p2_blob.info['clanks']
                game_stats['blob_x_distance_moved'] = game_stats['blob_x_distance_moved'] + round(p1_blob.info['x_distance_moved'] + p2_blob.info['x_distance_moved'])
                game_stats['wavebounces'] = game_stats['wavebounces'] + p1_blob.info['wavebounces'] + p2_blob.info['wavebounces']
                game_stats['jumps'] = game_stats['jumps'] + p1_blob.info['jumps'] + p2_blob.info['jumps']
                game_stats['jump_cancelled_focuses'] = game_stats['jump_cancelled_focuses'] + p1_blob.info['jump_cancelled_focuses'] + p2_blob.info['jump_cancelled_focuses']
                game_stats['time_focused_seconds'] = round(game_stats['time_focused_seconds'] + p1_blob.info['time_focused_seconds'] + p2_blob.info['time_focused_seconds'])
                game_stats['time_airborne_seconds'] = round(game_stats['time_airborne_seconds'] + p1_blob.info['time_airborne_seconds'] + p2_blob.info['time_airborne_seconds'])
                game_stats['time_grounded_seconds'] = round(game_stats['time_grounded_seconds'] + p1_blob.info['time_grounded_seconds'] + p2_blob.info['time_grounded_seconds'])
                game_stats['blob_standard_collisions'] = game_stats['blob_standard_collisions'] + ball.info['blob_standard_collisions']
                game_stats['blob_reflect_collisions'] = game_stats['blob_reflect_collisions'] + ball.info['blob_reflect_collisions']
                game_stats['blob_warp_collisions'] = game_stats['blob_warp_collisions'] + ball.info['blob_warp_collisions']
                game_stats['ball_kicked'] = game_stats['ball_kicked'] + ball.info['kicked']
                game_stats['ball_blocked'] = game_stats['ball_blocked'] + ball.info['blocked']
                game_stats['ball_x_distance_moved'] = round(game_stats['ball_x_distance_moved'] + ball.info['x_distance_moved'])
                game_stats['ball_y_distance_moved'] = round(game_stats['ball_y_distance_moved'] + ball.info['y_distance_moved'])
                game_stats['ball_floor_collisions'] = game_stats['ball_floor_collisions'] + ball.info['floor_collisions']
                game_stats['ball_goal_collisions'] = game_stats['ball_goal_collisions'] + ball.info['goal_collisions']
                game_stats['ball_ceiling_collisions'] = game_stats['ball_ceiling_collisions'] + ball.info['ceiling_collisions']
                game_stats['ball_wall_collisions'] = game_stats['ball_wall_collisions'] + ball.info['wall_collisions']
                
                
                game_stats['time_in_game'] = round(game_stats['time_in_game'] + game_info['time_seconds'])
                statsdoc.write(dumps(game_stats))
            
            game_score = [0, 0]
            timer = 180
            countdown = 0
            time_limit = 3600
            game_info['time'] = 0
            initialized = False
            p1_blob = None
            p2_blob = None
            ball = None
            return p1_blob, p2_blob, ball, game_score, timer, game_state, (winner_info)
    return p1_blob, p2_blob, ball, game_score, timer, game_state, time_limit