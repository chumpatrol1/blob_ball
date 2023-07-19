from json import loads, dumps
from os import getenv
from engine.unlock_event import createUnlockEvent
cwd = getenv('APPDATA')+'/BlobBall'

def attempt_blob_unlocks(game_stats):
    blob_unlock_requirements = {
        2: "fire",
        4: "ice",
        6: "water",
        8: "rock",
        10: "lightning",
        12: "wind",
        15: "judge",
        20: "doctor",
        25: "king",
        30: "cop",
        35: "boxer",
        40: "mirror",
        45: "fisher",
        52: "glue",
        59: "arcade",
        66: "joker",
        74: "taco",
        82: "cactus",
        90: "merchant",
        100: "bubble",
    }
    
    blobs_unlocked = 0
    for dict_key in blob_unlock_requirements:
        if(game_stats['matches_played'] >= dict_key):
            if(createUnlockEvent(blob_unlock_requirements[dict_key], 0)):
                blobs_unlocked += 1

    return blobs_unlocked

def attempt_costume_unlocks(mu_chart, p1_blob, p2_blob):
    costume_unlock_requirements = { # Key is Blob Species, Value is how we look up the costume when unlocking. The / is important!
        "quirkless": {10: "quirkless/grayscale_1"},
        "fire": {10: "fire/grayscale_1"},
        "ice": {10: "ice/grayscale_1"},
        "water": {10: "water/grayscale_1"},
        "rock": {10: "rock/grayscale_1"},
        "lightning": {10: "lightning/grayscale_1"},
        "wind": {10: "wind/grayscale_1"},
        "judge": {10: "judge/grayscale_1"},
        "doctor": {10: "doctor/grayscale_1"},
        "king": {10: "king/grayscale_1"},
        "cop": {10: "cop/grayscale_1"},
        "boxer": {10: "boxer/grayscale_1"},
        "mirror": {10: "mirror/grayscale_1"},
        "fisher": {10: "fisher/grayscale_1", 20: "fisher/jew_2"},
        "glue": {10: "glue/grayscale_1"},
        "arcade": {10: "arcade/grayscale_1"},
        "joker": {10: "joker/grayscale_1", 20: "joker/red_2", 30: "joker/mosaic_3"},
        "taco": {10: "taco/grayscale_1"},
        "cactus": {10: "cactus/grayscale_1"},
        "merchant": {10: "merchant/grayscale_1"},
        "bubble": {10: "bubble/grayscale_1"},
    }
    blobs_unlocked = 0
    try:
        for dict_key in costume_unlock_requirements[p1_blob.species]:
            if(mu_chart[p1_blob.species]['total'] >= dict_key):
                if(createUnlockEvent(costume_unlock_requirements[p1_blob.species][dict_key], 2)):
                    blobs_unlocked += 1
    except KeyError:
        print("No Costumes Available")

    try:
        for dict_key in costume_unlock_requirements[p2_blob.species]:
            if(mu_chart[p2_blob.species]['total'] >= dict_key):
                if(createUnlockEvent(costume_unlock_requirements[p2_blob.species][dict_key], 2)):
                    blobs_unlocked += 1
    except KeyError:
        print("No Costumes Available")

    return blobs_unlocked

def update_game_stats(game_info, p1_blob, p2_blob, ball):
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
        
        game_stats['blobs_unlocked'] += attempt_blob_unlocks(game_stats)


        game_stats['time_in_game'] = round(game_stats['time_in_game'] + game_info['time_seconds'])
        statsdoc.write(dumps(game_stats))

