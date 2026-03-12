# threading_helper.py
import threading

def run_threads(function, items, max_threads=10):
    threads = []
    for i in items:
        t = threading.Thread(target=function, args=(i,))
        threads.append(t)
        t.start()

        # Limit concurrent threads
        while threading.active_count() > max_threads:
            pass

    for t in threads:
        t.join()
