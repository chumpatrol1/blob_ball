from json import loads, dumps
from copy import deepcopy
# The original selector
css_selector_list_blobs = [
    ["back", "quirkless", "quirkless", "quirkless", "quirkless", "quirkless", "quirkless", "quirkless",],
    ["rules", "quirkless", "quirkless", "quirkless", "quirkless", "quirkless", "quirkless", "quirkless",],
    ["settings", "quirkless", "quirkless", "quirkless", "quirkless", "quirkless", "quirkless", "quirkless",],
    ["almanac", "quirkless", "quirkless", "quirkless", "quirkless", "quirkless", "quirkless", "quirkless",],
    ["back", "quirkless", "quirkless", "quirkless", "quirkless", "quirkless", "quirkless", "quirkless",],
]

original_css_display_list_blobs = [ #Creates an array of arrays, which contains the image to use, it's name, and special ability
[["/css_icons/back_arrow.png", "Back", ""], ["/blobs/quirkless_blob.png", "Quirkless Blob", "No Ability"], ["/blobs/fire_blob.png", "Fire Blob", "Fireball"], ["/blobs/ice_blob.png", "Ice Blob", "Snowball"], ["/blobs/water_blob.png", "Water Blob", "Geyser"], ["/blobs/rock_blob.png", "Rock Blob", "Spire"], ["/blobs/lightning_blob.png", "Lightning Blob", "Thunderbolt"], ["/blobs/wind_blob.png", "Wind Blob", "Gale"],],
[["/css_icons/rules_icon.png", "Rules", ""], ["/blobs/judge_blob.png", "Judge Blob", "C&D"], ["/blobs/doctor_blob.png", "Doctor Blob", "Pill"], ["/blobs/king_blob.png", "King Blob", "Tax"], ["/blobs/cop_blob.png", "Cop Blob", "Stoplight"], ["/blobs/boxer_blob.png", "Boxer Blob", "Starpunch"], ["/blobs/mirror_blob.png", "Mirror Blob", "Reflect"], ["/blobs/fisher_blob.png", "Fisher Blob", "Hook"],],
[["/css_icons/gear_icon.png", "Settings", ""], ["/blobs/glue_blob.png", "Glue Blob", "Gluegun"], ["/blobs/quirkless_blob.png", "", ""], ["/blobs/quirkless_blob.png", "", ""], ["/blobs/quirkless_blob.png", "", ""], ["/blobs/quirkless_blob.png", "", ""], ["/blobs/quirkless_blob.png", "", ""], ["/blobs/quirkless_blob.png", "", ""],],
[["/css_icons/almanac_icon.png", "Almanac", ""], ["/blobs/quirkless_blob.png", "", ""], ["/blobs/quirkless_blob.png", "", ""], ["/blobs/quirkless_blob.png", "", ""], ["/blobs/quirkless_blob.png", "", ""], ["/blobs/quirkless_blob.png", "", ""], ["/blobs/quirkless_blob.png", "", ""], ["/blobs/quirkless_blob.png", "", ""],],
[["/css_icons/cpu_icon.png", "Toggle CPU", ""], ["/blobs/quirkless_blob.png", "", ""], ["/blobs/quirkless_blob.png", "", ""], ["/blobs/quirkless_blob.png", "", ""], ["/blobs/quirkless_blob.png", "", ""], ["/blobs/quirkless_blob.png", "", ""], ["/blobs/quirkless_blob.png", "", ""], ["/blobs/quirkless_blob.png", "", ""],],
]

css_display_list_blobs = deepcopy(original_css_display_list_blobs) #Creates an array of arrays, which contains the image to use, it's name, and special ability


