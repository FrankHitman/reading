import time
from collections import defaultdict


class SlidingWindowCounter:
    """
    A sliding window counter class for rate limiting.
    """

    def __init__(self, window_size, limit):
        """
        Initializes a sliding window counter with a specific window size and request limit.

        Args:
          window_size (float): The size of the time window in seconds.
          limit (int): The maximum number of requests allowed within the window.
        """
        self.window_size = window_size
        self.limit = limit
        self.counts = defaultdict(int)  # Use defaultdict to handle missing timestamps

    def request(self, current_time=None):
        """
        Tracks a request and checks if the rate limit is exceeded.

        Args:
          current_time (float, optional): The current timestamp. Defaults to None (uses time.time()).

        Returns:
          bool: True if the request is allowed, False otherwise.
        """
        current_time = current_time or time.time()
        window_start = current_time - self.window_size

        # Decay counter weights based on time difference from request timestamp
        decay = lambda ts: max(0, 1 - (current_time - ts) / self.window_size)
        # self.counts = {key: value * decay(key) for key, value in self.counts.items()}
        tmp = defaultdict(int)
        for key, value in self.counts.items():
            tmp[key] = value* decay(key)
        self.counts = tmp

        # Update counter for current time window
        self.counts[current_time] += 1

        # Check if the total count within the window exceeds the limit
        total_count = sum(self.counts.values())
        return total_count <= self.limit


# Example usage
counter = SlidingWindowCounter(window_size=1.0, limit=3)  # 1 second window, 3 requests allowed

# Allow requests as long as the limit is not exceeded
for i in range(4):
    if counter.request():
        print(f"Request {i + 1} allowed!")
    else:
        print(f"Request {i + 1} denied! Rate limit exceeded.")
        break

# Wait for the window to slide partially
time.sleep(0.6)  # Sleep for less than the window size

# New requests might be allowed as the window slides and older counts decay
if counter.request():
    print("Request allowed (window slide)")

# output
# Request 1 allowed!
# Request 2 allowed!
# Request 3 allowed!
# Request 4 denied! Rate limit exceeded.
# Request allowed (window slide)
