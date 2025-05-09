from flask import Flask
import threading
import metrics
import utils

app = Flask(__name__)
counter = 0
lock = threading.Lock()

@app.route('/')
def home():
    return "Metrics Dashboard 📈"

@app.route('/counter')
def counter_page():
    global counter
    with lock:
        counter += 1
        current_count = counter

    # Safely trigger background collection
    if current_count % 2 == 0:
        try:
            metrics.trigger_background_collection()
        except Exception as e:
            app.logger.error(f"Error in background collection: {e}")

    return f"Counter value: {current_count}"

if __name__ == "__main__":
    utils.initialize_services()
    app.run(host="0.0.0.0", port=8080, threaded=True)

