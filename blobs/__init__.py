from os.path import dirname, basename, isfile, join
import glob
modules = glob.glob(join(dirname(__file__), "*.py"))
print(modules)
from . import *
__all__ = []
#__all__ = [ basename(f)[:-3] for f in modules if isfile(f) and not f.endswith('__init__.py') and not f.endswith('old_blobs.py') and not f.endswith('blobs.py')]
#print(__all__)
#print(__file__)
#print(dirname(__file__))
#print(join(dirname(__file__), "*.py"))
#print(glob.glob(join(dirname(__file__), "*.py")))
#print(__all__)

print("START LOOP")
folders = glob.glob(join(dirname(__file__) + "\\", "*\\"))
#for blob_folder in folders:
#    print(blob_folder)
#    folder_name = blob_folder.split("\\")[-2]
#    print(folder_name)
#    blob_modules = glob.glob(join(dirname(blob_folder), "*.py"))
#    print(blob_modules)
#    folder_paths = [basename(f)[:-3] for f in blob_modules if isfile(f) and not f.endswith('__init__.py')]
#    print(folder_paths)
#    __all__ += folder_paths

import pkgutil

__all__ = []
for loader, module_name, is_pkg in pkgutil.walk_packages(__path__):
    __all__.append(module_name)
    _module = loader.find_module(module_name).load_module(module_name)
    globals()[module_name] = _module

print("FINAL PRODUCT")
print(__all__)
