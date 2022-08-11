from urllib import request
from engine.initializer import return_game_version
import re
import os

from resources.graphics_engine.display_controller_pop_up import create_generic_pop_up
def currentVer():
    '''
    Outputs:
        - Version of the game that you just opened
    '''
    f = os.getenv('APPDATA')+"/BlobBall/config/ruleset.txt"
    f2=open(f, "r")
    f3=f2.read()
    f2.close()
    #return f3[13:20]
    return return_game_version()
def compare(game_ver, site_ver):
    '''
    Inputs:
        - game_ver: The version of the game that is currently up
        - site_ver: The version posted on the blobball.com website

    Outputs:
        - String ("New Version Available" when game_ver is older than site_ver, "Up to Date" otherwise)
    '''
    game_split = game_ver.split(".")
    game_split.append(game_ver[-1])
    game_split[2] = game_split[2][:-1]
    site_split = site_ver.split(".")
    site_split.append(site_ver[-1])
    site_split[2] = site_split[2][:-1]


    for v in zip(game_split, site_split):
        if(v[0] < v[1]):
            return True # New Version Available!
        elif(v[0] > v[1]):
            return False # Up to Date!
    
    return False # Up to Date!
def check_for_game_updates():
    try:
        resp = request.urlopen("http://blobball.com/")
        if(resp.code == 200):
            data = resp.read()
            html = data.decode("UTF-8")
            extract_flag = False
            extraction = []
            for line in html.split("\n"):
                if("<!--" in line):
                    extract_flag = True
                elif(extract_flag):
                    if("-->" in line):
                        extract_flag = False
                        break
                    else:
                        extraction.append(line)

            site_ver = "0.0.1a"
            for extracted in extraction:
                if("GAMEVER" in extracted):
                    site_ver = extracted.split("= ")[1]

            game_ver = currentVer()
            if(compare(game_ver, site_ver)):
                create_generic_pop_up(1)
            else:
                create_generic_pop_up(2)
            
        else:
            create_generic_pop_up(3)
            print("Something went wrong connecting, CODE: ",resp.code)
    except:
        create_generic_pop_up(3)

if(__name__ == "__main__"):
    assert compare("0.0.1a", "0.0.1a") == "Up to Date"
    assert compare("0.15.0b", "0.0.1b") == "Up to Date"
    assert compare("0.16.0b", "0.16.1b") == "New Version Available"
    assert compare("0.16.1b", "0.16.11a") == "New Version Available"
    assert compare("0.0.1a", "0.0.1b") == "New Version Available"