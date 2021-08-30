def handle_logic(blob, other_blob, ball, game_score, timer):
    '''
    Blob is the CPU blob
    Other_blob is the other blob
    Ball is the ball
    '''
    pressed = []
    if(ball.x_center > blob.x_center):
        pressed.append('right')
    else:
        pressed.append('left')

    if(blob.player == 1):
        for i in range(len(pressed)):
            pressed[i] = "p1_" + pressed[i]
    else:
        for i in range(len(pressed)):
            pressed[i] = "p2_" + pressed[i]
    print(pressed)
    return pressed