def update_mu_chart(game_score, p1_blob, p2_blob):
    try:
        with open(cwd+'/saves/matchup_chart.txt', 'r') as muchart:
                    mu_chart = loads(muchart.readline())
    except:
        mu_chart = {}
    with open(cwd+'/saves/matchup_chart.txt', 'w') as muchart:
        if(game_score[0] > game_score[1]):
            tied = False
            winner = p1_blob.species
            loser = p2_blob.species
        elif(game_score[1] > game_score[0]):
            tied = False
            winner = p2_blob.species
            loser = p1_blob.species
        else:
            tied = True
            winner = p1_blob.species
            loser = p2_blob.species
        if(not tied):
            if winner in mu_chart: #Entry for the winner
                if loser in mu_chart[winner]: #Has this MU been played before?
                    mu_chart[winner][loser][0] += 1
                else:
                    mu_chart[winner][loser] = [1, 0, 0] # Format is W/L/T
                if(not 'wins' in mu_chart[winner]):
                    mu_chart[winner]['wins'] = 1
                else:
                    mu_chart[winner]['wins'] += 1
            else:
                mu_chart[winner] = dict()
                mu_chart[winner][loser] = [1, 0, 0]
                mu_chart[winner]['wins'] = 1

            if loser in mu_chart: #Entry for the winner
                if winner in mu_chart[loser]: #Has this MU been played before?
                    mu_chart[loser][winner][1] += 1
                else:
                    mu_chart[loser][winner] = [0, 1, 0]
                if(not 'losses' in mu_chart[loser]):
                    mu_chart[loser]['losses'] = 1
                else:
                    mu_chart[loser]['losses'] += 1
            else:
                mu_chart[loser] = dict()
                mu_chart[loser][winner] = [0, 1, 0]
                mu_chart[loser]['losses'] = 1
        else:
            if winner in mu_chart: #Entry for the winner
                if loser in mu_chart[winner]: #Has this MU been played before?
                    mu_chart[winner][loser][2] += 1
                else:
                    mu_chart[winner][loser] = [0, 0, 1]
                if 'ties' not in mu_chart[winner]:
                    mu_chart[winner]['ties'] = 1
                else:
                    mu_chart[winner]['ties'] += 1
            else:
                mu_chart[winner] = dict()
                mu_chart[winner][loser] = [0, 0, 1]
                mu_chart[winner]['ties'] = 1

            if loser in mu_chart: #Entry for the winner
                if winner in mu_chart[loser]: #Has this MU been played before?
                    mu_chart[loser][winner][2] += 1
                else:
                    mu_chart[loser][winner] = [0, 0, 1]
                if 'ties' not in mu_chart[loser]:
                    mu_chart[winner]['ties'] = 1
                else:
                    mu_chart[winner]['ties'] += 1
            else:
                mu_chart[loser] = dict()
                mu_chart[loser][winner] = [0, 0, 1]
                mu_chart[loser]['ties'] = 1

        if not('total' in mu_chart[loser]):
            mu_chart[loser]['total'] = 0

        if not('total' in mu_chart[winner]):
            mu_chart[winner]['total'] = 0
        mu_chart[loser]['total'] += 1
        mu_chart[winner]['total'] += 1

        with open(cwd+'/saves/game_stats.txt', 'r') as statsdoc:
            game_stats = loads(statsdoc.readline())
        with open(cwd+'/saves/game_stats.txt', 'w') as statsdoc:
            game_stats['costumes_unlocked'] += attempt_costume_unlocks(mu_chart, p1_blob, p2_blob)
            statsdoc.write(dumps(game_stats))

        muchart.write(dumps(mu_chart))

        most_played_character = ""
        with open(cwd+'/saves/game_stats.txt', 'r') as statsdoc:
            game_stats = loads(statsdoc.readline())
        most_played_character = game_stats['most_played_character']
        if(most_played_character in mu_chart):
            if(mu_chart[loser]['total'] > mu_chart[most_played_character]['total']):
                most_played_character = loser

            if(mu_chart[winner]['total'] > mu_chart[most_played_character]['total']):
                most_played_character = winner
        else:
            most_played_character = winner

        game_stats['most_played_character'] = most_played_character
            
def save_tutorial_stats(info_getter):
    '''
    Info_Getter is the output of tutorial.handle_tutorial.
    Increments tutorial completion by 1, and sets the record of the tutorial.

    Inputs:
        - info_getter: Array with at least 5 elements. The 5th one represents an integer
        - game_stats.txt: Text file that stores player statistics

    Outputs:
        - game_stats.txt: Text file that stores player statistics
    '''
    with open(cwd+'/saves/game_stats.txt', 'r') as statsdoc:
        game_stats = loads(statsdoc.readline())
    with open(cwd+'/saves/game_stats.txt', 'w') as statsdoc:
        game_stats['tutorial_completion_count'] += 1
        completion_timer = info_getter[4]
        if(completion_timer < game_stats['fastest_tutorial_completion']):
            game_stats['fastest_tutorial_completion'] = completion_timer

        statsdoc.write(dumps(game_stats))