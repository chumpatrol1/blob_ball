from json import loads

def create_dict(max_hp = 3, top_speed = 3, traction = 3, friction = 3, gravity = 3, kick_cooldown = 3, \
    block_cooldown = 3, boost_cost = 600, boost_cooldown_max = 3, boost_duration = 3, special_ability = 'boost', \
        special_ability_cost = 840, special_ability_maintenance = 0, special_ability_max = 1800,\
        special_ability_cooldown = 510, special_ability_delay = 0, special_ability_duration = 0,):
    blob_dict = {
            'max_hp': max_hp,
            'top_speed': top_speed,
            'traction': traction,
            'friction': friction,
            'gravity': gravity,
            'kick_cooldown_rate': kick_cooldown,
            'block_cooldown_rate': block_cooldown,
            'boost_cost': boost_cost,
            'boost_cooldown_max': boost_cooldown_max,
            'boost_duration': boost_duration,

            'special_ability': special_ability,
            'special_ability_cost': special_ability_cost,
            'special_ability_maintenance': special_ability_maintenance,
            'special_ability_max': special_ability_max,
            'special_ability_cooldown': special_ability_cooldown,
            'special_ability_delay': special_ability_delay,
            'special_ability_duration': special_ability_duration,
        }
    return blob_dict

def species_to_stars(species):
    '''
    max_hp: The most HP a blob has (the amount they start each round with)
    top_speed: The fastest that a blob can naturally accelerate to in the ground/air
    traction: The rate at which a blob accelerates on the ground, or the amount that they decelerate when no key is held
    friction: The rate at which a blob accelerates in the air, or the amount that they decelerate when no key is held
    jump_force: Affects the jump height of a blob (Gravity should not affect this)
    gravity: Affects how long it takes for a blob to get back to the ground after jumping. 
    kick_cooldown_rate: Affects how long it takes for a kick to cool down
    block_cooldown_rate: Affects how long it takes for a block to cool down

    boost_cost: Affects the cost of using a boost
    boost_cooldown_rate: Affects how long it takes for a boost to cool down
    boost_duration: The amount of time that a stat boost lasts

    special_ability: The type of SA a blob has
    special_ability_cost: The amount that using a special ability costs
    speical_ability_max: The most special ability that can be stored at once
    special_ability_cooldown: The time between special ability uses. 0 means that it can be held down.
    '''
    with open(f"blobs\\{species}\\init.blob", "r") as f:
        init_file = f.read()
    blob_dict = loads(init_file)["stars"]
    return blob_dict

from os import getcwd
cwd = getcwd()
icon_cwd = cwd + "/resources/images/ui_icons/"
ability_cwd = cwd + "/resources/images/ability_icons/"

ability_image_dict = {
        "quirkless": icon_cwd + "boost_icon.png",
        "fire": ability_cwd + "fireball.png",
        "ice": ability_cwd + "snowball.png",
        'water': ability_cwd + "geyser.png",
        'rock': ability_cwd + "spire.png",
        'lightning': ability_cwd + "thunderbolt.png",
        'wind': ability_cwd + "gale.png",
        'judge': ability_cwd + "cnd.png",
        'doctor': ability_cwd + "pill.png",
        'king': ability_cwd + "tax.png",
        'cop': ability_cwd + "block_icon.png",
        'boxer': ability_cwd + 'starpunch.png',
        'mirror': ability_cwd + 'mirror.png',
        'fisher': ability_cwd + 'hook.png',
        'glue': ability_cwd + 'glue.png',
        'joker': ability_cwd + 'card.png',
        'arcade': ability_cwd + 'teleport.png',
        'taco': ability_cwd + 'filling.png',
        'cactus': ability_cwd + 'cactus_spike.png',
        'merchant': ability_cwd + 'coin.png',
        'bubble': ability_cwd + 'bubble.png',
        "random": icon_cwd + "boost_icon.png",
    }

def species_to_ability_icon(species):
    return ability_image_dict[species]