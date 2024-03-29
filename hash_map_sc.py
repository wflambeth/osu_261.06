# Name: Will Lambeth
# OSU Email: lambethw@oregonstate.edu
# Course: CS261 - Data Structures
# Assignment: 06 part 1 - Hash map with separate chaining
# Due Date: 03 June 2022    
# Description: An implementation of a hash map using separate chaining to resolve collisions.
#              Includes additional method to find the mode of a given hash map. 


from a6_include import (DynamicArray, LinkedList, SLNode,
                        hash_function_1, hash_function_2)


class HashMap:
    def __init__(self, capacity: int, function) -> None:
        """
        Initialize new HashMap that uses
        separate chaining for collision resolution
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self._buckets = DynamicArray()
        for _ in range(capacity):
            self._buckets.append(LinkedList())

        self._capacity = capacity
        self._hash_function = function
        self._size = 0

    def __str__(self) -> str:
        """
        Override string method to provide more readable output
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        out = ''
        for i in range(self._buckets.length()):
            out += str(i) + ': ' + str(self._buckets[i]) + '\n'
        return out

    def get_size(self) -> int:
        """
        Return size of map
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return self._size

    def get_capacity(self) -> int:
        """
        Return capacity of map
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return self._capacity

    # ------------------------------------------------------------------ #

    def put(self, key: str, value: object) -> None:
        """
        Takes a key-value pair and stores it in the hash table. If an
        element already exists with that key, updates its value instead.
        """

        bucket = self._get_bucket(key)
        for node in bucket: 
            # Update value with provided key, if already exists
            if node.key == key:
                node.value = value
                return
        
        # If not, add this value to the list and increment size 
        bucket.insert(key, value)
        self._size += 1

    def empty_buckets(self) -> int:
        """
        Returns the number of buckets in the current hash table which
        contain no elements. 
        """
        empty_count = 0

        for i in range(self._buckets.length()):
            if self._buckets[i].length() == 0:
                empty_count += 1
        
        return empty_count
        
    def table_load(self) -> float:
        """
        Returns the load factor of the current hash table. 
        """
        return self._size / self._capacity

    def clear(self) -> None:
        """
        Empties the current hash table of its contents, while
        preserving its capacity. 
        """
        self._size = 0
        self._buckets = DynamicArray()

        for _ in range(self._capacity):
            self._buckets.append(LinkedList())

    def resize_table(self, new_capacity: int) -> None:
        """
        Resizes the hash table to given capacity, re-hashing and storing
        existing elements. Does nothing if provided capacity is < 1.
        """
        if new_capacity < 1: 
            return
        
        # Instantiate new bucket list with provided capacity, fill with empty lists
        old_buckets = self._buckets
        self._buckets = DynamicArray()
        self._capacity = new_capacity
        self._size = 0
        for _ in range(new_capacity):
            self._buckets.append(LinkedList())
        
        # Iterate over old elements and hash/place in new list
        for i in range(old_buckets.length()):
            for node in old_buckets[i]:
                self.put(node.key, node.value)

    def get(self, key: str) -> object:
        """
        Returns the stored value associated with a given key. If value
        is not present, returns None. 
        """
        bucket = self._get_bucket(key)
        for node in bucket:
            if node.key == key:
                return node.value
        
        return None

    def contains_key(self, key: str) -> bool:
        """
        Returns True if given key is present in hash map, False otherwise.
        """
        bucket = self._get_bucket(key)
        for node in bucket: 
            if node.key == key:
                return True
        
        return False

    def remove(self, key: str) -> None:
        """
        Removes given key (and associated value) from hash map. If the key
        is not present in the map, does nothing. 
        """
        bucket = self._get_bucket(key)
        removed = bucket.remove(key)

        if removed:
            self._size -= 1

    def get_keys(self) -> DynamicArray:
        """
        Returns an unordered DynamicArray holding all keys currently in hash map. 
        """
        keys = DynamicArray()
        for i in range(self._capacity): 
            for node in self._buckets[i]:
                keys.append(node.key)
        
        return keys

    def _get_bucket(self, key: str) -> LinkedList:
        """
        Helper method to locate the "bucket" (LinkedList) associated with a 
        given hashed index. 
        """
        index = self._hash_function(key) % self._capacity
        bucket = self._buckets[index]
        return bucket


