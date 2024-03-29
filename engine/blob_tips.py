import pygame as pg
from os import getcwd
cwd = getcwd()
tip_font = pg.font.Font(cwd + "/resources/fonts/neuropol-x-free.regular.ttf", 30) # Load in the font
text_color = (0, 0, 255) # Set the text color to blue

# Should I put these into loops? -sunken

quirkless_tips = [
    tip_font.render("#1: Quirkless Blob has the highest average stats", False, text_color),
    tip_font.render("in the game, encouraging good fundamentals", False, text_color),
    tip_font.render("", False, text_color),
    tip_font.render("#2: Quirkless Blob's boost is slightly more ", False, text_color),
    tip_font.render("expensive than other blobs", False, text_color),
    tip_font.render("", False, text_color),
    tip_font.render("#3: Quirkless Blob's fast kicks allows him to", False, text_color),
    tip_font.render("deal frequent damage. Use this to maintain", False, text_color),
    tip_font.render("pressure and score points through KOs!", False, text_color),
    tip_font.render("", False, text_color),
    tip_font.render("#4: Quirkless Blob's block recharges very", False, text_color),
    tip_font.render("quickly, allowing you to stop the ball", False, text_color),
    tip_font.render("frequently or to parry incoming attacks!", False, text_color),
    tip_font.render("", False, text_color),
    tip_font.render("#5: Combining your boost with a kick will", False, text_color),
    tip_font.render("cause your kick to do +1 damage!", False, text_color),
]

fire_tips = [
    tip_font.render("#1: Fireball's speed boost is", False, text_color),
    tip_font.render("multiplicative, not additive", False, text_color),
    tip_font.render("", False, text_color),
    tip_font.render("#2: Holding down Fireball rather than tapping", False, text_color),
    tip_font.render("it will save on energy. If you do it long enough,", False, text_color),
    tip_font.render("you'll get a speed boost, but you'll also be", False, text_color),
    tip_font.render("vulnerable to damage.", False, text_color),
    tip_font.render("", False, text_color),
    tip_font.render("#3: Need more energy? Holding ''down'' ", False, text_color),
    tip_font.render("while on the ground will cause your blob", False, text_color),
    tip_font.render("to Focus, quintupling your energy ", False, text_color),
    tip_font.render("production! It comes at the cost", False, text_color),
    tip_font.render("of mobility, however", False, text_color),
    tip_font.render("", False, text_color),
    tip_font.render("#4: Fire Blob's boost kick will apply the", False, text_color),
    tip_font.render("Overheat effect on your enemy for 5 seconds,", False, text_color),
    tip_font.render("doubling all cooldowns for that time!", False, text_color),
]

ice_tips = [
    tip_font.render("#1: Snowball doesn't stop the ball instantly,", False, text_color),
    tip_font.render("but it will change the ball's trajectory", False, text_color),
    tip_font.render("significantly and cause it to hover!", False, text_color),
    tip_font.render("", False, text_color),
    tip_font.render("#2: Ice Blob is slippery on the ground, but has", False, text_color),
    tip_font.render("average air friction for better acceleration", False, text_color),
    tip_font.render("", False, text_color),
    tip_font.render("#3: Slowing down the ball slightly can cause", False, text_color),
    tip_font.render("opponents to mistime their abilities and jumps", False, text_color),
    tip_font.render("", False, text_color),
    tip_font.render("#4: You can use your block as an emergency", False, text_color),
    tip_font.render("brake since it halts all momentum", False, text_color),
    tip_font.render("", False, text_color),
    tip_font.render("#5: Boost Kicking applies a hypothermia effect", False, text_color),
    tip_font.render("which applies a slowing effect to your enemy!", False, text_color),
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
    tip_font.render("", False, text_color),
    tip_font.render("#4: If you are focusing to charge energy,", False, text_color),
    tip_font.render("remember that you can always jump to cancel", False, text_color),
    tip_font.render("your focus early!", False, text_color),
    tip_font.render("", False, text_color),
    tip_font.render("#5: Need even more energy?! Time your block so", False, text_color),
    tip_font.render("that you parry an incoming blow as early as", False, text_color),
    tip_font.render("possible, gaining 300 energy! That's about 10", False, text_color),
    tip_font.render("seconds of gameplay, or about half a boost!", False, text_color),
]