css_location_dict_blobs = { # Stores every location to loop through. The key is a location, the value is cross checked with blob_unlock_dict
    (1, 0): "quirkless",
    (2, 0): "fire",
    (3, 0): "ice",
    (4, 0): "water",
    (5, 0): "rock",
    (6, 0): "lightning",
    (7, 0): "wind",
    (1, 1): "judge",
    (2, 1): "doctor",
    (3, 1): "king",
    (4, 1): "cop",
    (5, 1): "boxer",
    (6, 1): "mirror",
    (7, 1): "fisher",
    (1, 2): "glue",
    (2, 2): "coming_soon",
    (3, 2): "coming_soon",
    (4, 2): "coming_soon",
    (5, 2): "coming_soon",
    (6, 2): "coming_soon",
    (7, 2): "coming_soon",
    (1, 3): "coming_soon",
    (2, 3): "coming_soon",
    (3, 3): "coming_soon",
    (4, 3): "coming_soon",
    (5, 3): "coming_soon",
    (6, 3): "coming_soon",
    (7, 3): "coming_soon",
    (1, 4): "coming_soon",
    (2, 4): "coming_soon",
    (3, 4): "coming_soon",
    (4, 4): "coming_soon",
    (5, 4): "coming_soon",
    (6, 4): "coming_soon",
    (7, 4): "coming_soon",
}

blob_unlock_dict = { # Whether a given blob has been unlocked or not
    "quirkless": True,
    "fire": False,
    "ice": False,
    "water": False,
    "rock": False,
    "lightning": False,
    "wind": False,
    "judge": False,
    "doctor": False,
    "king": False,
    "cop": False,
    "boxer": False,
    "mirror": False,
    "fisher": False,
    "glue": False,
}

def load_blob_unlocks(cwd):
    global blob_unlock_dict
    try:
        with open(cwd + "/saves/blob_unlocks.txt", "r") as blobunlockdoc:
            new_unlock_dict = loads(blobunlockdoc.readline())
            for blob in blob_unlock_dict:
                if blob not in new_unlock_dict:
                    new_unlock_dict[blob] = False
        
        blob_unlock_dict = new_unlock_dict

        with open(cwd + "/saves/blob_unlocks.txt", "w") as blobunlockdoc:
            blobunlockdoc.write(dumps(blob_unlock_dict))
        
    except:
        with open(cwd + "/saves/blob_unlocks.txt", "w") as blobunlockdoc:
            blobunlockdoc.write(dumps(blob_unlock_dict))

unlock_milestones = [0, 2, 4, 6, 8, 10, 12,\
    15, 20, 25, 30, 35, 40, 45,\
        52, 59, 66, 74, 82, 90,\
    100, 110, 120, 130, 140, 150, 160,\
    165, 180, 195, 210, 225, 240, 255]

def update_css_blobs(cwd):
    global blob_unlock_dict
    global css_selector_list_blobs
    global css_display_list_blobs

    with open(cwd+'/saves/game_stats.txt', 'r') as statsdoc:
            game_stats = loads(statsdoc.readline())

    unlock_slot = 0
    for y in range(0, 5):
        for x in range(1, 8):
            location = (x, y)
            if location in css_location_dict_blobs and css_location_dict_blobs[location] == "coming_soon":
                css_display_list_blobs[y][x] = ["/blobs/shadow_blob.png", "???", "Coming soon!"]
            elif location in css_location_dict_blobs and blob_unlock_dict[css_location_dict_blobs[location]]:
                blob_id = css_location_dict_blobs[location]
                css_selector_list_blobs[y][x] = blob_id
                css_display_list_blobs[y][x] = original_css_display_list_blobs[y][x]
            else:
                css_display_list_blobs[y][x] = ["/blobs/locked_blob.png", "Unlock Me!", str(game_stats['matches_played']) + "/" + str(unlock_milestones[unlock_slot]) + " Matches Complete"]
            unlock_slot += 1
            #if location in if_blob_shadow:
                #css_display_list_blobs[y][x] = ["/blobs/shadow_blob.png", "Bug", "Coming soon!"]

def unlock_blob(blob, cwd):
    global blob_unlock_dict
    if blob in blob_unlock_dict and not blob_unlock_dict[blob]:
        with open(cwd + "/saves/blob_unlocks.txt", "r") as blobunlockdoc:
            blob_unlock_dict = loads(blobunlockdoc.readline())
        blob_unlock_dict[blob] = True
        with open(cwd + "/saves/blob_unlocks.txt", "w") as blobunlockdoc:
            blobunlockdoc.write(dumps(blob_unlock_dict))
    else:
        raise ValueError("Blob already unlocked!")


def return_blob_unlocks():
    global blob_unlock_dict
    return blob_unlock_dict

def return_css_selector_blobs():
    global css_selector_list_blobs
    return css_selector_list_blobs

def return_css_display_blobs():
    global css_display_list_blobs
    return css_display_list_blobs


