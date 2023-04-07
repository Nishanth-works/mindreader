
# 🧠 Mind Reader 
#####  💾 Memory-Efficient File Reader Script with 🔍 Caching Mechanism, generators and mmap

- M.: Memory-mapped file I/O for efficient file reading
- I. : Iterator-based processing for seamless file handling
- N.: Native support for JSON, CSV, Image, and Text file formats
- D.: Dynamic caching for improved file access times

### Overview

This script provides a collection of file reader functions for reading JSON, CSV, image, and text files efficiently. The script includes a caching mechanism that stores frequently accessed data in memory to reduce disk reads and improve performance.

The caching mechanism can be configured to use either the Least Recently Used (LRU) Cache or the Write-Through Cache, providing flexibility and tuning capabilities. With its efficient file reading techniques, this script minimizes the amount of disk access required to read files, improving performance and reducing resource usage.

Whether you're a developer, data scientist, or data analyst, this file reader script is a useful tool for efficient and effective file reading.



### Installation

To install the dependencies for this script, you can use pip to install the packages specified in the requirements.txt file:

`pip install -r requirements.txt`

### Usage

To use this script, you can import the process_file function from the script and call it with the path to the file you want to read, the type of file you want to read (json, image, csv, or text), and the type of cache you want to use `(lru or write_through)`:


```from file_reader import process_file

file_path = 'path/to/your/file.ext'
file_type = 'json'  # Change this to 'image', 'csv', or 'text' to read other types of files
cache_type = 'lru'  # Change this to 'write_through' to use the write-through cache instead

data_iterator = process_file(file_path, file_type, cache_type)
# Use the data_iterator as needed in your application
```


You can also use this script to define your own file reader functions by creating a new function that calls the `Cache decorator` and defining the file reading logic within the function. For example:

```
from file_reader import Cache, CacheType, mmap_generator

@Cache(cache_type=CacheType.LRU, capacity=1000)
def read_my_file_lru(file_path: str) -> str:
    with open(file_path, 'r') as file_obj:
        for line in mmap_generator(file_obj):
            yield line.decode()
            
```
This will create a new file reader function that uses the LRU cache to store the contents of the file.



## Features


### Efficient File Reading

This script uses efficient file reading techniques to minimize the amount of disk access required to read files. For example, the script uses memory-mapped I/O to efficiently read large files. Memory-mapped I/O is a technique that maps a file to a portion of memory, allowing it to be accessed as if it were part of the application's memory. This allows the application to read the file much more efficiently, as it avoids the overhead of multiple disk reads.

The script also uses the csv.DictReader function to read CSV files with less overhead than traditional CSV parsing techniques. The csv.DictReader function reads a CSV file as a dictionary, allowing it to be accessed using key-value pairs instead of positional indexing. This makes it easier to work with CSV data and reduces the overhead of parsing the CSV file.

### Caching

The caching mechanism used in this script allows frequently accessed data to be stored in memory for faster access. The LRU Cache and Write-Through Cache are two types of caching mechanisms used in the script.

The LRU Cache stores frequently accessed data in memory and discards the least recently used items when the cache reaches its capacity limit. This ensures that the most frequently accessed data is always available in memory, reducing the number of disk reads required to access the data.

The Write-Through Cache ensures that the cache is always up-to-date with the underlying storage system by updating both simultaneously. This ensures that the cache is always in sync with the storage system, reducing the chances of data inconsistencies and improving performance by reducing the number of disk reads required to access the data.

### Configurability

The caching mechanism used in this script is highly configurable and can be easily customized to suit your needs. You can choose between the LRU Cache and the Write-Through Cache depending on your caching requirements, and you can also modify the cache size and time-to-live settings to optimize performance and resource usage.

By adjusting these settings, you can optimize performance for your specific use case and reduce the number of disk reads required to access frequently accessed data. This improves performance and reduces resource usage, making this script an ideal choice for applications that require efficient file reading.


### Generators

In the script, generators are used to read files in a memory-efficient manner. Instead of reading the entire file into memory at once, the script uses generators to read the file one line or one item at a time, allowing it to process the file without exceeding the memory limits of the system.

### Yield

In the script, the yield keyword is used in the generator functions to return data one item at a time. By using yield, the script is able to read and process large files efficiently, without storing the entire file in memory at once. Instead, the script reads the file one item at a time and returns each item using yield, allowing the calling code to consume the data as it is produced.
