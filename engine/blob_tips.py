import pygame as pg
from os import getcwd
cwd = getcwd()
tip_font = pg.font.Font(cwd + "/resources/fonts/neuropol-x-free.regular.ttf", 30) # Load in the font
text_color = (0, 0, 255) # Set the text color to blue

quirkless_tips = [
    tip_font.render("#1: Quirkless Blob has the highest average stats", False, text_color),
    tip_font.render("in the game, encouraging good fundamentals", False, text_color),
    tip_font.render("", False, text_color),
    tip_font.render("#2: Quirkless Blob's boost is slightly more ", False, text_color),
    tip_font.render("expensive than other blobs", False, text_color),
]

fire_tips = [
    tip_font.render("#1: Fireball's speed boost is", False, text_color),
    tip_font.render("multiplicative, not additive", False, text_color),
    tip_font.render("", False, text_color),
    tip_font.render("#2: Holding down Fireball rather than tapping", False, text_color),
    tip_font.render("it will save on energy", False, text_color),
]

ice_tips = [
    tip_font.render("#1: Snowball's ball slowdown is divisive, not ", False, text_color),
    tip_font.render("subtractive", False, text_color),
    tip_font.render("", False, text_color),
    tip_font.render("#2: Snowball doesn't stop the ball instantly, but it", False, text_color),
    tip_font.render("will change the ball's trajectory significantly", False, text_color),
    tip_font.render("", False, text_color),
    tip_font.render("#3: Ice Blob is slippery on the ground, but has", False, text_color),
    tip_font.render("average air friction for better acceleration", False, text_color),
    tip_font.render("", False, text_color),
    tip_font.render("#4: Slowing down the ball slightly can cause", False, text_color),
    tip_font.render("opponents to mistime their abilities and jumps", False, text_color),
]

water_tips = [
    tip_font.render("#1: Geyser's effect gets weaker the further", False, text_color),
    tip_font.render("up the ball is", False, text_color),
    tip_font.render("", False, text_color),
    tip_font.render("#2: If the ball is rolling towards the enemy ", False, text_color),
    tip_font.render("goal, you can tap the ability button to", False, text_color),
    tip_font.render("launch the ball a little bit", False, text_color),
    tip_font.render("", False, text_color),
    tip_font.render("#3: Blocking the ball prevents Geyser's", False, text_color),
    tip_font.render("effect from working", False, text_color),
]

rock_tips = [
    tip_font.render("#1: Spire can launch opponents into the air", False, text_color),
    tip_font.render("", False, text_color),
    tip_font.render("#2: Spire will increase block cooldown by half", False, text_color),
    tip_font.render("a second when blocked - watch out!", False, text_color),
    tip_font.render("", False, text_color),
    tip_font.render("#3: Spire will always target the ball when used", False, text_color),
]

lightning_tips = [
    tip_font.render("#1: Thunderbolt will grant Lightning Blob a few", False, text_color),
    tip_font.render("seconds of boost if you hit yourself with it", False, text_color),
    tip_font.render("", False, text_color),
    tip_font.render("#2: Thunderbolt will cause the ball to cling to", False, text_color),
    tip_font.render("the ground after the ball is hit, allowing you", False, text_color),
    tip_font.render("to combo with it!", False, text_color),
    tip_font.render("", False, text_color),
    tip_font.render("#3: Thunderbolt's hitbox against foes is", False, text_color),
    tip_font.render("smaller than the one that activates your boost", False, text_color),
]

wind_tips = [

]

judge_tips = [
    tip_font.render("#1: Cease and Desist does not stop delayed", False, text_color),
    tip_font.render("abilities after they have been started", False, text_color),
    tip_font.render("", False, text_color),
    tip_font.render("#2: C&D can be used as a pseudoblock,", False, text_color),
    tip_font.render("preventing you from taking damage", False, text_color),
    tip_font.render("for a bit", False, text_color),
    tip_font.render("", False, text_color),
    tip_font.render("#3: C&D does not increase cooldowns,", False, text_color),
    tip_font.render("but simply blocks use of any powers", False, text_color),
]

doctor_tips = [
    tip_font.render("#1: Doctor Blob is more likely to pull", False, text_color),
    tip_font.render("Gelatin Pills at low HP", False, text_color),
    tip_font.render("", False, text_color),
    tip_font.render("#2: Doctor Blob's next chosen pill is random,", False, text_color),
    tip_font.render("but pills that have been eaten recently", False, text_color),
    tip_font.render("are less likely to show up", False, text_color),
    tip_font.render("", False, text_color),
    tip_font.render("#3: The Steroid Pill is longer lasting than", False, text_color),
    tip_font.render("his standard Boost", False, text_color),
    tip_font.render("", False, text_color),
    tip_font.render("#4: Caffeine Pills reduce multiple cooldowns", False, text_color),
    tip_font.render("at once, making them effective for cycling", False, text_color),
]

king_tips = [

]

cop_tips = [
    tip_font.render("#1: Stoplight's ball intangibility allows", False, text_color),
    tip_font.render("you to run the ball through an opponent", False, text_color),
    tip_font.render("", False, text_color),
    tip_font.render("#2: Stoplight can be countered if the enemy", False, text_color),
    tip_font.render("uses their block on the ball", False, text_color),
    tip_font.render("", False, text_color),
    tip_font.render("#3: Stoplight will increase your block ", False, text_color),
    tip_font.render("cooldown significantly upon use", False, text_color),
]

boxer_tips = [
    tip_font.render("#1: Blocking Starpunch will reduce", False, text_color),
    tip_font.render("damage taken by two and prevents the stun", False, text_color),
    tip_font.render("", False, text_color),
    tip_font.render("#2: Starpunch's damage is increased by", False, text_color),
    tip_font.render(" boosting or by hitting the enemy in their", False, text_color),
    tip_font.render("Danger Zone", False, text_color),
    tip_font.render("", False, text_color),
    tip_font.render("#3: Boxer Blob is heavily reliant on KOs and", False, text_color),
    tip_font.render(" has a hard time scoring goals", False, text_color),
    tip_font.render("", False, text_color),
    tip_font.render("#4: Starpunch cannot be clanked with a kick", False, text_color),
    tip_font.render("", False, text_color),
    tip_font.render("#5: Starpunch increases your kick cooldown", False, text_color),
    tip_font.render("upon activation", False, text_color),
]

mirror_tips = [
    
]
def return_selected_blob_tips(selected_blob):
    tips_dict = {
        'quirkless': quirkless_tips,
        'fire': fire_tips,
        'ice': ice_tips,
        'water': water_tips,
        'rock': rock_tips,
        'lightning': lightning_tips,
        'wind': wind_tips,
        'judge': judge_tips,
        'doctor': doctor_tips,
        'king': king_tips,
        'cop': cop_tips,
        'boxer': boxer_tips,
        'mirror': mirror_tips,
    }
    return tips_dict[selected_blob]