'''MEDALS'''
original_css_display_list_medals = [ # Format: [Image, Name, Description]
    [["/css_icons/back_arrow.png", "Back", ""], ["/medals/", "Goal!", "Score a point by kicking the ball into the goal!"], ["/medals/", "KO!", "Score a point by kicking a player into unconsciousness!"], ["/medals/", "Parry This!", "Use your block to nullify an incoming attack!"], ["/medals/", "Ball Stopper", "Use your block to completely stop the ball"], ["/medals/", "Clash of the Blobs", "Cancel out the kick of an opponent with a kick of your own"], ["/medals/", "Power Up!", "Increase your speed and damage with a boost"], ["/medals/", "Damage Stacking", "Deal 4 damage with a single kick!"], ["/medals/", "Ready and Able", "Use a Blob's ability!"], ["/medals/", "Goal!", "Score a point by kicking the ball into the goal!"], ],
    [["/medals/", "Goal!", "Score a point by kicking the ball into the goal!"], ["/medals/", "Goal!", "Score a point by kicking the ball into the goal!"], ["/medals/", "Goal!", "Score a point by kicking the ball into the goal!"], ["/medals/", "Goal!", "Score a point by kicking the ball into the goal!"], ["/medals/", "Goal!", "Score a point by kicking the ball into the goal!"], ["/medals/", "Goal!", "Score a point by kicking the ball into the goal!"], ["/medals/", "Goal!", "Score a point by kicking the ball into the goal!"], ["/medals/", "Goal!", "Score a point by kicking the ball into the goal!"], ["/medals/", "Goal!", "Score a point by kicking the ball into the goal!"], ],
    [["/medals/", "Goal!", "Score a point by kicking the ball into the goal!"], ["/medals/", "Goal!", "Score a point by kicking the ball into the goal!"], ["/medals/", "Goal!", "Score a point by kicking the ball into the goal!"], ["/medals/", "Goal!", "Score a point by kicking the ball into the goal!"], ["/medals/", "Goal!", "Score a point by kicking the ball into the goal!"], ["/medals/", "Goal!", "Score a point by kicking the ball into the goal!"], ["/medals/", "Goal!", "Score a point by kicking the ball into the goal!"], ["/medals/", "Goal!", "Score a point by kicking the ball into the goal!"], ["/medals/", "Goal!", "Score a point by kicking the ball into the goal!"], ],
    [["/medals/", "Goal!", "Score a point by kicking the ball into the goal!"], ["/medals/", "Goal!", "Score a point by kicking the ball into the goal!"], ["/medals/", "Goal!", "Score a point by kicking the ball into the goal!"], ["/medals/", "Goal!", "Score a point by kicking the ball into the goal!"], ["/medals/", "Goal!", "Score a point by kicking the ball into the goal!"], ["/medals/", "Goal!", "Score a point by kicking the ball into the goal!"], ["/medals/", "Goal!", "Score a point by kicking the ball into the goal!"], ["/medals/", "Goal!", "Score a point by kicking the ball into the goal!"], ["/medals/", "Goal!", "Score a point by kicking the ball into the goal!"], ],
    [["/medals/", "Goal!", "Score a point by kicking the ball into the goal!"], ["/medals/", "Goal!", "Score a point by kicking the ball into the goal!"], ["/medals/", "Goal!", "Score a point by kicking the ball into the goal!"], ["/medals/", "Goal!", "Score a point by kicking the ball into the goal!"], ],
    ]

css_selector_list_medals = [
    ["back", "questionmedal", "questionmedal", "questionmedal", "questionmedal", "questionmedal", "questionmedal", "questionmedal",],
    ["rules", "questionmedal", "questionmedal", "questionmedal", "questionmedal", "questionmedal", "questionmedal", "questionmedal",],
    ["settings", "questionmedal", "questionmedal", "questionmedal", "questionmedal", "questionmedal", "questionmedal", "questionmedal",],
    ["almanac", "questionmedal", "questionmedal", "questionmedal", "questionmedal", "questionmedal", "questionmedal", "questionmedal",],
    ["back", "questionmedal", "questionmedal", "questionmedal", "questionmedal", "questionmedal", "questionmedal", "questionmedal",],
]

