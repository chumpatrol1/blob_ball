# Add a new import here for each modifier.
from os.path import dirname, basename, isfile, join
import glob
modules = glob.glob(join(dirname(__file__), "*.py"))
__all__ = [ basename(f)[:-3] for f in modules if isfile(f) and not f.endswith('__init__.py') and not f.endswith('old_blobs.py') and not f.endswith('blobs.py')]
#print("Shokupan W")
#print(modules)
#print(__all__)
#print(dir())