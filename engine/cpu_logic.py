import random

def handle_logic(blob, other_blob, ball, game_score, timer):
    '''
    Blob is the CPU blob
    Other_blob is the other blob
    Ball is the ball

    Returns pressed (the inputs that the blob will do)
    Returns logic_memory (which lets the blob remember what sort of playstyle or decisions it has done recently)
    '''

    '''
    There are 8 inputs that blobs will accept:
    left (Left input)
    right (Right input)
    up (Upwards input, does a jump)
    down (Downwards input, which can activate a focus while grounded, or a fastfall in the air)
    
    ability (Ability input, which can activate a special power. 
    Powers are usually either single input (ex: Gale, Spire) or held (ex: Fireball, Geyser))
    kick (Kick input, which does damage and smacks the ball really hard)
    blob (Block input, which protects against kicks and can stop the ball)
    boost (Boost input, which increases player stats greatly)
    '''

    '''
    Note to BoingK (8/30/2021):
    Feel free to play with whatever code you'd like to. Don't hesitate to DM me
    If the program compiles I'm fine with it, so don't hesitate to commit things to the dev build!
    Add whatever logic you'd like
    '''
    pressed = []
    logic_memory = blob.cpu_memory
    #Aggress/Defend?
    if ((blob.x_center < ball.x_center+60) and (blob.player != 1)) or ((blob.x_center > ball.x_center-60) and (blob.player == 1)):
        logic_memory = ['defensive']
    elif (abs(other_blob.x_center - ball.x_center)>200)and(((other_blob.facing=='left')and(other_blob.player==1))or((other_blob.facing=='right')and(other_blob.player!=1))):
        logic_memory = ['agressive']
    elif (abs(blob.x_center - ball.x_center) < 600) and (abs(blob.x_center - ball.x_center) < abs(other_blob.x_center - ball.x_center)):
        logic_memory = ['agressive']
    elif abs(other_blob.x_center - ball.x_center) < 500:
        if abs(blob.x_center - ball.x_center) > 500:
            logic_memory = ['agressive']
        if abs(blob.x_center - ball.x_center) < 500:
            logic_memory = ['defensive']
    else:
        logic_memory = ['agressive']
    #Jump?
    if (((blob.x_center - ball.x_center)>100) and (blob.player != 1)) or (((ball.x_center - blob.x_center)>100) and (blob.player == 1)) and (blob.y_center>ball.y_center):
        logic_memory.append('jump')


    #Logic for each strategy goes here
    if(blob.player == 1):
        if 'agressive' in logic_memory:
            pressed.append('right')
        if 'defensive' in logic_memory:
            pressed.append('left')
    else:
        if 'agressive' in logic_memory:
            pressed.append('left')
        if 'defensive' in logic_memory:
            pressed.append('right')
    if 'jump' in logic_memory:
        pressed.append('up')

    #Converts the logic to something readable by the blob's movement function
    if(blob.player == 1):
        for i in range(len(pressed)):
            pressed[i] = "p1_" + pressed[i]
    else:
        for i in range(len(pressed)):
            pressed[i] = "p2_" + pressed[i]

    return pressed, logic_memory
