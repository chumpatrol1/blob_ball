# INITIALIZER
import os
from json import loads, dumps

game_version = '0.17.0b'

def check_folders(cwd):
    if(not os.path.isdir(cwd+"/config")):
        os.mkdir(cwd+"/config")
        print("Created config folder")

    if(not os.path.isdir(cwd+"/saves")):
        os.mkdir(cwd+"/saves")
        print("Created saves folder")

    if(not os.path.isdir(cwd+"/screenshots")):
        os.mkdir(cwd+"/screenshots")
        print("Created screenshots folder")

    if(not os.path.isdir(cwd+"/replays")):
        os.mkdir(cwd+"/replays")
        print("Created replays folder")

def initialize_game_stats(cwd):
    game_stat_dict = {
    #Stats about the state of the game
    'original_version': game_version, #Version this file was created on
    'times_bb_started': 0, #Number of times Blob Ball was started up
    'time_open': 0, #Time in seconds.mm that the game has been open
    'time_in_game': 0, #Time in seconds.mm that was spent in an actual match
    'blobs_unlocked': 1, #Number of blobs unlocked
    'costumes_unlocked': 0, #Number of costumes unlocked
    'backgrounds_unlocked': 0, #Number of backgrounds unlocked
    'most_played_character': 'quirkless', #Most played character
    'tutorial_completion_count': 0,
    'fastest_tutorial_completion': 360000,

    #Stats about game/match info
    'matches_played': 0, #Number of matches completed
    'points_scored': 0, #Total points scored (should be sum of bottom 2)
    'points_from_goals': 0, #Total points scored from kicking the ball into the goal
    'points_from_kos': 0, #Total points scored from kills

    #Stats relating directly to blobs
    'damage_dealt': 0, #Total damage accumulated
    'kick_count': 0, #Total amount of times the kick button was pressed
    'block_count': 0, #Total amount of times the block button was pressed
    'boost_count': 0, #Total amount of times the boost button was pressed
    'parries': 0, #Total number of kicks or attacks deflected by blocks
    'clanks': 0, #Total numbers of kicks deflected by other kicks
    'blob_x_distance_moved': 0, #Total distance moved by blobs
    'wavebounces': 0, #Total wavebounces performed
    'jumps': 0, #Total jumps
    'jump_cancelled_focuses': 0, #Total focuses cancelled by jumps
    'time_focused_seconds': 0, #Total time spent focusing
    'time_airborne_seconds': 0, #Total time spent in the air
    'time_grounded_seconds': 0, #Total time spent on the ground

    'blob_standard_collisions': 0, #Normal ball collisions (hitting the top)
    'blob_reflect_collisions': 0, #Reflecting ball collisions (hitting the bottom)
    'blob_warp_collisions': 0, #Warp ball collisions (ball warps above the blob)
    'ball_kicked': 0, #Times hit with a kick
    'ball_blocked': 0, #Times hit with a block
    'ball_x_distance_moved': 0, #Distance moved horizontally
    'ball_y_distance_moved': 0, #Distance moved vertically
    'ball_wall_collisions': 0, #Hitting a wall
    'ball_ceiling_collisions': 0, #Hitting the ceiling
    'ball_floor_collisions': 0, #Bouncing off of the floor specifically
    'ball_goal_collisions': 0, #Goalpost collisions
        }

    try:
        with open(cwd+'/saves/game_stats.txt', 'r') as statsdoc:
            n_game_stat_dict = loads(statsdoc.readline())
            for key in game_stat_dict:
                if not key in n_game_stat_dict:
                    n_game_stat_dict[key] = game_stat_dict[key]
            game_stat_dict = n_game_stat_dict
        with open(cwd+'/saves/game_stats.txt', 'w') as statsdoc:
            statsdoc.write(dumps(game_stat_dict))
    except:
        with open(cwd+'/saves/game_stats.txt', 'w') as statsdoc:
            statsdoc.write(dumps(game_stat_dict))
            print("game_stats.txt written")



    return game_stat_dict

def load_default_ruleset():
    player_mods = {
        'max_hp': None,
        'top_speed': None,
        'traction': None,
        'friction': None,
        'gravity': None,
        'kick_cooldown_rate': None,
        'block_cooldown_rate': None,
        'boost_cost': None,
        'boost_cooldown_max': None,
        'boost_duration': None,

        'special_ability_cost': None,
        'special_ability_maintenance': None,
        'special_ability_max': None,
        'special_ability_cooldown': None,
        'special_ability_delay': None,
        'special_ability_duration': None,
    }
    ruleset = {
        'version': game_version,
        'goal_limit': 5,
        'time_limit': 3600,
        'time_bonus': 600,
        'special_ability_charge_base': 1,
        'danger_zone_enabled': True,
        'p1_modifiers': dict(player_mods),
        'p2_modifiers': player_mods,
        'hp_regen': 0,
    }
    return ruleset

def initialize_ruleset(cwd):
    ruleset = load_default_ruleset()

    def open_ruleset(ruleset):
        try:
            with open(cwd+'/config/ruleset.txt', 'r') as rulesetdoc:
                n_ruleset = loads(rulesetdoc.readline())
                for key in ruleset:
                    if not key in n_ruleset:
                        n_ruleset[key] = ruleset[key]
            ruleset = n_ruleset
            with open(cwd+'/config/ruleset.txt', 'w') as rulesetdoc:
                ruleset['version'] = game_version
                rulesetdoc.write(dumps(ruleset))
            return ruleset
        except:
            with open(cwd+'/config/ruleset.txt', 'w') as rulesetdoc:
                rulesetdoc.write(dumps(ruleset))
            return ruleset

    ruleset = open_ruleset(ruleset)
    return ruleset

def load_matchup_chart(cwd):
    try:
        with open(cwd+'/saves/matchup_chart.txt', 'r') as statsdoc:
            #print("Sucessfully Opened MU Chart")
            pass
    except:
        with open(cwd+'/saves/matchup_chart.txt', 'w') as statsdoc:
                statsdoc.write(dumps({}))
                print("Created MU Chart")

def initialize_settings(cwd):
    settings = {
    'hd_backgrounds': True,
    'hd_blobs': True,
    'smooth_scaling': True,
    'music_volume': 10,
    'sound_volume': 10,
    'ui_mode': False, # True if shown on top, False is shown on bottom
    }

    try:
        with open(cwd+'/config/settings.txt', 'r') as settingsdoc:
            n_settings = loads(settingsdoc.readline())
            for key in settings:
                if not key in n_settings:
                    n_settings[key] = settings[key]
            settings = n_settings
    except:
        with open(cwd+'/config/settings.txt', 'w') as settingsdoc:
            settingsdoc.write(dumps(settings))
    return settings

def check_existing_directory(cwd):
    '''
    Checks to see if the following folders exist. If they don't, create them!
    '''
    if not(os.path.isdir(cwd)): # Blob Ball Roaming
        print(cwd)
        os.mkdir(cwd)
    if not(os.path.isdir(cwd + '/config')): # Config folder
        os.mkdir(cwd+'/config') 
    if not(os.path.isdir(cwd + '/saves')): # Saves folder
        os.mkdir(cwd+'/saves')
    if not(os.path.isdir(cwd + '/screenshots')): # Screenshots folder
        os.mkdir(cwd+'/screenshots')
    if not(os.path.isdir(cwd + '/replays')): # Replays folder
        os.mkdir(cwd+'/replays')

def return_game_version():
    return game_version
