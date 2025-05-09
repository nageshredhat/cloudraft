import time

def idle_worker():
    while True:
        # periodically sync some stats
        time.sleep(5)
