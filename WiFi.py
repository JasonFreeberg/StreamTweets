import socket
import subprocess
import time


def connected(host="8.8.8.8", port=53, timeout=10):
    """
    Helper function for persistConnection().
    Returns true if a connection was established
    Returns false if not.
    Timeout in MINUTES.


    Host: 8.8.8.8 (google-public-dns-a.google.com)
    OpenPort: 53/tcp
    Service: domain (DNS/TCP)
    """
    try:
        socket.setdefaulttimeout(timeout)
        socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect((host, port))
        # For testing
        # print 'Connection established.'
        return True
    except Exception as ex:
        print '#####', 'WARN:', ex
        return False


def persistConnection(timeoutMinutes=2, trys=1, cumTimeOut=0):
    """
    * Don't fuck with trys and cumTimeOut *
    Recursively try to re-establish WiFi connection.
    Exponentially back off.

    timeOutMinutes: Total time to wait while trying to reconnect
    Trys: Reconnection tries
    cumTimeOut: Running total of waiting time
    """
    # Convert minutes to seconds
    timeout = timeoutMinutes * 60

    # Check initial connection
    if connected():
        return True

    else:
        # Something went wrong
        # Connection wasn't estabished, wait
        # If: wait time exceeds timeout, stop and return False
        # Else: turn WiFi off then on
        print '#####', 'WARN: WiFi dropped, reconnecting.'
        while not connected():
            timeToSleep = 2 ** trys
            cumTimeOut += timeToSleep
            if cumTimeOut >= timeout:
                print '#####', 'ERROR: Connection timeout reached. Tried', trys, 'reconnections.'
                return False
            else:
                print '#####', 'Wait', timeToSleep, 'seconds.'
                subprocess.call(['networksetup', '-setairportpower', 'en0', 'off'])
                subprocess.call(['networksetup', '-setairportpower', 'en0', 'on'])
                time.sleep(timeToSleep)
                trys += 1
                time.sleep(1)
        return True
