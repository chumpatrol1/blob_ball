import pygame as pg
import sys
import engine.handle_input
import engine.blobs
import engine.ball

def initialize_players(p1_selected, p2_selected):
    p1_blob = engine.blobs.blob(type = p1_selected, player = 1, x_pos = 1600, facing = 'left')
    p2_blob = engine.blobs.blob(type = p2_selected, player = 2, x_pos = 100, facing = 'right')
    ball = engine.ball.ball()
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
score_goal = False

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
    game_score[winner] += 1
    timer = 180
    if(game_score[winner] >= goal_limit):
        return "casual_css"
    reset_round()
    return "casual_match"
    

def handle_gameplay(p1_selected, p2_selected):
    pressed = engine.handle_input.gameplay_input()
    global initialized
    global p1_blob
    global p2_blob
    global ball
    global game_score
    global timer
    global p1_ko
    global p2_ko
    goal_limit = 5
    game_state = "casual_match"

    def blob_ko(blob):
        blob.blob_ko()

    if not initialized:
        blobs = initialize_players(p1_selected, p2_selected)
        p1_blob = blobs[0]
        p2_blob = blobs[1]
        ball = blobs[2]
        initialized = True
    else:
        if(timer == 0):
            p1_blob.move(pressed)
            p2_blob.move(pressed)
            ball.check_block_collisions(p1_blob, p2_blob)
            ball.check_block_collisions(p2_blob, p1_blob)
            if(p1_blob.kick_timer == 1 and not p2_blob.kick_timer == 1):
                p1_blob.check_blob_collision(p2_blob)
                if(p2_blob.hp <= 0):
                    timer = 120
                    p2_ko = True
                    p1_blob.cooldown()
                    p2_blob.damage_flash_timer = 0
                    
            if(p2_blob.kick_timer == 1 and not p1_blob.kick_timer == 1):
                p2_blob.check_blob_collision(p1_blob)
                if(p1_blob.hp <= 0):
                    timer = 120
                    p1_ko = True
                    p2_blob.cooldown()
                    p1_blob.damage_flash_timer = 0
                    #p2_blob.kick_timer = 0
            p1_blob.cooldown()
            p2_blob.cooldown()
            ball.move()
            ball.check_blob_collisions(p1_blob)
            ball.check_blob_collisions(p2_blob)
            if(ball.x_pos < 60 and ball.y_pos > 925): #Left Goal
                game_state = score_goal(1, goal_limit)
                
            elif(ball.x_pos > 1745 and ball.y_pos > 925): #Right Goal
                game_state = score_goal(0, goal_limit)

        else:
            if(p1_ko):
                blob_ko(p1_blob)
                if(p1_blob.y_pos >= 1800):
                    game_state = score_goal(0, goal_limit)
                    p1_ko = False
                    p1_blob.hp = p1_blob.max_hp
                    reset_round()
            if(p2_ko):
                blob_ko(p2_blob)
                if(p2_blob.y_pos >= 1800):
                    game_state = score_goal(1, goal_limit)
                    p2_blob.hp = p2_blob.max_hp
                    p2_ko = False
                    reset_round()
            timer -= 1
        if(game_state == "casual_css"):
            initialized = False
            p1_blob = None
            p2_blob = None
            ball = None
            game_score = [0, 0]
            timer = 180
            countdown = 0
            return p1_blob, p2_blob, ball, game_score, timer, game_state
    return p1_blob, p2_blob, ball, game_score, timer, game_state