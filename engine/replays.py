from bz2 import decompress
import time
from json import dumps, loads
import zlib

def compress_replay_file(string_to_compress, file_str):
    compressed_data = zlib.compress(string_to_compress.encode('ascii'), zlib.Z_BEST_COMPRESSION)
    with open(file_str, "wb") as compressed_v:
        compressed_v.write(compressed_data)
    
    with open("compressed", "wb") as compressed_v:
        compressed_v.write(compressed_data)

def decompress_replay_file(): # DANGER: DO NOT USE! WE NEED TO HAVE FILE EXPLORER
    with open("compressed", "rb") as compressed_v:
        string_to_compress = compressed_v.read()
    decompressed_data = zlib.decompress(string_to_compress).decode('ascii').split('\n')
    print('seed', decompressed_data[0])
    print('rules', loads(decompressed_data[1]))
    print('p1', loads(decompressed_data[2])['species'])
    print('p2', loads(decompressed_data[2])['species'])
    #print(decompressed_data)
    #with open("decompressed", "wb") as compressed_v:
    #    compressed_v.write(decompressed_data)

def return_replay_info():
    pass

def save_replay(random_seed, ruleset, replay_inputs, p1_blob, p2_blob):
    current_time = time.localtime()
    time_str = f"{current_time.tm_year}-{current_time.tm_mon}-{current_time.tm_mday} {current_time.tm_hour}.{current_time.tm_min}.{current_time.tm_sec}_"
    identifier = 1
    from os import getcwd
    file_str = getcwd() + '/replays/Blob Ball Replay ' + time_str + str(identifier) + ".bbr"
    from os.path import exists
    
    while exists(file_str + ".bbr"):
        identifier += 1
        file_str = getcwd() + '/replays/Blob Ball Replay ' + time_str + str(identifier) + ".bbr"

    string_to_save = str(random_seed) + "\n" + dumps(ruleset) + "\n" + dumps(p1_blob.info) + "\n" + dumps(p2_blob.info) + "\n" + replay_inputs
    compress_replay_file(string_to_save, file_str)