from collections import deque
import time

class LeakyBucket:
    """
    A leaky bucket class for rate limiting.
    """
    def __init__(self, capacity, leak_rate):
        """
        Initializes a leaky bucket with a specific capacity and leak rate.

        Args:
          capacity (int): The maximum number of requests the bucket can hold.
          leak_rate (float): The rate at which requests are removed from the bucket (requests per second).
        """
        self.capacity = capacity
        self.leak_rate = leak_rate
        self.queue = deque(maxlen=capacity)  # Use deque for efficient queue operations

    def _leak(self, current_time):
        """
        Simulates leaking requests from the bucket based on the leak rate and elapsed time.

        Args:
          current_time (float): The current timestamp.
        """
        if self.queue:
            elapsed_time = current_time - self.queue[0][0]  # Time since oldest request
            to_remove = int(elapsed_time * self.leak_rate)
            print('to remove is', to_remove)
            print('queue is ', self.queue)
            for _ in range(min(to_remove, len(self.queue))):
                self.queue.popleft()

    def allow(self, current_time):
        """
        Checks if the bucket can accept a new request.

        Args:
          current_time (float): The current timestamp.

        Returns:
          bool: True if the request is allowed, False otherwise.
        """
        self._leak(current_time)
        return len(self.queue) < self.capacity

    def add(self, current_time):
        """
        Adds a request to the bucket (if allowed) with a timestamp.

        Args:
          current_time (float): The current timestamp.

        Returns:
          bool: True if the request was added, False otherwise.
        """
        if self.allow(current_time):
            self.queue.append((current_time, None))
            return True
        return False

# Example usage
bucket = LeakyBucket(capacity=5, leak_rate=1.0)  # 5 requests, leak 1 per second

# Allow requests as long as the bucket is not full
for _ in range(7):
    if bucket.add(time.time()):
        print("Request allowed!")
    else:
        print("Request denied! Rate limit exceeded.")

# Simulate some time passing (adjust sleep time as needed)
time.sleep(2)
print('-----sleep over-----')
# Try another request
for _ in range(7):
    if bucket.add(time.time()):
        print("Request allowed!")
    else:
        print("Request denied! Rate limit exceeded.")

# output
# Request allowed!
# to remove is 0
# queue is  deque([(1716269856.6164322, None)], maxlen=5)
# Request allowed!
# to remove is 0
# queue is  deque([(1716269856.6164322, None), (1716269856.616457, None)], maxlen=5)
# Request allowed!
# to remove is 0
# queue is  deque([(1716269856.6164322, None), (1716269856.616457, None), (1716269856.616961, None)], maxlen=5)
# Request allowed!
# to remove is 0
# queue is  deque([(1716269856.6164322, None), (1716269856.616457, None), (1716269856.616961, None), (1716269856.616986, None)], maxlen=5)
# Request allowed!
# to remove is 0
# queue is  deque([(1716269856.6164322, None), (1716269856.616457, None), (1716269856.616961, None), (1716269856.616986, None), (1716269856.6170082, None)], maxlen=5)
# Request denied! Rate limit exceeded.
# to remove is 0
# queue is  deque([(1716269856.6164322, None), (1716269856.616457, None), (1716269856.616961, None), (1716269856.616986, None), (1716269856.6170082, None)], maxlen=5)
# Request denied! Rate limit exceeded.
# -----sleep over-----
# to remove is 2
# queue is  deque([(1716269856.6164322, None), (1716269856.616457, None), (1716269856.616961, None), (1716269856.616986, None), (1716269856.6170082, None)], maxlen=5)
# Request allowed!
# to remove is 2
# queue is  deque([(1716269856.616961, None), (1716269856.616986, None), (1716269856.6170082, None), (1716269858.621387, None)], maxlen=5)
# Request allowed!
# to remove is 2  # 在这一步有问题了，会把最新的删掉一个，即 1716269858.621387
# queue is  deque([(1716269856.6170082, None), (1716269858.621387, None), (1716269858.621431, None)], maxlen=5)
# Request allowed!
# to remove is 0
# queue is  deque([(1716269858.621431, None), (1716269858.621451, None)], maxlen=5)
# Request allowed!
# to remove is 0
# queue is  deque([(1716269858.621431, None), (1716269858.621451, None), (1716269858.6214678, None)], maxlen=5)
# Request allowed!
# to remove is 0
# queue is  deque([(1716269858.621431, None), (1716269858.621451, None), (1716269858.6214678, None), (1716269858.621484, None)], maxlen=5)
# Request allowed!
# to remove is 0
# queue is  deque([(1716269858.621431, None), (1716269858.621451, None), (1716269858.6214678, None), (1716269858.621484, None), (1716269858.6215, None)], maxlen=5)
# Request denied! Rate limit exceeded.
