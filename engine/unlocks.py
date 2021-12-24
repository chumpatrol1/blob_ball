from json import loads, dumps
from copy import deepcopy
# The original selector
css_selector_list = [
    ["back", "quirkless", "quirkless", "quirkless", "quirkless", "quirkless", "quirkless", "quirkless",],
    ["rules", "quirkless", "quirkless", "quirkless", "quirkless", "quirkless", "quirkless", "quirkless",],
    ["settings", "quirkless", "quirkless", "quirkless", "quirkless", "quirkless", "quirkless", "quirkless",],
    ["almanac", "quirkless", "quirkless", "quirkless", "quirkless", "quirkless", "quirkless", "quirkless",],
    ["back", "quirkless", "quirkless", "quirkless", "quirkless", "quirkless", "quirkless", "quirkless",],
]

original_css_display_list = [ #Creates an array of arrays, which contains the image to use, it's name, and special ability
[["/css_icons/back_arrow.png", "Back", ""], ["/blobs/quirkless_blob.png", "Quirkless Blob", "No Ability"], ["/blobs/fire_blob.png", "Fire Blob", "Fireball"], ["/blobs/ice_blob.png", "Ice Blob", "Snowball"], ["/blobs/water_blob.png", "Water Blob", "Geyser"], ["/blobs/rock_blob.png", "Rock Blob", "Spire"], ["/blobs/lightning_blob.png", "Lightning Blob", "Thunderbolt"], ["/blobs/wind_blob.png", "Wind Blob", "Gale"],],
[["/css_icons/rules_icon.png", "Rules", ""], ["/blobs/judge_blob.png", "Judge Blob", "C&D"], ["/blobs/doctor_blob.png", "Doctor Blob", "Pill"], ["/blobs/king_blob.png", "King Blob", "Tax"], ["/blobs/cop_blob.png", "Cop Blob", "Stoplight"], ["/blobs/quirkless_blob.png", "", ""], ["/blobs/quirkless_blob.png", "", ""], ["/blobs/quirkless_blob.png", "", ""],],
[["/css_icons/gear_icon.png", "Settings", ""], ["/blobs/quirkless_blob.png", "", ""], ["/blobs/quirkless_blob.png", "", ""], ["/blobs/quirkless_blob.png", "", ""], ["/blobs/quirkless_blob.png", "", ""], ["/blobs/quirkless_blob.png", "", ""], ["/blobs/quirkless_blob.png", "", ""], ["/blobs/quirkless_blob.png", "", ""],],
[["/css_icons/almanac_icon.png", "Almanac", ""], ["/blobs/quirkless_blob.png", "", ""], ["/blobs/quirkless_blob.png", "", ""], ["/blobs/quirkless_blob.png", "", ""], ["/blobs/quirkless_blob.png", "", ""], ["/blobs/quirkless_blob.png", "", ""], ["/blobs/quirkless_blob.png", "", ""], ["/blobs/quirkless_blob.png", "", ""],],
[["/css_icons/cpu_icon.png", "Toggle CPU", ""], ["/blobs/quirkless_blob.png", "", ""], ["/blobs/quirkless_blob.png", "", ""], ["/blobs/quirkless_blob.png", "", ""], ["/blobs/quirkless_blob.png", "", ""], ["/blobs/quirkless_blob.png", "", ""], ["/blobs/quirkless_blob.png", "", ""], ["/blobs/quirkless_blob.png", "", ""],],
]

css_display_list = deepcopy(original_css_display_list) #Creates an array of arrays, which contains the image to use, it's name, and special ability


