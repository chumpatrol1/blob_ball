from bz2 import decompress
from os import getcwd
import time
from json import dumps, loads
import zlib

from resources.graphics_engine.display_controller_pop_up import create_generic_pop_up

def compress_replay_file(string_to_compress, file_str):
    full_string = string_to_compress
    #print(full_string)
    compressed_data = zlib.compress(full_string.encode('ascii'), zlib.Z_BEST_COMPRESSION)
    with open(file_str, "wb") as compressed_v:
        compressed_v.write(compressed_data)
    '''with open("bruh.txt", "w") as compressed_v:
        compressed_v.write(string_to_compress)'''
    

current_replay = None

def check_replay_integrity(current_replay):
    # Compare the inputs we stored to the amount of time shown in the gameplay
    #print(len(current_replay[6]), current_replay[7]['time'] + 1)
    if(len(current_replay[6]) != current_replay[7]['time'] + 1):
        create_generic_pop_up(-1)

def decompress_replay_file(file_name): # DANGER: DO NOT USE! WE NEED TO HAVE FILE EXPLORER
    global current_replay
    with open(file_name, "rb") as compressed_v:
        string_to_compress = compressed_v.read()
    decompressed_data = zlib.decompress(string_to_compress).decode('ascii')
    #print('seed', decompressed_data[0])
    #print('rules', loads(decompressed_data[1]))
    #print('p1', loads(decompressed_data[2])['species'])
    #print('p2', loads(decompressed_data[2])['species'])
    #print(type(decompressed_data))
    #print(decompressed_data)
    loaded_replay = loads(decompressed_data)
    current_replay = [loaded_replay[0], loaded_replay[1], loaded_replay[2]['species'], loaded_replay[2]['costume'], loaded_replay[3]['species'], loaded_replay[3]['costume'], loaded_replay[4], loaded_replay[5]]
    print(current_replay[7])
    check_replay_integrity(current_replay)
    #print(decompressed_data[4].split('/'))
    #print(decompressed_data)
    #with open("decompressed", "wb") as compressed_v:
    #    compressed_v.write(zlib.decompress(string_to_compress))

def return_replay_info():
    return current_replay

def save_replay(random_seed, ruleset, replay_inputs, p1_blob, p2_blob, game_info):
    current_time = time.localtime()
    time_str = f"{current_time.tm_year}-{current_time.tm_mon}-{current_time.tm_mday} {current_time.tm_hour}.{current_time.tm_min}.{current_time.tm_sec}_"
    identifier = 1
    from os import getenv
    file_str = getenv('APPDATA')+'/BlobBall' + '/replays/' + p1_blob.species.capitalize() + " vs " + p2_blob.species.capitalize() + " " + time_str + str(identifier) + ".bbr"
    from os.path import exists
    
    while exists(file_str + ".bbr"):
        identifier += 1
        file_str = getenv('APPDATA')+'/BlobBall' + '/replays/' + p1_blob.species.capitalize() + " vs " + p2_blob.species.capitalize() + " " + time_str + str(identifier) + ".bbr"
    json_to_save = dumps([str(random_seed), ruleset, p1_blob.info, p2_blob.info, replay_inputs, game_info])
    compress_replay_file(json_to_save, file_str)