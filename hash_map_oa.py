# Name: Will Lambeth
# OSU Email: lambethw@oregonstate.edu
# Course: CS261 - Data Structures
# Assignment: 06 part 2 - Hash map with open addressing
# Due Date: 03 June 2022    
# Description: An implementation of a hash map using open addressing to resolve collisions. 


from asyncio import proactor_events
from a6_include import (DynamicArray, HashEntry,
                        hash_function_1, hash_function_2)


class HashMap:
    def __init__(self, capacity: int, function) -> None:
        """
        Initialize new HashMap that uses
        quadratic probing for collision resolution
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self._buckets = DynamicArray()
        for _ in range(capacity):
            self._buckets.append(None)

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
        Takes a key-value pair and stores it in the hash table. 
        """
        # Check load factor and resize if needed
        load_factor = self.table_load()
        if load_factor >= 0.5:
            self.resize_table(self._capacity * 2)

        # Retrieve index of matching element, or first open index
        index = self._get_index(key, False)
        element = self._buckets[index]
        # If index is open, insert key/value pair there
        if element == None or element.is_tombstone:
            self._buckets[index] = HashEntry(key, value)
            self._size += 1
        # Otherwise, update element's value to provided value
        else:
            element.value = value

    def table_load(self) -> float:
        """
        Returns the load factor of the current hash table. 
        """
        empties = self.empty_buckets()
        return (self._capacity - empties) / self._capacity


    def empty_buckets(self) -> int:
        """
        Returns the number of empty buckets in the current hash table.
        """
        return (self._capacity - self._size)

    def resize_table(self, new_capacity: int) -> None:
        """
        Takes an integer and resizes the hash table's capacity to that number.
        """
        # Validate new capacity and return if not valid
        if new_capacity < 1 or new_capacity < self._size:
            return 

        old_table = self._buckets
        # Fill new array with requested number of buckets
        self._buckets = DynamicArray()
        for _ in range(new_capacity):
            self._buckets.append(None)
        self._capacity = new_capacity
        self._size = 0

        # Rehash and populate new array with old values
        for i in range(old_table.length()):
            entry = old_table[i]
            if entry != None and entry.is_tombstone == False:
                self.put(entry.key, entry.value)

    def get(self, key: str) -> object:
        """
        Takes a string and returns the value stored with that string as key, 
        or None if key does not exist. 
        """
        index = self._get_index(key)
        element = self._buckets[index]
        if element != None: 
            return element.value
        else:
            return None     

    def contains_key(self, key: str) -> bool:
        """
        Takes a string and returns a boolean denoting whether that string
        is a valid key in the current hash table.
        """
        index = self._get_index(key)
        return self._buckets[index] != None 

    def remove(self, key: str) -> None:
        """
        Takes a key and removes the element with that key from the 
        hash table. If key is not found, does nothing. 
        """
        index = self._get_index(key)
        element = self._buckets[index]

        if element != None: 
            element.is_tombstone = True
            self._size -= 1

    def clear(self) -> None:
        """
        Removes all stored elements from the hash table, while retaining
        its current capacity. 
        """
        self._size = 0
        self._buckets = DynamicArray()

        for _ in range(self._capacity):
            self._buckets.append(None)

    def get_keys(self) -> DynamicArray:
        """
        Returns a DynamicArray containing all valid keys for 
        objects stored in hash table. 
        """
        keys = DynamicArray()
        for i in range(self._capacity):
            element = self._buckets[i]
            if element != None and element.is_tombstone == False: 
                keys.append(element.key)
        
        return keys

    def _get_index(self, key: str, skip_tombstones: bool=True) -> int:
        """
        Helper method that takes a key and an optional parameter to accept/ignore 
        tombstone values. Returns the index of the given key in the hashmap, 
        or of the first open index if key is not found. 
        """
        initial_index = self._hash_function(key) % self._capacity

        # Find first hashed index and set up for probing
        probe_iterator = 0 
        index = initial_index
        item = self._buckets[index]

        # Loop until empty element is found
        while item is not None: 
            # Return if item is found (and isn't a tombstone)
            if item.key == key and item.is_tombstone == False:
                return index
            # Also return on tombstones if operation requires (i.e. put())
            elif item.key == key and skip_tombstones == False: 
                return index 

            # If not a match or an empty index, increment probe and continue
            probe_iterator += 1
            index = (initial_index + (probe_iterator ** 2)) % self._capacity
            item = self._buckets[index]

        # If key not found, return index of first open spot
        return index

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

        if m.table_load() >= 0.5:
            print("Check that capacity gets updated during resize(); "
                  "don't wait until the next put()")

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
