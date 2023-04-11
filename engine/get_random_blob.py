import random
from engine.unlocks import return_blob_unlock_set

def get_random_blob():
    blob_set = return_blob_unlock_set()
    return random.choice(blob_set)