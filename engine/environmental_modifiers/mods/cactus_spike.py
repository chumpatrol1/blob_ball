from .base_class import em_base_class # Main Class
from math import sin, cos, radians, pi
# em_ prefix is to signify in other files that it's an Environment Modifier.
class em_cactus_spike(em_base_class):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs) # Do not touch. You can add special functionality after this line.
