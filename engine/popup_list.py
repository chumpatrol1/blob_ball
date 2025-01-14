blob_unlock_splashes = { # Key is Blob name, first value is image, second is blob name, third is blob blurb
    'quirkless': ["quirkless_blob.png", "Quirkless Blob", "Has no ability, but good stats./Pressing your Ability Button/activates your boost instead!", "quirkless"],
    'fire': ["fire_blob.png", "Fire Blob", "Press and hold your ability/button to speed the ball up!", "fire"],
    'ice': ["ice_blob.png", "Ice Blob", "Press and hold your ability/button to slow the ball down!", "ice"],
    'water': ['water_blob.png', "Water Blob", "Press and hold your ability/button to push the ball up!", "water"],
    'rock': ['rock_blob.png', "Rock Blob", "Press your ability button/to summon a spire!/It shoots the ball up/and also damages nearby foes!", "rock"],
    'lightning': ['lightning_blob.png', "Lightning Blob", "Press your ability button/to summon a lightning bolt!/It spikes the ball down/and also damages nearby foes!", "lightning"],
    'wind': ['wind_blob.png', "Wind Blob", "Press your ability button to/blow wind across the field./The wind pushes airborne foes and the ball!/Wind Blob also kicks quickly!", "wind"],
    'judge': ['judge_blob.png', "Judge Blob", "Cease and desist your foes,/preventing them from using their/kicks, blocks boosts or abilities!", "judge"],
    'doctor': ['doctor_blob.png', "Doctor Blob", "This blob eats a variety of pills!/The blue caffeine pill reduces all cooldowns./The yellow steroid pill boosts yourself./The green gelatin pill heals yourself.", "doctor"],
    'king': ['king_blob.png', "King Blob", "Tax your foes, reducing/your own cooldowns and/swapping your speed stats!", "king"],
    'cop': ['cop_blob.png', "Cop Blob", "Blow your whistle at the/ball to stop it completely,/and make it intangible to the enemy!", "cop"],
    'boxer': ['boxer_blob.png', "Boxer Blob", "Unleash a mighty punch/at your enemy to do/heavy damage and stun them!/Blocking won't help much.", "boxer"],
    'mirror': ['mirror_blob.png', "Mirror Blob", "Shatters as easily as it/is to find a used mirror./Reverses the ball's direction.", "mirror"],
    'fisher': ['fisher_blob.png', "Fisher Blob", "Press and hold your ability button/to reel in your catch!/It seems to always be a soccer ball.", "fisher"],
    'glue': ['glue_blob.png', "Glue Blob", "Press and hold your ability button/to shoot out glue pellets!/When they land, the puddles trap/both your enemy and the ball!", "glue"],
    'arcade': ['arcade_blob.png', "Arcade Blob", "Press your ability button to/throw out a cheat cartridge!/Press and hold down to teleport to it.", "arcade"],
    'joker': ['joker_blob.png', "Joker Blob", "Press your ability button to/look at your deck of cards!/Press a direction and press an action button/to swap out an action with an Ability Card!", "joker"],
    'taco': ['taco_blob.png', "Taco Blob", "Press your ability button to/look at your menu!/Press a direction and press an action button/to change your stats mid-battle!", "taco"],
    'cactus': ['cactus_blob.png', "Cactus Blob", "Press your ability button to/shoot out a spiky ball!/It targets the ball, draining energy/ from enemies as it travels!", "cactus"],
    'merchant': ['merchant_blob.png', "Merchant Blob", "Open up shop with your ability button!/Simply pick a direction in order/to buy some fragile accessories!", "merchant"],
    'bubble': ['bubble_blob.png', "Bubble Blob", "Press your ability button to/blow a bubble! The bubble picks/up the ball and launches it!", "bubble"],
    'monk': ['monk_white.png', "Monk Blob", "Starts with abysmal stats./Your ability button upgrades/your stats and shoots a shuriken!", "monk"]
}

def find_blob_unlock(key):
    try:
        return blob_unlock_splashes[key]
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