rock_tips = [
    tip_font.render("#1: Spire can launch opponents into the air", False, text_color),
    tip_font.render("", False, text_color),
    tip_font.render("#2: Spire will increase block cooldown by half", False, text_color),
    tip_font.render("a second when blocked - watch out!", False, text_color),
    tip_font.render("", False, text_color),
    tip_font.render("#3: Spire will always target the ball when used", False, text_color),
    tip_font.render("", False, text_color),
    tip_font.render("#4: Pressing down in the air will make your", False, text_color),
    tip_font.render("descent a lot faster!", False, text_color),
    tip_font.render("", False, text_color),
    tip_font.render("#5: Need a burst of speed, but you're focusing?", False, text_color),
    tip_font.render("After your focus aura turns grey, you can", False, text_color),
    tip_font.render("hold left or right for a quick burst of speed", False, text_color),
    tip_font.render("called a wavedash!", False, text_color),
]

lightning_tips = [
    tip_font.render("#1: Thunderbolt will alaways target the ball", False, text_color),
    tip_font.render("when used. The delay is short, so watch out!", False, text_color),
    tip_font.render("", False, text_color),
    tip_font.render("#2: Thunderbolt will grant Lightning Blob a few", False, text_color),
    tip_font.render("seconds of boost if you hit yourself with it", False, text_color),
    tip_font.render("", False, text_color),
    tip_font.render("#3: Thunderbolt will cause the ball to cling", False, text_color),
    tip_font.render("to the ground after the ball is hit, allowing", False, text_color),
    tip_font.render("you to combo with it!", False, text_color),
    tip_font.render("", False, text_color),
    tip_font.render("#4: Thunderbolt's hitbox against foes is", False, text_color),
    tip_font.render("smaller than the one that activates your boost", False, text_color),
]

wind_tips = [
    tip_font.render("#1: Wind Blob can get across the field", False, text_color),
    tip_font.render("very quickly by chaining short hops!", False, text_color),
    tip_font.render("", False, text_color),
    tip_font.render("#2: Gale will always push the enemy", False, text_color),
    tip_font.render("and the ball away from your goal", False, text_color),
    tip_font.render("for a bit", False, text_color),
    tip_font.render("", False, text_color),
    tip_font.render("#3: Wind Blob can harass the opponent", False, text_color),
    tip_font.render("with frequent kicks. Run and gun!", False, text_color),
    tip_font.render("", False, text_color),
    tip_font.render("#4: The yellow area surrounding your goal", False, text_color),
    tip_font.render("is a danger zone! If you get kicked, you will", False, text_color),
    tip_font.render("take +1 damage! Use Gale to reset the", False, text_color),
    tip_font.render("situation and to preserve your pool of HP!", False, text_color),
    tip_font.render("", False, text_color),
    tip_font.render("#5: Wind Blob's boost kick knocks back", False, text_color),
    tip_font.render("opponents! Holding in reduces the effect.", False, text_color),
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
    tip_font.render("", False, text_color),
    tip_font.render("#4: Judge Blob's boost kick is a short stun.", False, text_color),
    tip_font.render("If the opponent is C&D'd, the stun lasts longer.", False, text_color),
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
    tip_font.render("his standard Boost, and also causes his", False, text_color),
    tip_font.render("kicks to partially pierce blocks!", False, text_color),
    tip_font.render("", False, text_color),
    tip_font.render("#4: Caffeine Pills reduce multiple cooldowns", False, text_color),
    tip_font.render("at once, making them effective for cycling", False, text_color),
]

