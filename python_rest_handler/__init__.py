import sys
if sys.version_info[0] == 2:
    from prh import *
else:
    from .prh import *

