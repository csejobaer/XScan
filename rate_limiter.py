# rate_limiter.py

import time
import random

class RateLimiter:

    def __init__(self, delay=1.0):
        self.delay = delay
        self.last_request = 0

    def wait(self):

        now = time.time()

        elapsed = now - self.last_request

        if elapsed < self.delay:
            time.sleep(self.delay - elapsed)

        # small random delay to avoid pattern detection
        time.sleep(random.uniform(0.1, 0.3))

        self.last_request = time.time()
