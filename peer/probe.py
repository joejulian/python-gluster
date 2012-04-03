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