king_tips = [
    tip_font.render("#1: Tax will make your enemy much slower", False, text_color),
    tip_font.render("and their movement much slipperier!", False, text_color),
    tip_font.render("", False, text_color),
    tip_font.render("#2: Your kick, block and boost cooldowns", False, text_color),
    tip_font.render("will all be reduced by a full second!", False, text_color),
    tip_font.render("", False, text_color),
    tip_font.render("#3: You can stack the speed boost with", False, text_color),
    tip_font.render("the stat swap from Tax!", False, text_color),
    tip_font.render("", False, text_color),
    tip_font.render("#4: King Blob's boost kick is known as the", False, text_color),
    tip_font.render("Royal Loan. While the opponent has Royal Loan,", False, text_color),
    tip_font.render("their cooldowns are greatly reduced. After 8", False, text_color),
    tip_font.render("actions are used, that enemy gets the overheat", False, text_color),
    tip_font.render("effect while King improves his cooldowns!", False, text_color),
    tip_font.render("", False, text_color),
    tip_font.render("#5: If an opponent has Royal Loan active,", False, text_color),
    tip_font.render("King Blob's boost kick will increase the counter instead.", False, text_color),
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
    tip_font.render("boosting or by hitting the enemy in their", False, text_color),
    tip_font.render("Danger Zone", False, text_color),
    tip_font.render("", False, text_color),
    tip_font.render("#3: Starpunch cannot be clanked with a kick", False, text_color),
    tip_font.render("", False, text_color),
    tip_font.render("#4: Starpunch increases your kick cooldown", False, text_color),
    tip_font.render("upon activation, but if you hit your attack", False, text_color),
    tip_font.render("your kick cooldown decreases. Hitting a boost kick", False, text_color),
    tip_font.render("decreases your Starpunch cooldown", False, text_color),
    tip_font.render("", False, text_color),
    tip_font.render("#5: Missing Starpunch applies the Overheat", False, text_color),
    tip_font.render("effect, doubling your cooldowns for 2 seconds", False, text_color),
]

mirror_tips = [
    tip_font.render("#1: Blocking the ball as the ability is", False, text_color),
    tip_font.render("used can completely negate it", False, text_color),
    tip_font.render("", False, text_color),
    tip_font.render("#2: If used at the right time, Reflect", False, text_color),
    tip_font.render("may net you a goal", False, text_color),
    tip_font.render("", False, text_color),
    tip_font.render("#3: Mirror Blob shatters easily,", False, text_color),
    tip_font.render("try not to encounter an offensive Blob", False, text_color),
    tip_font.render("like Boxer Blob!", False, text_color),
    tip_font.render("", False, text_color),
    tip_font.render("#4: Reflect's reflection power is much", False, text_color),
    tip_font.render("stronger horizontally than it is vertically.", False, text_color),
    tip_font.render("", False, text_color),
    tip_font.render("#5: Mirror Blob gains a reflection", False, text_color),
    tip_font.render("status effect when using Reflect.", False, text_color),
    tip_font.render("It reduces incoming damage slightly", False, text_color),
    tip_font.render("and reflects that damage to the attacker!", False, text_color),
]

fisher_tips = [
    tip_font.render("#1: Fisher Blob hooks onto the ball", False, text_color),
    tip_font.render("faster if the ball is closeby!", False, text_color),
    tip_font.render("", False, text_color),
    tip_font.render("#2: Fisher Blob is extra vulnerable when", False, text_color),
    tip_font.render("using Hook - he takes +1 damage", False, text_color),
    tip_font.render("from all sources!", False, text_color),
    tip_font.render("", False, text_color),
    tip_font.render("#3: You can block Hook from working by", False, text_color),
    tip_font.render("using your block on the ball!", False, text_color),
    tip_font.render("", False, text_color),
    tip_font.render("#4: A spicy trick you can do is called", False, text_color),
    tip_font.render("Threading the Loop. Jump, hook the ball", False, text_color),
    tip_font.render("and have it spin around you before letting go.", False, text_color),
    tip_font.render("", False, text_color),
    tip_font.render("#5: Kicking Fisher Blob or the ball while", False, text_color),
    tip_font.render("hook is active will force Hook into cooldown.", False, text_color),
]