def find_mode(da: DynamicArray) -> (DynamicArray, int):
    """
    Takes a DynamicArray and returns the element or elements with the
    highest frequency, along with the number of times they appear. 
    """
    # Count each string's frequency and populate hashmap 
    map = HashMap(da.length() // 3, hash_function_1)
    for i in range(da.length()):
        key = da[i]
        count = map.get(key)
        if count is None: 
            map.put(key, 1)
        else:
            map.put(key, count + 1)

    mode_strings = DynamicArray()
    mode_count = 0   

    # Iterate over strings in map, checking for highest freqeuency
    map_keys = map.get_keys()
    for i in range(map_keys.length()):
        key = map_keys[i]
        value = map.get(key)
        # If higher than current highest, store as new mode 
        if value > mode_count:
            mode_strings = DynamicArray()
            mode_strings.append(key)
            mode_count = value
        # If equal, add to list of current modes 
        elif value == mode_count:
            mode_strings.append(key)

    return (mode_strings, mode_count)

# ------------------- BASIC TESTING ---------------------------------------- #

if __name__ == "__main__":

    print("\nPDF - put example 1")
    print("-------------------")
    m = HashMap(50, hash_function_1)
    for i in range(150):
        m.put('str' + str(i), i * 100)
        if i % 25 == 24:
            print(m.empty_buckets(), m.table_load(), m.get_size(), m.get_capacity())

    print("\nPDF - put example 2")
    print("-------------------")
    m = HashMap(40, hash_function_2)
    for i in range(50):
        m.put('str' + str(i // 3), i * 100)
        if i % 10 == 9:
            print(m.empty_buckets(), m.table_load(), m.get_size(), m.get_capacity())

    print("\nPDF - empty_buckets example 1")
    print("-----------------------------")
    m = HashMap(100, hash_function_1)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key1', 10)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key2', 20)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key1', 30)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key4', 40)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())

    print("\nPDF - empty_buckets example 2")
    print("-----------------------------")
    m = HashMap(50, hash_function_1)
    for i in range(150):
        m.put('key' + str(i), i * 100)
        if i % 30 == 0:
            print(m.empty_buckets(), m.get_size(), m.get_capacity())

    print("\nPDF - table_load example 1")
    print("--------------------------")
    m = HashMap(100, hash_function_1)
    print(m.table_load())
    m.put('key1', 10)
    print(m.table_load())
    m.put('key2', 20)
    print(m.table_load())
    m.put('key1', 30)
    print(m.table_load())

    print("\nPDF - table_load example 2")
    print("--------------------------")
    m = HashMap(50, hash_function_1)
    for i in range(50):
        m.put('key' + str(i), i * 100)
        if i % 10 == 0:
            print(m.table_load(), m.get_size(), m.get_capacity())

    print("\nPDF - clear example 1")
    print("---------------------")
    m = HashMap(100, hash_function_1)
    print(m.get_size(), m.get_capacity())
    m.put('key1', 10)
    m.put('key2', 20)
    m.put('key1', 30)
    print(m.get_size(), m.get_capacity())
    m.clear()
    print(m.get_size(), m.get_capacity())

    print("\nPDF - clear example 2")
    print("---------------------")
    m = HashMap(50, hash_function_1)
    print(m.get_size(), m.get_capacity())
    m.put('key1', 10)
    print(m.get_size(), m.get_capacity())
    m.put('key2', 20)
    print(m.get_size(), m.get_capacity())
    m.resize_table(100)
    print(m.get_size(), m.get_capacity())
    m.clear()
    print(m.get_size(), m.get_capacity())

    print("\nPDF - resize example 1")
    print("----------------------")
    m = HashMap(20, hash_function_1)
    m.put('key1', 10)
    print(m.get_size(), m.get_capacity(), m.get('key1'), m.contains_key('key1'))
    m.resize_table(30)
    print(m.get_size(), m.get_capacity(), m.get('key1'), m.contains_key('key1'))

    print("\nPDF - resize example 2")
    print("----------------------")
    m = HashMap(75, hash_function_2)
    keys = [i for i in range(1, 1000, 13)]
    for key in keys:
        m.put(str(key), key * 42)
    print(m.get_size(), m.get_capacity())

    for capacity in range(111, 1000, 117):
        m.resize_table(capacity)

        m.put('some key', 'some value')
        result = m.contains_key('some key')
        m.remove('some key')

        for key in keys:
            # all inserted keys must be present
            result &= m.contains_key(str(key))
            # NOT inserted keys must be absent
            result &= not m.contains_key(str(key + 1))
        print(capacity, result, m.get_size(), m.get_capacity(), round(m.table_load(), 2))

    print("\nPDF - get example 1")
    print("-------------------")
    m = HashMap(30, hash_function_1)
    print(m.get('key'))
    m.put('key1', 10)
    print(m.get('key1'))

    print("\nPDF - get example 2")
    print("-------------------")
    m = HashMap(150, hash_function_2)
    for i in range(200, 300, 7):
        m.put(str(i), i * 10)
    print(m.get_size(), m.get_capacity())
    for i in range(200, 300, 21):
        print(i, m.get(str(i)), m.get(str(i)) == i * 10)
        print(i + 1, m.get(str(i + 1)), m.get(str(i + 1)) == (i + 1) * 10)

    print("\nPDF - contains_key example 1")
    print("----------------------------")
    m = HashMap(10, hash_function_1)
    print(m.contains_key('key1'))
    m.put('key1', 10)
    m.put('key2', 20)
    m.put('key3', 30)
    print(m.contains_key('key1'))
    print(m.contains_key('key4'))
    print(m.contains_key('key2'))
    print(m.contains_key('key3'))
    m.remove('key3')
    print(m.contains_key('key3'))

    print("\nPDF - contains_key example 2")
    print("----------------------------")
    m = HashMap(75, hash_function_2)
    keys = [i for i in range(1, 1000, 20)]
    for key in keys:
        m.put(str(key), key * 42)
    print(m.get_size(), m.get_capacity())
    result = True
    for key in keys:
        # all inserted keys must be present
        result &= m.contains_key(str(key))
        # NOT inserted keys must be absent
        result &= not m.contains_key(str(key + 1))
    print(result)

    print("\nPDF - remove example 1")
    print("----------------------")
    m = HashMap(50, hash_function_1)
    print(m.get('key1'))
    m.put('key1', 10)
    print(m.get('key1'))
    m.remove('key1')
    print(m.get('key1'))
    m.remove('key4')

    print("\nPDF - get_keys example 1")
    print("------------------------")
    m = HashMap(10, hash_function_2)
    for i in range(100, 200, 10):
        m.put(str(i), str(i * 10))
    print(m.get_keys())

    m.resize_table(1)
    print(m.get_keys())

    m.put('200', '2000')
    m.remove('100')
    m.resize_table(2)
    print(m.get_keys())

    print("\nPDF - find_mode example 1")
    print("-----------------------------")
    da = DynamicArray(["apple", "apple", "grape", "melon", "melon", "peach"])
    map = HashMap(da.length() // 3, hash_function_1)
    mode, frequency = find_mode(da)
    print(f"Input: {da}\nMode: {mode}, Frequency: {frequency}")

    print("\nPDF - find_mode example 2")
    print("-----------------------------")
    test_cases = (
        ["Arch", "Manjaro", "Manjaro", "Mint", "Mint", "Mint", "Ubuntu", "Ubuntu", "Ubuntu", "Ubuntu"],
        ["one", "two", "three", "four", "five"],
        ["2", "4", "2", "6", "8", "4", "1", "3", "4", "5", "7", "3", "3", "2"]
    )

    for case in test_cases:
        da = DynamicArray(case)
        map = HashMap(da.length() // 3, hash_function_2)
        mode, frequency = find_mode(da)
        print(f"Input: {da}\nMode: {mode}, Frequency: {frequency}\n")
