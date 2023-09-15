# CS 261 - Hashmap Implementation

This is a from-scratch Python implementation of a hashmap, including both "open addressing" and "separate chaining" options for resolving hash value collisions. By hashing input values and storing the value at the resulting table index, data can be stored and retrieved in amortized O(1) time. 

This was a project for Oregon State's **CS 261 - Data Structures**. 

## Installation

Download and run either `hash_map_oa.py` (for open addressing) or `hash_map_sc.py` (for separate chaining). 

## Usage

A new hash table can be initialized via the HashMap class: 
`my_map = HashMap(capacity, hash_function)`

Once initialized, it can be used to: 
* insert a key-value pair: `my_map.put(key, value)`
* retrieve a key's value: `value = my_map.get(key)`
* check if a key exists: `exists = my_map.contains_key(key)`
* remove a key-value pair: `my_map.remove(key)`
* obtain all keys currently stored: `keys = my_map.get_keys()`
* obtain the table's current size (number of elements): `size = my_map.get_size()`
* obtain the current capacity (number of slots): `capacity = my_map.get_capacity()`
* check the load factor of the table: `load_factor = my_map.table_load()`
* clear the contents of the table: `my_map.clear()`
