blob_unlock_popups = { # Key is Blob name, first value is image, second is blob name, third is blob blurb
    'fire': ["fire_blob.png", "Fire Blob", "Press and hold your ability/button to speed the ball up!"],
    'ice': ["ice_blob.png", "Ice Blob", "Press and hold your ability/button to slow the ball down!"],
    'water': ['water_blob.png', "Water Blob", "Press and hold your ability/button to push the ball up!"],
    'rock': ['rock_blob.png', "Rock Blob", "Press your ability button/to summon a spire!/It shoots the ball up/and also damages nearby foes!"],
    'lightning': ['lightning_blob.png', "Lightning Blob", "Press your ability button/to summon a lightning bolt!/It spikes the ball down/and also damages nearby foes!"],
    'wind': ['wind_blob.png', "Wind Blob", "Press your ability button to/blow wind across the field./The wind pushes airborne foes and the ball!/Wind Blob also kicks quickly!"],
    'judge': ['judge_blob.png', "Judge Blob", "Cease and desist your foes,/preventing them from using their/kicks, blocks boosts or abilities!"],
    'doctor': ['doctor_blob.png', "Doctor Blob", "This blob eats a variety of pills!/The blue caffeine pill reduces all cooldowns./The yellow steroid pill boosts yourself./The green gelatin pill heals yourself."],
    'king': ['king_blob.png', "King Blob", "Tax your foes, reducing/your own cooldowns and/swapping your speed stats!"],
    'cop': ['cop_blob.png', "Cop Blob", "Blow your whistle at the/ball to stop it completely,/and make it intangible to the enemy!"],
    'boxer': ['boxer_blob.png', "Boxer Blob", "Unleash a mighty punch/at your enemy to do/heavy damage and stun them!/Blocking won't help much."],
}

def find_blob_unlock(key):
    try:
        return blob_unlock_popups[key]
    except:
        print("Cannot find blob")

medal_unlock_popups = { # Key is Medal name, first value is image, second is medal name, third is the description
    'goal': ["goal_medal.jpg", "Goal!", "You got a point from a goal, good shots!"],
    'ko': ["ko_medal.jpg", "KO!", "You got a point from a KO, nice slap!"],
    'parry_this': ["parrythis.jpg", "Parry This!", "Use your block to nullify an incoming attack!"],
}

def find_medal_unlock(key):
    try:
        return medal_unlock_popups[key]
    except:
        print("Cannot find medal")