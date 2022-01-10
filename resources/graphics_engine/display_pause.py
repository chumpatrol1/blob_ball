snapshot = None
def capture_gameplay(game_surface):
    global snapshot
    snapshot = game_surface.copy()

def draw_pause_background(game_surface):
    global snapshot
    game_surface.blit(snapshot, (0, 0))