from os.path import dirname, basename, isfile, join
import glob
#print(dirname(__file__))
modules = glob.glob(join(dirname(__file__), "*.py"))
#print(__path__)
#print(modules)
from . import *
__all__ = []
#__all__ = [ basename(f)[:-3] for f in modules if isfile(f) and not f.endswith('__init__.py') and not f.endswith('old_blobs.py') and not f.endswith('blobs.py')]
#print(__all__)
#print(__file__)
#print(dirname(__file__))
#print(join(dirname(__file__), "*.py"))
#print(glob.glob(join(dirname(__file__), "*.py")))
#print(__all__)

#print("START LOOP")
'''folders = glob.glob(join(dirname(__file__) + "\\", "*\\"))
for blob_folder in folders:
    print(blob_folder)
    folder_name = blob_folder.split("\\")[-2]
    print(folder_name)
    blob_modules = glob.glob(join(dirname(blob_folder), "*.py"))
    print(blob_modules)
    folder_paths = [basename(f)[:-3] for f in blob_modules if isfile(f) and not f.endswith('__init__.py')]
    print(folder_paths)
    __all__ += folder_paths'''

import sys, pkgutil, traceback

def onerror(name):
    print("Error importing module %s" % name)
    type, value, traceback = sys.exc_info()
    traceback.print_tb(traceback)

__all__ = []
for loader, module_name, is_pkg in pkgutil.walk_packages(__path__, onerror=onerror):
    __all__.append(module_name)
    _module = loader.find_module(module_name).load_module(module_name)
    globals()[module_name] = _module

#print("FINAL PRODUCT")
#print(__all__)

import blobs.arcade.arcade
import blobs.boxer.boxer
import blobs.bubble.bubble
import blobs.cactus.cactus
import blobs.cop.cop
import blobs.doctor.doctor
import blobs.fire.fire
import blobs.fisher.fisher
import blobs.glue.glue
import blobs.ice.ice
import blobs.joker.joker
import blobs.judge.judge
import blobs.king.king
import blobs.lightning.lightning
import blobs.merchant.merchant
import blobs.mirror.mirror
import blobs.monk.monk
import blobs.quirkless.quirkless
import blobs.random.random
import blobs.rock.rock
import blobs.taco.taco
import blobs.water.water
import blobs.wind.wind