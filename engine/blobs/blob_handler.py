# .blubs import *
#from .blobs.blobs import Blob
from blobs import *
from engine.blobs.blobs import Blob
from json import loads

class BlobContainer:
    def __init__(self):
        self.blob_dict = {}
        #print(Blob.__subclasses__())
        for blob in Blob.__subclasses__():
            temp = blob()
            self.blob_dict[temp.species] = blob
        self.blob_keys = [*self.blob_dict.keys()]
        Blob.clear_sprite_collisions()
        #print(self.blob_keys)

    def get_blob(self, blob_id):
        return self.blob_dict[blob_id]

    def return_blob_dict(self):
        return self.blob_dict

    def return_blob_keys(self):
        return self.blob_keys

blob_list = BlobContainer()
#blob_list = BlobContainer().blob_dict

#print("~"*100)
#print(blob_list.return_blob_dict())


def get_blob_list():
    global blob_list
    return blob_list

if __name__ == "__main__":
    print("Loading in!")
    BlobContainer()