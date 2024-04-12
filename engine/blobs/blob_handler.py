
try:
    from .blobs import *
    from .blobs.blobs import Blob
except:
    from blobs import *
    from blobs.blobs import Blob
class BlobContainer:
    def __init__(self):
        self.blob_dict = {}
        for blob in Blob.__subclasses__():
            temp = blob()
            self.blob_dict[temp.species] = blob
        self.blob_keys = [*self.blob_dict.keys()]
        print(self.blob_keys)

    def get_blob(self, blob_id):
        return self.blob_dict[blob_id]

    def return_blob_dict(self):
        return self.blob_dict

    def return_blob_keys(self):
        return self.blob_keys

#blob_list = BlobContainer()
#blob_list = BlobContainer().blob_dict
#print(blob_list)


def get_blob_list():
    global blob_list
    return blob_list

if __name__ == "__main__":
    print("Loading in!")
    BlobContainer()