css_display_list_medals = deepcopy(original_css_display_list_medals)

css_location_dict_medals = {
    (1, 0): "goal",
    (2, 0): "ko",
    (3, 0): "parry_this",
    (4, 0): "ball_stop",
    (5, 0): "clash_of_the_blobs",
    (6, 0): "power_up",
    (7, 0): "damage_stacking",
	(1, 1): "rule_breaker",
	(2, 1): "questionmedal",
	(3, 1): "questionmedal",
	(4, 1): "questionmedal",
	(5, 1): "questionmedal",
    (6, 1): "questionmedal",
    (7, 1): "questionmedal",
    (1, 2): "questionmedal",
    (2, 2): "questionmedal",
    (3, 2): "questionmedal",
    (4, 2): "questionmedal",
    (5, 2): "questionmedal",
    (6, 2): "questionmedal",
    (7, 2): "questionmedal",
    (1, 3): "questionmedal",
    (2, 3): "questionmedal",
    (3, 3): "questionmedal",
    (4, 3): "questionmedal",
    (5, 3): "questionmedal",
    (6, 3): "questionmedal",
    (7, 3): "questionmedal",
    (1, 4): "questionmedal",
    (2, 4): "questionmedal",
    (3, 4): "questionmedal",
    (4, 4): "questionmedal",
    (5, 4): "questionmedal",
    (6, 4): "questionmedal",
    (7, 4): "questionmedal",
}

medal_unlock_dict = {
    "total": 0,
    "goal": False,
    "ko": False,
    "parry_this": False,
    "ball_stop": False,
    "clash_of_the_blobs": False,
    "power_up": False,
    "damage_stacking": False,
}

def load_medal_unlocks(cwd):
    global medal_unlock_dict
    try:
        with open(cwd + "/saves/medal_unlocks.txt", "r") as medalunlockdoc:
            new_unlock_dict = loads(medalunlockdoc.readline())
            for medal in medal_unlock_dict:
                if medal not in new_unlock_dict:
                    new_unlock_dict[medal] = False
        
        medal_unlock_dict = new_unlock_dict

        with open(cwd + "/saves/medal_unlocks.txt", "w") as medalunlockdoc:
            medalunlockdoc.write(dumps(medal_unlock_dict))
        
    except:
        with open(cwd + "/saves/medal_unlocks.txt", "w") as medalunlockdoc:
            medalunlockdoc.write(dumps(medal_unlock_dict))

def update_css_medals(cwd):
    global medal_unlock_dict
    global css_selector_list_medals
    global css_display_list_medals

    with open(cwd+'/saves/medals.txt', 'r') as statsdoc:
            game_stats = loads(statsdoc.readline())

def unlock_medal(medal, cwd):
    global medal_unlock_dict
    if medal in medal_unlock_dict and not medal_unlock_dict[medal]:
        with open(cwd + "/saves/medals.txt", "r") as medaldoc:
            medal_unlock_dict = loads(medaldoc.readline())
        medal_unlock_dict[medal] = True
        medal_unlock_dict['total'] += 1
        with open(cwd + "/saves/medals.txt", "w") as medaldoc:
            medaldoc.write(dumps(medal_unlock_dict))
    else:
        raise ValueError("Medal already unlocked!")

def load_medals(cwd):
    global medal_unlock_dict
    try:
        with open(cwd + "/saves/medals.txt", "r") as medaldoc:
            medal_unlock_dict = loads(medaldoc.readline())
    except:
        with open(cwd + "/saves/medals.txt", "w") as medaldoc:
            medaldoc.write(dumps(medal_unlock_dict))

def update_css_medals(cwd):
    global medal_unlock_dict
    global css_selector_list_medals
    global css_display_list_medals

    with open(cwd+'/saves/game_stats.txt', 'r') as statsdoc:
            game_stats = loads(statsdoc.readline())

    unlock_slot = 0
    for y in range(0, 5):
        for x in range(1, 8):
            location = (x, y)
            if location in css_location_dict_medals and css_location_dict_medals[location] == "questionmedal":
                css_display_list_medals[y][x] = ["/medals/questionMedal.png", "???", "Coming soon!"]
            elif location in css_location_dict_medals and medal_unlock_dict[css_location_dict_medals[location]]:
                medal_id = css_location_dict_medals[location]
                css_selector_list_medals[y][x] = medal_id
                css_display_list_medals[y][x] = original_css_display_list_medals[y][x]
            else:
                css_display_list_medals[y][x] = ["/medals/questionMedal.png", "Unlock Me!", str(game_stats['matches_played']) + "/" + str(unlock_milestones[unlock_slot]) + " Matches Complete"]
            unlock_slot += 1

