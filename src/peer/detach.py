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
import subprocess
def detach(hostname,remotehost="localhost"):
    """
Detach ``host`` from the peer group. Failure will raise DetachError or DetachWarning.

If ``remotehost`` is set, detach will be run on remote host.
"""
    try:
        response = subprocess.check_output([
                "/usr/sbin/gluster", 
                "--remote-host=%s" % remotehost, 
                "peer", 
                "detach", 
                hostname])
    except subprocess.CalledProcessError,e:
        response = e.output
        if response[-14:] == " is localhost\n":
            raise Warning(response)
        if response[-24:] == " is not part of cluster\n":
            raise Warning(response)
        if response[:23] == "Brick(s) with the peer ":
            raise Warning(response)
        if response[:36] == "Detach unsuccessful\nDetach returned ":
            raise Exception(response)
    return True