costume_unlock_splashes = { # Key is 
    'quirkless/grayscale_1': ["quirkless_blob_1.png", "Grayscale Quirkless", "Press block after selecting/this blob to toggle costumes!", "Play 10 Matches", "quirkless"],
    'fire/grayscale_1': ["fire_blob_1.png", "Grayscale Fire", "Press block after selecting/this blob to toggle costumes!", "Play 10 Matches", "fire"],
    'ice/grayscale_1': ["ice_blob_1.png", "Grayscale Ice", "Press block after selecting/this blob to toggle costumes!", "Play 10 Matches", "ice"],
    'water/grayscale_1': ["water_blob_1.png", "Grayscale Water", "Press block after selecting/this blob to toggle costumes!", "Play 10 Matches", "water"],
    'rock/grayscale_1': ["rock_blob_1.png", "Grayscale Rock", "Press block after selecting/this blob to toggle costumes!", "Play 10 Matches", "rock"],
    'lightning/grayscale_1': ["lightning_blob_1.png", "Grayscale Lightning", "Press block after selecting/this blob to toggle costumes!", "Play 10 Matches", "lightning"],
    'wind/grayscale_1': ["wind_blob_1.png", "Grayscale Wind", "Press block after selecting/this blob to toggle costumes!", "Play 10 Matches", "wind"],
    'judge/grayscale_1': ["judge_blob_1.png", "Grayscale Judge", "Press block after selecting/this blob to toggle costumes!", "Play 10 Matches", "judge"],
    'doctor/grayscale_1': ["doctor_blob_1.png", "Grayscale Doctor", "Press block after selecting/this blob to toggle costumes!", "Play 10 Matches", "doctor"],
    'king/grayscale_1': ["king_blob_1.png", "Grayscale King", "Press block after selecting/this blob to toggle costumes!", "Play 10 Matches", "king"],
    'cop/grayscale_1': ["cop_blob_1.png", "Grayscale Cop", "Press block after selecting/this blob to toggle costumes!", "Play 10 Matches", "cop"],
    'boxer/grayscale_1': ["boxer_blob_1.png", "Grayscale Boxer", "Press block after selecting/this blob to toggle costumes!", "Play 10 Matches", "boxer"],
    'mirror/grayscale_1': ["mirror_blob_1.png", "Grayscale Mirror", "Press block after selecting/this blob to toggle costumes!", "Play 10 Matches", "mirror"],
    'mirror/dark_2': ["mirror_blob_2.png", "Dark Reflection", "Press block after selecting/this blob to toggle costumes!", "Play 20 Matches", "mirror"],
    'fisher/grayscale_1': ["fisher_blob_1.png", "Grayscale Fisher", "Press block after selecting/this blob to toggle costumes!", "Play 10 Matches", "fisher"],
    'fisher/jew_2': ["fisher_blob_2.png", "Jew Fisher", "Press block after selecting/this blob to toggle costumes!", "Play 20 Matches", "fisher"],
    'glue/grayscale_1': ["glue_blob_1.png", "Grayscale Glue", "Press block after selecting/this blob to toggle costumes!", "Play 10 Matches", "glue"],
    'arcade/grayscale_1': ["arcade_blob_1.png", "Grayscale Arcade", "Press block after selecting/this blob to toggle costumes!", "Play 10 Matches", "arcade"],
    'joker/grayscale_1': ["joker_blob_1.png", "Grayscale Joker", "Press block after selecting/this blob to toggle costumes!", "Play 10 Matches", "joker"],
    'joker/red_2': ["joker_blob_2.png", "Red Joker", "Press block after selecting/this blob to toggle costumes!", "Play 20 Matches", "joker"],
    'joker/mosaic_3': ["joker_blob_3.png", "Mosaic Joker", "Press block after selecting/this blob to toggle costumes!", "Play 30 Matches", "joker"],
    'taco/grayscale_1': ["taco_blob_1.png", "Grayscale Taco", "Press block after selecting/this blob to toggle costumes!", "Play 10 Matches", "taco"],
    'cactus/grayscale_1': ["cactus_blob_1.png", "Grayscale Cactus", "Press block after selecting/this blob to toggle costumes!", "Play 10 Matches", "cactus"],
    'merchant/grayscale_1': ["merchant_blob_1.png", "Grayscale Merchant", "Press block after selecting/this blob to toggle costumes!", "Play 10 Matches", "merchant"],
    'bubble/grayscale_1': ["merchant_blob_1.png", "Grayscale Bubble", "Press block after selecting/this blob to toggle costumes!", "Play 10 Matches", "bubble"],
    'monk/grayscale_1': ["monk_white_1.png", "Grayscale Monk", "Press block after selecting/this blob to toggle costumes!", "Play 10 Matches", "monk"],
}

def find_costume_unlock(key):
    try:
        return costume_unlock_splashes[key]
    except:
        print("Cannot find costume")