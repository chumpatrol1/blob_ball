from bz2 import decompress
from os import getcwd
import time
from json import dumps, loads
import zlib

from resources.graphics_engine.display_controller_pop_up import create_generic_pop_up

def compress_replay_file(string_to_compress, file_str):
    compressed_data = zlib.compress(string_to_compress.encode('ascii'), zlib.Z_BEST_COMPRESSION)
    with open(file_str, "wb") as compressed_v:
        compressed_v.write(compressed_data)
    '''with open("bruh.txt", "w") as compressed_v:
        compressed_v.write(string_to_compress)'''
    

current_replay = None

def check_replay_integrity(current_replay):
    if(len(current_replay[4]) != current_replay[5]['time']):
        create_generic_pop_up(-1)

def decompress_replay_file(file_name): # DANGER: DO NOT USE! WE NEED TO HAVE FILE EXPLORER
    global current_replay
    with open(file_name, "rb") as compressed_v:
        string_to_compress = compressed_v.read()
    decompressed_data = zlib.decompress(string_to_compress).decode('ascii').split('\n')
    #print('seed', decompressed_data[0])
    #print('rules', loads(decompressed_data[1]))
    #print('p1', loads(decompressed_data[2])['species'])
    #print('p2', loads(decompressed_data[2])['species'])

    current_replay = [decompressed_data[0], loads(decompressed_data[1]), loads(decompressed_data[2])['species'], loads(decompressed_data[2])['costume'], loads(decompressed_data[3])['species'], loads(decompressed_data[3])['costume'], loads(decompressed_data[4]), loads(decompressed_data[5])]

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

    string_to_save = str(random_seed) + "\n" + dumps(ruleset) + "\n" + dumps(p1_blob.info) + "\n" + dumps(p2_blob.info) + "\n" + dumps(replay_inputs) + "\n" + dumps(game_info)
    compress_replay_file(string_to_save, file_str)