glue_tips = [
    tip_font.render("#1: Glue Gun shoots its pellets", False, text_color),
    tip_font.render("based on your momentum and direction!", False, text_color),
    tip_font.render("", False, text_color),
    tip_font.render("#2: Once a glue puddle is formed, it", False, text_color),
    tip_font.render("dries up in about three seconds!", False, text_color),
    tip_font.render("", False, text_color),
    tip_font.render("#3: Glue Blob synergizes well with its ", False, text_color),
    tip_font.render("own glue. In fact, you will move slightly", False, text_color),
    tip_font.render("faster across the field!", False, text_color),
    tip_font.render("", False, text_color),
    tip_font.render("#4: In addition to the slowing effect of", False, text_color),
    tip_font.render("the glue, you should remember that your", False, text_color),
    tip_font.render("enemies will have a hard time jumping out", False, text_color),
    tip_font.render("of the glue, and the ball bounces less too!", False, text_color),
    tip_font.render("", False, text_color),
    tip_font.render("#5: For 300 energy, wavedashing will create", False, text_color),
    tip_font.render("several pellets of glue that can cover the", False, text_color),
    tip_font.render("whole field.", False, text_color),
]

arcade_tips = [
    tip_font.render("#1: Cheat Cartridge's initial speed is", False, text_color),
    tip_font.render("based on your momentum and direction!", False, text_color),
    tip_font.render("", False, text_color),
    tip_font.render("#2: Leave a cartridge by your goal so", False, text_color),
    tip_font.render("you can go on the offensive!", False, text_color),
    tip_font.render("", False, text_color),
    tip_font.render("#3: Boost kicking your opponent will leave", False, text_color),
    tip_font.render("a console on the ground. They will be", False, text_color),
    tip_font.render("forcibly teleported after a few seconds,", False, text_color),
    tip_font.render("or alternatively they can hold down to", False, text_color),
    tip_font.render("teleport once the console starts sparking.", False, text_color),
    tip_font.render("", False, text_color),
    tip_font.render("#4: Cartridges have a limited lifespan,", False, text_color),
    tip_font.render("and afterwards Arcade Blob will be teleported.", False, text_color),
]

joker_tips = [
    tip_font.render("#1: Pressing Down lets you close your menu", False, text_color),
    tip_font.render("instantly, but you won't get a refund!", False, text_color),
    tip_font.render("", False, text_color),
    tip_font.render("#2: After closing the menu or buying", False, text_color),
    tip_font.render("something, you won't be able to pick the card", False, text_color),
    tip_font.render("you ignored. Choose wisely!", False, text_color),
    tip_font.render("", False, text_color),
    tip_font.render("#3: Equipping a card means you won't be", False, text_color),
    tip_font.render("able to use that particular action ", False, text_color),
    tip_font.render("until you spend the card. When in doubt,", False, text_color),
    tip_font.render("equip to your Ability or Boost slot!", False, text_color),
]

taco_tips = [
    tip_font.render("#1: Each filling (Meat, Hot Sauce, Cheese, and", False, text_color),
    tip_font.render("Vegan Crunch) has its own cooldown.", False, text_color),
    tip_font.render("", False, text_color),
    tip_font.render("#2: Cheese (Up) increases your jump height", False, text_color),
    tip_font.render("and air control, but you also take extra damage.", False, text_color),
    tip_font.render("When landing, you will summon spires!", False, text_color),
    tip_font.render("", False, text_color),
    tip_font.render("#3: Hot Sauce (Right) increases your", False, text_color),
    tip_font.render("horizontal speed greatly, but you are ", False, text_color),
    tip_font.render("vulnerable to damage.", False, text_color),
    tip_font.render("", False, text_color),
    tip_font.render("#4: Vegan Crunch (Down) decreases the damage you take", False, text_color),
    tip_font.render("and makes your blocks frequent. You also take less damage!", False, text_color),
    tip_font.render("", False, text_color),
    tip_font.render("#5: Meat (Left) increases your kick damage, pierce and", False, text_color),
    tip_font.render("reduces your kick cooldown. The meat is too greasy", False, text_color),
    tip_font.render("for your shell so you take more damage, though.", False, text_color),
]

