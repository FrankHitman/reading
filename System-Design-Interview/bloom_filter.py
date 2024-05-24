class BloomFilter:
    """
    A Bloom filter class for probabilistic membership testing.
    """

    def __init__(self, size, num_hash_funcs):
        """
        Initializes a Bloom filter with a specific size and number of hash functions.

        Args:
          size (int): The size of the bit array.
          num_hash_funcs (int): The number of hash functions to use.
        """
        self.size = size
        self.num_hash_funcs = num_hash_funcs
        self.bit_array = bytearray(size // 8)  # Efficient bit array using bytearray

    def __hash_element(self, element):
        """
        Hashes an element using multiple hash functions.

        Args:
          element: The element to hash.

        Returns:
          list: A list of hash values for the element.
        """
        return [hash(element) % self.size for _ in range(self.num_hash_funcs)]

    def add(self, element):
        """
        Adds an element to the Bloom filter.

        Args:
          element: The element to add.
        """
        for hash_value in self.__hash_element(element):
            self.bit_array[hash_value // 8] |= (1 << (hash_value % 8))  # Set the corresponding bit

    def check(self, element):
        """
        Checks if an element is possibly present in the Bloom filter.

        Args:
          element: The element to check.

        Returns:
          bool: True if the element might be present, False otherwise.
        """
        for hash_value in self.__hash_element(element):
            if (self.bit_array[hash_value // 8] & (1 << (hash_value % 8))) == 0:
                return False  # One bit is not set, so element is definitely not present
        return True  # All bits are set, element might be present (possible false positive)


# Example usage
bloom_filter = BloomFilter(size=1024, num_hash_funcs=3)
bloom_filter.add("apple")
bloom_filter.add("banana")
print(bloom_filter.bit_array)

if bloom_filter.check("apple"):
    print("Apple might be in the set.")
else:
    print("Apple is definitely not in the set.")

if bloom_filter.check("orange"):  # False positive
    print("Orange might be in the set.")
else:
    print("Orange is definitely not in the set.")

# hash 函数可以生成固定 19 位的结果，相同输入对应相同输出。
# >>> hash('1')
# -8265630591234824463
# >>> hash('1')%1024
# 753
# >>> 753//8
# 94
# >>> 753%8
# 1
# >>> 1<<(753%8)
# 2
# >>> 0|1
# 1
# >>> 1|1
# 1
# >>> 0|0
# 0
# >>> a = bytearray(128)
# >>> a
# bytearray(b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00')
# 以上是 16 进制表示的 128 个字节的 bytearray。一个字节 8 bit位 1|2|4|8| 0000 0000，4个bit位表示一个十六进制数



# output
# bytearray(b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00')
# Apple might be in the set.
# Orange is definitely not in the set.
