# Top level blobs test
from blobs import *
from engine.blobs.blobs import Blob
class BlobContainer:
    def __init__(self):
        self.blob_dict = {}
        for blob in Blob.__subclasses__():
            temp = blob()
            self.blob_dict[temp.species] = blob
        self.blob_keys = [*self.blob_dict.keys()]
        print(self.blob_keys)

print(BlobContainer().blob_dict)