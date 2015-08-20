#    Copyright 2014, 2015 Joe Julian <me@joejulian.name>
#
#    This file is part of python-gluster.
#
#    python-gluster is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    python-gluster is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with python-gluster.  If not, see <http://www.gnu.org/licenses/>.
#
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
