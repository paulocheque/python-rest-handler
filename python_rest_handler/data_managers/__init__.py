import sys
if sys.version_info[0] == 2:
    from mongoengine import *
else:
    from .mongoengine import *

