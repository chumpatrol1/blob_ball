from os.path import dirname, basename, isfile, join
import glob
#print(dirname(__file__))
modules = glob.glob(join(dirname(__file__), "*.py"))
#print(__name__)
#print(modules)

import os
#for path, subdirs, files in os.walk("."):
#    for name in files:
#        print(os.path.join(path, name))
#print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
#for path, subdirs, files in os.walk("."):
#    print(subdirs)

#print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
subdirs = next(os.walk('.'))[1]
#print(subdirs)

with open("blob_imports.txt", "w") as f:
    for subdir in subdirs:
        f.write(f"import blobs.{subdir}.{subdir}\n")