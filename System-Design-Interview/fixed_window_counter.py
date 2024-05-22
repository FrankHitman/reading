import time
from collections import defaultdict


class FixedWindowCounter:
    """
    A fixed window counter class for rate limiting.
    """

    def __init__(self, window_size, limit):
        """
        Initializes a fixed window counter with a specific window size and request limit.

        Args:
          window_size (float): The size of the time window in seconds.
          limit (int): The maximum number of requests allowed within the window.
        """
        self.window_size = window_size
        self.limit = limit
        self.counts = defaultdict(int)  # Use defaultdict to handle missing keys

    def request(self, current_time=None):
        """
        Tracks a request and checks if the rate limit is exceeded.

        Args:
          current_time (float, optional): The current timestamp. Defaults to None (uses time.time()).

        Returns:
          bool: True if the request is allowed, False otherwise.
        """
        current_time = current_time or int(time.time())
        window_start = current_time - self.window_size

        # Remove expired entries from the counter
        # self.counts = {key: value for key, value in self.counts.items() if key >= window_start}
        tmp = defaultdict(int)
        for key, value in self.counts.items():
            if key >= window_start:
                tmp[key] = value
        self.counts = tmp

        # Check if the current request exceeds the limit
        print(self.counts)
        print(self.counts[current_time])
        self.counts[current_time] += 1
        return self.counts[current_time] <= self.limit


# Example usage
counter = FixedWindowCounter(window_size=1.0, limit=3)  # 1 second window, 3 requests allowed

# Allow requests as long as the limit is not exceeded
for i in range(4):
    if counter.request():
        print(f"Request {i + 1} allowed!")
    else:
        print(f"Request {i + 1} denied! Rate limit exceeded.")
        break

# Wait for the window to reset
time.sleep(1.1)  # Sleep for slightly more than the window size

# New requests allowed after the window resets
if counter.request():
    print("Request allowed (window reset)")

# output
# defaultdict(<class 'int'>, {})
# 0
# Request 1 allowed!
# defaultdict(<class 'int'>, {1716277621: 1})
# 1
# Request 2 allowed!
# defaultdict(<class 'int'>, {1716277621: 2})
# 2
# Request 3 allowed!
# defaultdict(<class 'int'>, {1716277621: 3})
# 3
# Request 4 denied! Rate limit exceeded.
# defaultdict(<class 'int'>, {1716277621: 4})
# 0
# Request allowed (window reset)