css_location_dict = { # Stores every location to loop through. The key is a location, the value is cross checked with blob_unlock_dict
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
    (5, 1): "quirkless",
    (6, 1): "quirkless",
    (7, 1): "quirkless",
    (1, 2): "quirkless",
    (2, 2): "quirkless",
    (3, 2): "quirkless",
    (4, 2): "quirkless",
    (5, 2): "quirkless",
    (6, 2): "quirkless",
    (7, 2): "quirkless",
    (1, 3): "quirkless",
    (2, 3): "quirkless",
    (3, 3): "quirkless",
    (4, 3): "quirkless",
    (5, 3): "quirkless",
    (6, 3): "quirkless",
    (7, 3): "quirkless",
    (1, 4): "quirkless",
    (2, 4): "quirkless",
    (3, 4): "quirkless",
    (4, 4): "quirkless",
    (5, 4): "quirkless",
    (6, 4): "quirkless",
    (7, 4): "quirkless",
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

def update_css_blobs():
    global blob_unlock_dict
    global css_selector_list
    global css_display_list

    for y in range(0, 5):
        for x in range(1, 8):
            location = (x, y)
            if location in css_location_dict and blob_unlock_dict[css_location_dict[location]]:
                blob_id = css_location_dict[location]
                css_selector_list[y][x] = blob_id
                css_display_list[y][x] = original_css_display_list[y][x]
            else:
                css_display_list[y][x] = ["/blobs/quirkless_blob.png", "Quirkless Blob", "No Ability"]

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

def return_css_selector():
    global css_selector_list
    return css_selector_list

def return_css_display():
    global css_display_list
    return css_display_list


'''MEDALS'''
original_medal_list = [ # Format: [Image, Name, Description]
    [["/medals/", "Goal!", "Score a point by kicking the ball into the goal!"], ["/medals/", "KO!", "Score a point by kicking a player into unconsciousness!"], ["/medals/", "Parry This!", "Use your block to nullify an incoming attack!"], ["/medals/", "Ball Stopper", "Use your block to completely stop the ball"], ["/medals/", "Clash of the Blobs", "Cancel out the kick of an opponent with a kick of your own"], ["/medals/", "Power Up!", "Increase your speed and damage with a boost"], ["/medals/", "Damage Stacking", "Deal 4 damage with a single kick!"], ["/medals/", "Goal!", "Score a point by kicking the ball into the goal!"], ["/medals/", "Goal!", "Score a point by kicking the ball into the goal!"], ],
    [["/medals/", "Goal!", "Score a point by kicking the ball into the goal!"], ["/medals/", "Goal!", "Score a point by kicking the ball into the goal!"], ["/medals/", "Goal!", "Score a point by kicking the ball into the goal!"], ["/medals/", "Goal!", "Score a point by kicking the ball into the goal!"], ["/medals/", "Goal!", "Score a point by kicking the ball into the goal!"], ["/medals/", "Goal!", "Score a point by kicking the ball into the goal!"], ["/medals/", "Goal!", "Score a point by kicking the ball into the goal!"], ["/medals/", "Goal!", "Score a point by kicking the ball into the goal!"], ["/medals/", "Goal!", "Score a point by kicking the ball into the goal!"], ],
    [["/medals/", "Goal!", "Score a point by kicking the ball into the goal!"], ["/medals/", "Goal!", "Score a point by kicking the ball into the goal!"], ["/medals/", "Goal!", "Score a point by kicking the ball into the goal!"], ["/medals/", "Goal!", "Score a point by kicking the ball into the goal!"], ["/medals/", "Goal!", "Score a point by kicking the ball into the goal!"], ["/medals/", "Goal!", "Score a point by kicking the ball into the goal!"], ["/medals/", "Goal!", "Score a point by kicking the ball into the goal!"], ["/medals/", "Goal!", "Score a point by kicking the ball into the goal!"], ["/medals/", "Goal!", "Score a point by kicking the ball into the goal!"], ],
    [["/medals/", "Goal!", "Score a point by kicking the ball into the goal!"], ["/medals/", "Goal!", "Score a point by kicking the ball into the goal!"], ["/medals/", "Goal!", "Score a point by kicking the ball into the goal!"], ["/medals/", "Goal!", "Score a point by kicking the ball into the goal!"], ["/medals/", "Goal!", "Score a point by kicking the ball into the goal!"], ["/medals/", "Goal!", "Score a point by kicking the ball into the goal!"], ["/medals/", "Goal!", "Score a point by kicking the ball into the goal!"], ["/medals/", "Goal!", "Score a point by kicking the ball into the goal!"], ["/medals/", "Goal!", "Score a point by kicking the ball into the goal!"], ],
    [["/medals/", "Goal!", "Score a point by kicking the ball into the goal!"], ["/medals/", "Goal!", "Score a point by kicking the ball into the goal!"], ["/medals/", "Goal!", "Score a point by kicking the ball into the goal!"], ["/medals/", "Goal!", "Score a point by kicking the ball into the goal!"], ["/medals/", "Goal!", "Score a point by kicking the ball into the goal!"], ["/medals/", "Goal!", "Score a point by kicking the ball into the goal!"], ["/medals/", "Goal!", "Score a point by kicking the ball into the goal!"], ["/medals/", "Goal!", "Score a point by kicking the ball into the goal!"], ["/medals/", "Goal!", "Score a point by kicking the ball into the goal!"], ],
    ]

medal_list = original_medal_list.copy()

medal_location_dict = {
    (0, 0): "goal",
    (1, 0): "ko",
    (2, 0): "parry_this",
    (3, 0): "ball_stop",
    (4, 0): "clash_of_the_blobs",
    (5, 0): "power_up",
    (6, 0): "damage_stacking",
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

if __name__ == "__main__":
    from os import getcwd
    cwd = getcwd()
    load_blob_unlocks(cwd)
    #unlock_blob("ice", cwd)
    update_css_blobs()
    
    print(css_selector_list)
    print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    print(css_display_list)
    print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    load_medals(cwd)
    print(medal_unlock_dict)
    unlock_medal("goal", cwd)
    print(medal_unlock_dict)