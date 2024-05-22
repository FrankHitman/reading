import time
from collections import deque


class SlidingWindowLog:
    """
    A sliding window log class for rate limiting.
    """

    def __init__(self, window_size, limit):
        """
        Initializes a sliding window log with a specific window size and request limit.

        Args:
          window_size (float): The size of the time window in seconds.
          limit (int): The maximum number of requests allowed within the window.
        """
        self.window_size = window_size
        self.limit = limit
        self.window = deque(maxlen=int(window_size * 1000))  # milliseconds for timer resolution

    def request(self, current_time=None):
        """
        Tracks a request and checks if the rate limit is exceeded.

        Args:
          current_time (float, optional): The current timestamp in milliseconds. Defaults to None (uses time.time()).

        Returns:
          bool: True if the request is allowed, False otherwise.
        """
        current_time = int(current_time * 1000) if current_time else int(time.time() * 1000)

        # Remove expired entries from the window
        while self.window and self.window[0] <= current_time - self.window_size * 1000:
            self.window.popleft()

        # Check if the current request exceeds the limit
        self.window.append(current_time)
        return len(self.window) <= self.limit


# Example usage
window = SlidingWindowLog(window_size=1.0, limit=3)  # 1 second window, 3 requests allowed

# Allow requests as long as the limit is not exceeded
for i in range(4):
    if window.request():
        print(f"Request {i + 1} allowed!")
    else:
        print(f"Request {i + 1} denied! Rate limit exceeded.")
        break

# Wait for the window to slide partially
time.sleep(0.6)  # Sleep for less than the window size

# New requests might be allowed as the window slides
if window.request():
    print("Request allowed (window slide)")

# output
# Request 1 allowed!
# Request 2 allowed!
# Request 3 allowed!
# Request 4 denied! Rate limit exceeded.
