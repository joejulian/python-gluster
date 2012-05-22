import subprocess,re

def info(volname="all",remotehost="localhost"):
    """
Retrieve the volume information

Returns a dict in the form of:
    {'myvol1': {'bricks': ['server1:/data/a_myvol1/brickroot', 'server2:/data/a_myvol1/brickroot', 'server3:/data/a_myvol1/brickroot', 'server1:/data/b_myvol1/brickroot', 'server2:/data/b_myvol1/brickroot', 'server3:/data/b_myvol1/brickroot', 'server1:/data/c_myvol1/brickroot', 'server2:/data/c_myvol1/brickroot', 'server3:/data/c_myvol1/brickroot', 'server1:/data/d_myvol1/brickroot', 'server2:/data/d_myvol1/brickroot', 'server3:/data/d_myvol1/brickroot'], 'status': 'Started', 'type': 'Distributed-Replicate', 'options': {'performance.quick-read': 'off', 'performance.write-behind': 'off', 'performance.io-thread-count': '1', 'performance.io-cache': 'off', 'performance.read-ahead': 'off', 'performance.flush-behind': 'off'}, 'transport': ['tcp']}}

If ``remotehost`` is set, volume info will be retrieved from the remote host.
"""
    volumes = {}
    program = ["/usr/sbin/gluster", 
            "--remote-host=%s" % remotehost, 
            "volume", 
            "info",
            volname]
    try:
        response = subprocess.check_output(program,stderr=subprocess.STDOUT).split("\n")
    except subprocess.CalledProcessError,e:
        print e.output
        raise
    

    for line in response:
        m = re.match("Volume Name: (.+)",line)
        if m:
            volname = m.group(1)
            volumes[volname] = {"bricks": [], "options": {}}
        m = re.match("Type: (.+)",line)
        if m:
            volumes[volname]["type"] = m.group(1)
        m = re.match("Status: (.+)",line)
        if m:
            volumes[volname]["status"] = m.group(1)
        m = re.match("Transport-type: (.+)",line)
        if m:
            volumes[volname]["transport"] = [x.strip() for x in m.group(1).split(",")]
        m = re.match("Brick[1-9][0-9]*: (.+)",line)
        if m:
            volumes[volname]["bricks"].append(m.group(1))
        m = re.match("^([-.a-z]+: .+)$",line)
        if m:
            # TODO this is pretty lazy. Would be better to have the list of all
            #      options and their defaults, then update from matches
            opt,value = [x.strip() for x in m.group(1).split(":")]
            volumes[volname]["options"][opt] = value
    return volumes

