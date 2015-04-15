import subprocess,re

def status(remotehost="localhost"):
    """
Retrieve the status of the peer group.

Returns a dict in the form of:
{'host': {'server1': {'state': {'server2': 'Peer in Cluster (Connected)', 'server3': 'Peer in Cluster (Connected)', 'server4': 'Peer in Cluster (Connected)'}, 'uuid': '2d85014b-3e4c-4b53-b274-c25d2fa14771'}, 'server4': {'state': {'server1': 'Peer in Cluster (Connected)', 'server3': 'Peer in Cluster (Connected)', 'server2': 'Peer in Cluster (Connected)'}, 'uuid': 'fcac92e9-b7c5-440a-bac0-8fb6dfe4b899'}, 'server3': {'state': {'server1': 'Peer in Cluster (Connected)', 'server2': 'Peer in Cluster (Connected)', 'server4': 'Peer in Cluster (Connected)'}, 'uuid': '09366c55-a8b6-4b27-b23b-ee40bb9fd224'}, 'server2': {'state': {'server1': 'Peer in Cluster (Connected)', 'server3': 'Peer in Cluster (Connected)', 'server4': 'Peer in Cluster (Connected)'}, 'uuid': '68211a37-3497-4920-a86a-128db5e0fe49'}}, 'peers': 4}

If ``remotehost`` is set, status will be run on remote host.
"""
    return _status(remotehost)

def _status(remotehost="localhost",recursion=False):
    peerstatus = {"host": {},}
    program = ["/usr/sbin/gluster", 
            "--remote-host=%s" % remotehost, 
            "peer", 
            "status"]
    try:
        response = subprocess.check_output(program,stderr=subprocess.STDOUT).split("\n")
    except subprocess.CalledProcessError,e:
        print e.output
        raise

    # step through the output and build the dict
    for line in response:
        if line == "No peers present":
            peerstatus["peers"] = 0
            return peerstatus
        m = re.match("^Number of Peers: (\d+)$", line)
        if m:
            peerstatus["peers"] = int(m.group(1)) + 1
        m = re.match("^Hostname: (.+)$", line)
        if m:
            hostname = m.group(1)
            peerstatus["host"][hostname] = {}
            peerstatus["host"][hostname]["state"] = {}
        m = re.match("Uuid: ([-0-9a-f]+)", line)
        if m:
            peerstatus["host"][hostname]["uuid"] = m.group(1)

    # our first pass through
    if not recursion:
        remotehost = [x for x in 
                _status(remotehost=peerstatus["host"].keys()[0],recursion=True)["host"].keys()
                if x not in peerstatus["host"].keys()][0]
        peerstatus["host"][remotehost] = {}
        peerstatus["host"][remotehost]["self"] = True
        peerstatus["host"][remotehost]["state"] = {}
        for host in peerstatus["host"].keys():
            if host != remotehost:
                peerstatus["host"][remotehost]["uuid"] = _status(remotehost=host,recursion=True)["host"][remotehost]["uuid"]
            remotestatus = _status(host,recursion=True)
            for statehost in remotestatus["host"]:
                for state in remotestatus["host"][statehost]["state"]:
                    peerstatus["host"][statehost]["state"][state] = remotestatus["host"][statehost]["state"][state]
    for line in response:
        m = re.match("^Hostname: (.+)$", line)
        if m:
            hostname = m.group(1)
        m = re.match("State: (.+)", line)
        if m:
            peerstatus["host"][hostname]["state"][remotehost] = m.group(1)

    return peerstatus
