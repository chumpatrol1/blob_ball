from json import loads, dumps
# The original selector
css_selector_list = [
    ["back", "quirkless", "quirkless", "quirkless", "quirkless", "quirkless", "quirkless", "quirkless",],
    ["rules", "quirkless", "quirkless", "quirkless", "quirkless", "quirkless", "quirkless", "quirkless",],
    ["settings", "quirkless", "quirkless", "quirkless", "quirkless", "quirkless", "quirkless", "quirkless",],
    ["almanac", "quirkless", "quirkless", "quirkless", "quirkless", "quirkless", "quirkless", "quirkless",],
    ["back", "quirkless", "quirkless", "quirkless", "quirkless", "quirkless", "quirkless", "quirkless",],
]

original_css_display_list = [ #Creates an array of arrays, which contains the image to use, it's name, and special ability
[["/back_arrow.png", "Back", ""], ["/blobs/quirkless_blob.png", "Quirkless Blob", "No Ability"], ["/blobs/fire_blob.png", "Fire Blob", "Fireball"], ["/blobs/ice_blob.png", "Ice Blob", "Snowball"], ["/blobs/water_blob.png", "Water Blob", "Geyser"], ["/blobs/rock_blob.png", "Rock Blob", "Spire"], ["/blobs/lightning_blob.png", "Lightning Blob", "Thunderbolt"], ["/blobs/wind_blob.png", "Wind Blob", "Gale"],],
[["/rules_icon.png", "Rules", ""], ["/blobs/judge_blob.png", "Judge Blob", "C&D"], ["/blobs/doctor_blob.png", "Doctor Blob", "Pill"], ["/blobs/king_blob.png", "King Blob", "Tax"], ["/blobs/quirkless_blob.png", "", ""], ["/blobs/quirkless_blob.png", "", ""], ["/blobs/quirkless_blob.png", "", ""], ["/blobs/quirkless_blob.png", "", ""],],
[["/gear_icon.png", "Settings", ""], ["/blobs/quirkless_blob.png", "", ""], ["/blobs/quirkless_blob.png", "", ""], ["/blobs/quirkless_blob.png", "", ""], ["/blobs/quirkless_blob.png", "", ""], ["/blobs/quirkless_blob.png", "", ""], ["/blobs/quirkless_blob.png", "", ""], ["/blobs/quirkless_blob.png", "", ""],],
[["/almanac_icon.png", "Almanac", ""], ["/blobs/quirkless_blob.png", "", ""], ["/blobs/quirkless_blob.png", "", ""], ["/blobs/quirkless_blob.png", "", ""], ["/blobs/quirkless_blob.png", "", ""], ["/blobs/quirkless_blob.png", "", ""], ["/blobs/quirkless_blob.png", "", ""], ["/blobs/quirkless_blob.png", "", ""],],
[["/cpu_icon.png", "Toggle CPU", ""], ["/blobs/quirkless_blob.png", "", ""], ["/blobs/quirkless_blob.png", "", ""], ["/blobs/quirkless_blob.png", "", ""], ["/blobs/quirkless_blob.png", "", ""], ["/blobs/quirkless_blob.png", "", ""], ["/blobs/quirkless_blob.png", "", ""], ["/blobs/quirkless_blob.png", "", ""],],
]

css_display_list = [ #Creates an array of arrays, which contains the image to use, it's name, and special ability
[["/back_arrow.png", "Back", ""], ["/blobs/quirkless_blob.png", "Quirkless Blob", "No Ability"], ["/blobs/fire_blob.png", "Fire Blob", "Fireball"], ["/blobs/ice_blob.png", "Ice Blob", "Snowball"], ["/blobs/water_blob.png", "Water Blob", "Geyser"], ["/blobs/rock_blob.png", "Rock Blob", "Spire"], ["/blobs/lightning_blob.png", "Lightning Blob", "Thunderbolt"], ["/blobs/wind_blob.png", "Wind Blob", "Gale"],],
[["/rules_icon.png", "Rules", ""], ["/blobs/judge_blob.png", "Judge Blob", "C&D"], ["/blobs/doctor_blob.png", "Doctor Blob", "Pill"], ["/blobs/king_blob.png", "King Blob", "Tax"], ["/blobs/quirkless_blob.png", "", ""], ["/blobs/quirkless_blob.png", "", ""], ["/blobs/quirkless_blob.png", "", ""], ["/blobs/quirkless_blob.png", "", ""],],
[["/gear_icon.png", "Settings", ""], ["/blobs/quirkless_blob.png", "", ""], ["/blobs/quirkless_blob.png", "", ""], ["/blobs/quirkless_blob.png", "", ""], ["/blobs/quirkless_blob.png", "", ""], ["/blobs/quirkless_blob.png", "", ""], ["/blobs/quirkless_blob.png", "", ""], ["/blobs/quirkless_blob.png", "", ""],],
[["/almanac_icon.png", "Almanac", ""], ["/blobs/quirkless_blob.png", "", ""], ["/blobs/quirkless_blob.png", "", ""], ["/blobs/quirkless_blob.png", "", ""], ["/blobs/quirkless_blob.png", "", ""], ["/blobs/quirkless_blob.png", "", ""], ["/blobs/quirkless_blob.png", "", ""], ["/blobs/quirkless_blob.png", "", ""],],
[["/cpu_icon.png", "Toggle CPU", ""], ["/blobs/quirkless_blob.png", "", ""], ["/blobs/quirkless_blob.png", "", ""], ["/blobs/quirkless_blob.png", "", ""], ["/blobs/quirkless_blob.png", "", ""], ["/blobs/quirkless_blob.png", "", ""], ["/blobs/quirkless_blob.png", "", ""], ["/blobs/quirkless_blob.png", "", ""],],
]

css_location_dict = {
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
    (4, 1): "quirkless",
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

blob_unlock_dict = {
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
}

def load_blob_unlocks(cwd):
    global blob_unlock_dict
    try:
        with open(cwd + "/saves/blob_unlocks.txt", "r") as blobunlockdoc:
            blob_unlock_dict = loads(blobunlockdoc.readline())
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

if __name__ == "__main__":
    from os import getcwd
    cwd = getcwd()
    load_blob_unlocks(cwd)
    unlock_blob("ice")
    update_css_blobs()
    
    print(css_selector_list)
    print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    print(css_display_list)