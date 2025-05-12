import json
import time
import datetime
import socket
import struct
import configparser
import os

def check_time_sync(conn):
    result = {"time_sync_status": "unknown", "details": {}}
    
    # Load domain controller from config
    config = configparser.ConfigParser()
    config.read('config.ini')
    domain_controller = os.getenv('AD_DOMAIN_CONTROLLER', config['DEFAULT']['domain_controller'])

    try:
        # Simple NTP-like check using UDP to port 123 (basic implementation)
        client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        client.settimeout(5)
        data = b'\x1b' + 47 * b'\0'
        client.sendto(data, (domain_controller, 123))
        data, _ = client.recvfrom(1024)
        t = struct.unpack('!12I', data)[10]
        t -= 2208988800  # Convert NTP time to Unix epoch
        dc_time = datetime.datetime.fromtimestamp(t)
        local_time = datetime.datetime.now()
        time_diff = abs((dc_time - local_time).total_seconds())

        result["details"] = {
            "dc_time": str(dc_time),
            "local_time": str(local_time),
            "time_difference_seconds": time_diff
        }
        result["time_sync_status"] = "in_sync" if time_diff < 5 else "out_of_sync"
    except Exception as e:
        result["time_sync_status"] = "failed"
        result["details"]["error"] = str(e)

    return result