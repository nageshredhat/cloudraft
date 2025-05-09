import collector
import random
import time

def trigger_background_collection():
    delay = random.randint(180, 30)
    time.sleep(delay)
    collector.launch_collector()
