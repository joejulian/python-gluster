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
import subprocess,re

def create(voldef={},remotehost="localhost"):
    """
Create a volume

If ``remotehost`` is set, volume info will be retrieved from the remote host.
"""
    brickdiv = 1

    if not "name"   in voldef.keys():
        raise KeyError("Volume must have a name")
    if not "bricks" in voldef.keys():
        raise KeyError("Volume must have bricks")

    program = ["/usr/sbin/gluster", 
            "--remote-host=%s" % remotehost, 
            "volume", 
            "create",
            voldef["name"],
            ]
    if "stripe" in voldef.keys():
        stripe = int(voldef["stripe"])
        program.append("stripe")
        program.append(str(stripe))
        brickdiv = stripe
    if "replica" in voldef.keys():
        replica = int(voldef["replica"])
        program.append("replica")
        program.append(str(replica))
        brickdiv = brickdiv * replica
    if "transport" in voldef.keys():
        transport = voldef["transport"] if voldef["transport"] in ("tcp","rdma","tcp,rdma","rdma,tcp") else "tcp"
        program.append("transport")
        program.append(transport)
    if len(voldef["bricks"]) % brickdiv:
        raise KeyError("Invalid brick count. Bricks must be in multiples of %d" % brickdiv)
    [ program.append(x) for x in voldef["bricks"] ]

    response = subprocess.check_output(program).split("\n")
    success = "Creation of volume %s has been successful. Please start the volume to access data." % voldef["name"]
    if not success in response:
        raise RuntimeError(response)

    return True
