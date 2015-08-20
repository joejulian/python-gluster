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

def probe(hostname,remotehost="localhost"):
    """
Add ``host`` to the peer group. Failure will raise ProbeError or ProbeWarning.

If ``remotehost`` is set, probe will be run on remote host.
"""
    response = subprocess.check_output([
            "/usr/sbin/gluster", 
            "--remote-host=%s" % remotehost, 
            "peer", 
            "probe", 
            host])
    if response == "Probe on localhost not needed":
        raise ProbeWarning, response
    if response[:13] == "Probe on host":
        raise ProbeWarning, response
    if response[:33] == "Probe returned with unknown errno":
        raise ProbeError, response
    return true
