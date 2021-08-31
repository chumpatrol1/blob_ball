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
    convertdict = {
        '1': {
            'back': 'left',
            'forward': 'right',
            'jump': 'up',
            'down': 'down'
            'ability': 'ability',
            'kick': 'kick',
            'block': 'blob',
            'boost': 'boost'},
        '2': {
            'back': 'right',
            'forward': 'left',
            'jump': 'up',
            'down': 'down'
            'ability': 'ability',
            'kick': 'kick',
            'block': 'blob',
            'boost': 'boost'}
        }

    #Decide which strategy to use
    if abs(blob.x_center - ball.x_center) > (abs(other_blob.x_center - ball.x_center)+10):
        logic_memory = ['defensive']
    else:
        logic_memory = ['aggressive']

    #Logic for each strategy goes here
    inputstoconvert = []
    if 'defensive' in logic_memory:
        inputstoconvert.append('back')
    if 'aggresive' in logic_memory:
        inputstoconvert.append('forward')

    #Convert inputs to something the engine can read    
    for tupin in inputstoconvert:
        pressed.append(convertdict[str(blob.player)][tupin])

    #Converts the logic to something readable by the blob's movement function
    if(blob.player == 1):
        for i in range(len(pressed)):
            pressed[i] = "p1_" + pressed[i]
    else:
        for i in range(len(pressed)):
            pressed[i] = "p2_" + pressed[i]

    return pressed, logic_memory
