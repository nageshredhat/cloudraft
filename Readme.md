## Architecture diagram
![](https://lh7-rt.googleusercontent.com/docsz/AD_4nXebAFJ04ku9XHDW5z3c1Om_SPOe1Mr8eXTeKbEseq3RuYTiITJEAsaRe65vK2jBaYzK_u4hbF2HXsZJDSqFku0_QLANJFEX48Ixg6HCmog73fGU5AM5Y_RaO_iag9JVaQsRUoH6FA?key=vUvFrm-5SMd3IIP1U_FR1w)
## THE ARGO APP
![](https://lh7-rt.googleusercontent.com/docsz/AD_4nXdH0nGmdsYZs4Ri-l4rum1N4ydqEpFi6sttpC8LpfkkXH2IRe-_XAMfWIhvXB8lUnGJ60hsoxv6xPOHou6AgvEA3sFY4YXq9crmsWzQ67IUVXKzbW0citjnp_PcW61OBIGTBSyKvQ?key=vUvFrm-5SMd3IIP1U_FR1w)
## Testing Summary and Bug Fix

### Overview

Before deploying this application, I performed basic testing on the Python-based counter API. The application increments a counter with each API hit to the following endpoint:


`GET /counter` 

Expected behavior:  
Each request should return the incremented counter value, like:


`Counter value:  1  Counter value:  2  Counter value:  3  ...` 

----------

### ❌ Issue Observed

During testing via:


`curl localhost:8080/counter` 

I observed **inconsistent behavior**. Every second (even-numbered) request resulted in a `500 Internal Server Error`. Example output:


`$ curl localhost:8080/counter
Counter value: 1

$ curl localhost:8080/counter
500 Internal Server Error

$ curl localhost:8080/counter
Counter value: 3

$ curl localhost:8080/counter
500 Internal Server Error` 

----------

### ✅ Root Cause

-   The application used a **global `counter` variable** without proper **thread synchronization**, leading to **race conditions** when accessed concurrently.
    
-   The function `metrics.trigger_background_collection()` was executed on even counts, and if it raised an exception, it caused a **server crash**.
    

----------

### 🛠️ Fix Implemented

-   Added a **thread lock** (`threading.Lock`) to ensure thread-safe access to the counter.
    
-   Wrapped the call to `metrics.trigger_background_collection()` in a `try-except` block to gracefully handle any runtime errors.
    
The fix ready file `app.py`:
```
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

```
These changes ensure the application runs reliably under concurrent access without crashing.
