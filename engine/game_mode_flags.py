game_mode = "classic"
# classic: Standard Blob Ball Match. KO blobs or score goals to earn points
# squadball: 3 on 3 battle. KO opposing blobs or score goals to win
# colloseum: Duels battle. Gain items and power over time and KO your opponent a set number of times to win

def return_game_mode():
    global game_mode
    return game_mode

def set_game_mode(new_game_mode):
    global game_mode
    game_mode = new_game_mode