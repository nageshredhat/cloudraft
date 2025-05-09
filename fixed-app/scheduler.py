import threading
import service

def start_schedulers():
    t = threading.Thread(target=service.idle_worker, daemon=True)
    t.start()
