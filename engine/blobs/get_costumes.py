from json import loads
def species_to_image(species, costume):
    '''
    Receives a species and costume number, and returns path to costume image
    Inputs
        - species (str): Name of species, typically lowercase
        - costume (int): Costume number. 0 is default
    '''
    try:
        print(f"blobs\\{species}\\init.blob")
        with open(f"blobs\\{species}\\init.blob", "r") as f:
            init_file = f.read()
    except:
        return {"alive": "shadow_blob.png"}
    return loads(init_file)["costumes"][str(costume)]