cactus_tips = [
    tip_font.render("#1: The spike follows the ball, but beware", False, text_color),
    tip_font.render("its travel time! The angle it hits the ball", False, text_color),
    tip_font.render("influences the knockback direction.", False, text_color),
    tip_font.render("", False, text_color),
    tip_font.render("#2: Hitting an opponent with the spike", False, text_color),
    tip_font.render("deals a little damage and stun. It also applies", False, text_color),
    tip_font.render("an effect that reduces energy build rate.", False, text_color),
    tip_font.render("", False, text_color),
    tip_font.render("#3: Cactus Blob's boost kick steals 360", False, text_color),
    tip_font.render("energy (about 20%) from the enemy on hit.", False, text_color),
    tip_font.render("", False, text_color),
    tip_font.render("#4: For 200 energy, Cactus Blob's wavedash will", False, text_color),
    tip_font.render("deal 3 damage to enemies on contact.", False, text_color),
]

merchant_tips = [
    tip_font.render("#1: Merchant Blob can equip charms to buff", False, text_color),
    tip_font.render("himself, but they break over time.", False, text_color),
    tip_font.render("", False, text_color),
    tip_font.render("#2: Passive charms (up) provide effects like", False, text_color),
    tip_font.render("increasing energy build rate, converting taken", False, text_color),
    tip_font.render("damage to energy, and increasing speed.", False, text_color),
    tip_font.render("", False, text_color),
    tip_font.render("#3: Offensive charms (right) provide effects", False, text_color),
    tip_font.render("like gaining energy when dealing damage,", False, text_color),
    tip_font.render("faster kicks, and stronger kicks.", False, text_color),
    tip_font.render("", False, text_color),
    tip_font.render("#4: Focus charms (down) provide effects like", False, text_color),
    tip_font.render("damage reduction, free kicks, and healing.", False, text_color),
    tip_font.render("", False, text_color),
    tip_font.render("#5: Defensive charms (left) provide effects like", False, text_color),
    tip_font.render("damaging wavedashes, gaining the reflect status,", False, text_color),
    tip_font.render("and getting passive damage reduction and faster blocks.", False, text_color),
]

bubble_tips = [
    tip_font.render("#1: Bubbles will float around in circles. The", False, text_color),
    tip_font.render("direction is dependent on the player's team!", False, text_color),
    tip_font.render("", False, text_color),
    tip_font.render("#2: While the ball is caught in a bubble, ", False, text_color),
    tip_font.render("it gains a damaging effect! Touching the ball", False, text_color),
    tip_font.render("will hurt you a little bit.", False, text_color),
    tip_font.render("", False, text_color),
    tip_font.render("#3: While the ball is caught in a bubble,", False, text_color),
    tip_font.render("many abilities will affect the bubble!", False, text_color),
    tip_font.render("", False, text_color),
    tip_font.render("#4: Popping the bubble at any point will launch", False, text_color),
    tip_font.render("the ball, regardless of when or how!", False, text_color),
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
        'fisher': fisher_tips,
        'glue': glue_tips,
        'arcade': arcade_tips,
        'joker': joker_tips,
        'taco': taco_tips,
        'cactus': cactus_tips,
        'merchant': merchant_tips,
        'bubble': bubble_tips,
    }
    try:
        return tips_dict[selected_blob]
    except:
        return []