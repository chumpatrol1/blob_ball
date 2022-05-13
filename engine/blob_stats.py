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

def species_to_stars(species, stat_overrides):
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
    full_dict = {
        'quirkless': create_dict(3, 4, 4, 4, 4, 5, 5, 840, 5, 5, 'boost', 840, 0, 1800, 510, 0, 0),
        'fire': create_dict(2, 4, 4, 3, 1, 3, 4, 600, 3, 3, 'fireball', 150, 12, 1800, 2, 0, 0),
        'ice': create_dict(4, 4, 1, 3, 4, 3, 5, 600, 3, 3, 'snowball', 150, 12, 1800, 2, 0, 0),
        'water': create_dict(2, 3, 4, 2, 3, 3, 3, 600, 3, 3, 'geyser', 210, 15, 1800, 2, 0, 0),
        'rock': create_dict(5, 1, 5, 1, 5, 1, 2, 600, 3, 5, 'spire', 360, 0, 1800, 300, 30, 0),
        'lightning': create_dict(1, 5, 3, 5, 5, 2, 1, 600, 3, 3, 'thunderbolt', 600, 0, 1800, 360, 10, 120),
        'wind': create_dict(1, 5, 2, 5, 1, 5, 1, 600, 3, 3, 'gale', 120, 12, 1800, 2, 0, 0),
        'judge': create_dict(3, 3, 2, 3, 3, 3, 3, 600, 3, 3, 'c&d', 510, 0, 1800, 300, 0, 60),
        'doctor': create_dict(4, 2, 3, 3, 4, 1, 1, 600, 1, 1, 'pill', 300, 0, 1800, 240, 0, 0),
        'king': create_dict(3, 1, 1, 1, 1, 4, 4, 600, 5, 5, 'tax', 600, 0, 1800, 540, 0, 180),
        'cop': create_dict(3, 4, 4, 2, 3, 3, 1, 600, 2, 3, 'stoplight', 750, 0, 1800, 900, 0, 0),
        'boxer': create_dict(3, 2, 5, 2, 2, 1, 3, 600, 4, 2, 'starpunch', 750, 0, 1800, 810, 25, 0),
        'mirror': create_dict(1, 1, 5, 3, 2, 2, 2, 600, 2, 4, 'mirror', 450, 0, 1800, 30, 0, 60),
        'fisher': create_dict(1, 3, 4, 1, 3, 2, 1, 600, 3, 4, 'hook', 15, 12, 1800, 2, 40, 0),
        'glue': create_dict(2, 1, 5, 4, 2, 2, 2, 600, 3, 3, 'gluegun', 150, 15, 1800, 2, 40, 0),
    }

    blob_dict = full_dict[species]
    for key in stat_overrides:
        if stat_overrides[key] is not None:
            if(key == "max_hp"):
                if(stat_overrides[key] == 1):
                    blob_dict[key] = -2.5
                else:
                    blob_dict[key] = (stat_overrides[key] - 6)//2
            else:
                blob_dict[key] = stat_overrides[key]

    return blob_dict
