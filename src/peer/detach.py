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