def return_medal_unlocks():
    global medal_unlock_dict
    return medal_unlock_dict

def return_css_selector_medals():
    global css_selector_list_medals
    return css_selector_list_medals

def return_css_display_medals():
    global css_display_list_medals
    return css_display_list_medals


'''COSTUMES'''
costume_unlock_dict = {
    "quirkless": {"grayscale_1": False},
    "fire": {"grayscale_1": False},
    "ice": {"grayscale_1": False},
    "water": {"grayscale_1": False},
    "rock": {"grayscale_1": False},
    "lightning": {"grayscale_1": False},
    "wind": {"grayscale_1": False},
    "judge": {"grayscale_1": False},
    "doctor": {"grayscale_1": False},
    "king": {"grayscale_1": False},
    "cop": {"grayscale_1": False},
    "boxer": {"grayscale_1": False},
    "mirror": {"grayscale_1": False},
    "fisher": {"grayscale_1": False},
    "glue": {"grayscale_1": False},
}

def load_costume_unlocks(cwd):
    global costume_unlock_dict
    try:
        with open(cwd + "/saves/costume_unlocks.txt", "r") as blobunlockdoc:
            new_unlock_dict = loads(blobunlockdoc.readline())
            for blob in blob_unlock_dict:
                if blob not in new_unlock_dict:
                    new_unlock_dict[blob] = costume_unlock_dict[blob]
                    continue
                for costume in costume_unlock_dict:
                    if(costume not in new_unlock_dict[blob]):
                        new_unlock_dict[blob][costume] = False
                        continue
                
        
        costume_unlock_dict = new_unlock_dict

        with open(cwd + "/saves/costume_unlocks.txt", "w") as blobunlockdoc:
            blobunlockdoc.write(dumps(costume_unlock_dict))
        
    except:
        with open(cwd + "/saves/costume_unlocks.txt", "w") as blobunlockdoc:
            blobunlockdoc.write(dumps(costume_unlock_dict))

def return_costume_unlocks():
    global costume_unlock_dict
    return costume_unlock_dict

available_costumes = dict(return_blob_unlocks())

def update_costumes():
    global available_costumes
    for i in available_costumes:
        available_costumes[i] = [0]
        for j in costume_unlock_dict[i]:
            if(costume_unlock_dict[i][j]):
                available_costumes[i].append(int(j.split("_")[-1]))

def return_available_costumes():
    global available_costumes
    return available_costumes

def unlock_costume(blob, costume, cwd):
    global costume_unlock_dict
    if blob in costume_unlock_dict:
        if(costume in costume_unlock_dict[blob] and not costume_unlock_dict[blob][costume]):
            with open(cwd + "/saves/costume_unlocks.txt", "r") as blobunlockdoc:
                costume_unlock_dict = loads(blobunlockdoc.readline())
            costume_unlock_dict[blob][costume] = True
            with open(cwd + "/saves/costume_unlocks.txt", "w") as blobunlockdoc:
                blobunlockdoc.write(dumps(costume_unlock_dict))
            #print(f"Unlocked {blob} {costume}!")
        else:
            raise ValueError("Already Unlocked")
    else:
        print("Invalid Blob!")
        raise ValueError("Invalid Blob!")

if __name__ == "__main__":
    from os import getcwd
    cwd = getcwd()
    load_blob_unlocks(cwd)
    #unlock_blob("ice", cwd)
    #update_css_blobs()
	#unlock_medal("goal", cwd)
    #update_css_medals()
    
    load_medals(cwd)
    print(medal_unlock_dict)
    unlock_medal("goal", cwd)
    print(medal_unlock_dict)
    print(css_selector_list_blobs)
    print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    print(css_display_list_blobs)
    print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    print(css_selector_list_blobs)
    print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    print(css_display_list_medals)
    print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    
    unlock_costume("quirkless", "grayscale_1", cwd)
    print(costume_unlock_dict)