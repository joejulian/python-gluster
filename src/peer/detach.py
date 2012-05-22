import subprocess

def detach(hostname,remotehost="localhost"):
    """
Detach ``host`` from the peer group. Failure will raise DetachError or DetachWarning.

If ``remotehost`` is set, detach will be run on remote host.
"""
    response = subprocess.check_output([
            "/usr/sbin/gluster", 
            "--remote-host=%s" % remotehost, 
            "peer", 
            "detach", 
            hostname])
    if response[-13:] == " is localhost":
        raise DetachWarning, response
    if response[-23:] == " is not part of cluster":
        raise DetachWarning, response
    if response[:23] == "Brick(s) with the peer ":
        raise DetachWarning, response
    if response[:36] == "Detach unsuccessful\nDetach returned ":
        raise DetachError, response
    return true
