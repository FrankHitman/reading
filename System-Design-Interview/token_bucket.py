import time


class TokenBucket:
    """
    A token bucket class for rate limiting.
    """

    def __init__(self, capacity, refill_rate, last_refill_time=None):
        """
        Initializes a token bucket with a specific capacity and refill rate.

        Args:
          capacity (int): The maximum number of tokens the bucket can hold.
          refill_rate (float): The rate at which tokens are added to the bucket (tokens per second).
          last_refill_time (float, optional): The timestamp of the last refill. Defaults to None.
        """
        self.capacity = capacity
        self.refill_rate = refill_rate
        self.num_tokens = min(capacity, 0 if last_refill_time is None else self._calculate_tokens(last_refill_time))
        self.last_refill_time = last_refill_time or time.time()

    def _calculate_tokens(self, current_time):
        """
        Calculates the number of tokens available based on the refill rate and last refill time.

        Args:
          current_time (float): The current timestamp.

        Returns:
          int: The number of tokens available in the bucket.
        """
        elapsed_time = current_time - self.last_refill_time
        return min(self.capacity, self.num_tokens + (elapsed_time * self.refill_rate))

    def has_tokens(self, num_tokens):
        """
        Checks if the bucket has enough tokens available for a request.

        Args:
          num_tokens (int): The number of tokens required for the request.

        Returns:
          bool: True if enough tokens are available, False otherwise.
        """
        current_tokens = self._calculate_tokens(time.time())
        return current_tokens >= num_tokens

    def consume(self, num_tokens):
        """
        Attempts to consume tokens from the bucket for a request.

        Args:
          num_tokens (int): The number of tokens to consume.

        Returns:
          bool: True if enough tokens were consumed, False otherwise.
        """
        current_tokens = self._calculate_tokens(time.time())
        if current_tokens >= num_tokens:
            self.num_tokens = max(0, current_tokens - num_tokens)
            self.last_refill_time = time.time()
            return True
        return False


# Example usage
bucket = TokenBucket(capacity=10, refill_rate=2.0, last_refill_time=None)  # 10 tokens, refill 2 per second

# Allow requests as long as tokens are available
for _ in range(2):
    if bucket.has_tokens(3):
        # Process request (consume 3 tokens)
        bucket.consume(3)
        print("Request allowed!")
    else:
        print("Request denied! Rate limit exceeded.")
time.sleep(2)
for _ in range(3):
    if bucket.has_tokens(3):
        # Process request (consume 3 tokens)
        bucket.consume(3)
        print("Request allowed!")
    else:
        print("Request denied! Rate limit exceeded.")
time.sleep(2)
for _ in range(2):
    if bucket.has_tokens(3):
        # Process request (consume 3 tokens)
        bucket.consume(3)
        print("Request allowed!")
    else:
        print("Request denied! Rate limit exceeded.")

# output
# Request denied! Rate limit exceeded.
# Request denied! Rate limit exceeded.
# Request allowed!
# Request denied! Rate limit exceeded.
# Request denied! Rate limit exceeded.
# Request allowed!
# Request denied! Rate limit exceeded.
