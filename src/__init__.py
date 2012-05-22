class GlusterError(Exception):
    def __init__(self,value):
        self.value = value
    def _str_(self):
        return repr(self.value)

class GlusterWarning(Warning):
    def __init__(self,value):
        self.value = value
    def _str_(self):
        return repr(self.value)

import os,sys
if not os.geteuid()==0:
    raise GlusterError("Gluster commands require root permissions.")
        
import peer
import volume
