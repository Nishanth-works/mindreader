import json
import csv
from PIL import Image
import mmap
import functools
from typing import Union, Iterator, List, Dict, Any
from enum import Enum
from cachetools import LRUCache
from cachetools.keys import hashkey
from datetime import datetime, timedelta

class FileType(Enum):
    JSON = 'json'
    IMAGE = 'image'
    CSV = 'csv'
    TEXT = 'text'


class CacheType(Enum):
    LRU = 'lru'
    WRITE_THROUGH = 'write_through'


class Cache:
    def __init__(self, cache_type: CacheType, capacity: int = 100, ttl: int = 60):
        if cache_type == CacheType.LRU:
            self.cache = LRUCache(maxsize=capacity)
        elif cache_type == CacheType.WRITE_THROUGH:
            self.cache = {}
        else:
            raise ValueError(f"Unsupported cache type '{cache_type}'")
        self.ttl = timedelta(seconds=ttl)

    def __call__(self, func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            key = hashkey(*args, **kwargs)
            if key in self.cache:
                value, timestamp = self.cache[key]
                if datetime.now() - timestamp < self.ttl:
                    return value
            value = func(*args, **kwargs)
            self.cache[key] = (value, datetime.now())
            return value

        return wrapper


def mmap_generator(file_obj):
    with mmap.mmap(file_obj.fileno(), length=0, access=mmap.ACCESS_READ) as mmapped_file:
        yield from mmapped_file


@Cache(cache_type=CacheType.LRU, capacity=1000)
def read_json_lru(file_path: str) -> Iterator[Dict[str, Any]]:
    with open(file_path, 'r') as file_obj:
        data = json.load(mmap_generator(file_obj))
        for item in data:
            yield item


@Cache(cache_type=CacheType.WRITE_THROUGH)
def read_json_write_through(file_path: str) -> Iterator[Dict[str, Any]]:
    with open(file_path, 'r') as file_obj:
        data = json.load(mmap_generator(file_obj))
        for item in data:
            yield item


@Cache(cache_type=CacheType.LRU, capacity=1000)
def read_image_lru(file_path: str) -> Image.Image:
    return Image.open(file_path)


@Cache(cache_type=CacheType.WRITE_THROUGH)
def read_image_write_through(file_path: str) -> Image.Image:
    return Image.open(file_path)


@Cache(cache_type=CacheType.LRU, capacity=1000)
def read_csv_lru(file_path: str) -> Iterator[Dict[str, Union[str, int, float]]]:
    with open(file_path, 'r') as file_obj:
        csv_reader = csv.DictReader(mmap_generator(file_obj))
        for row in csv_reader:
            yield row


@Cache(cache_type=CacheType.WRITE_THROUGH)
def read_csv_write_through(file_path: str) -> Iterator[Dict[str, Union[str, int, float]]]:
    with open(file_path, 'r') as file_obj:
        csv_reader = csv.DictReader(mmap_generator(file_obj))
        for row in csv_reader:
            yield row


@Cache(cache_type=CacheType.LRU, capacity=1000)
def read_text_lru(file_path: str) -> Iterator[str]:
    with open(file_path, 'r') as file_obj:
        for line in mmap_generator(file_obj):
            yield line.decode()

@Cache(cache_type=CacheType.WRITE_THROUGH)
def read_text_write_through(file_path: str) -> Iterator[str]:
    with open(file_path, 'r') as file_obj:
        for line in mmap_generator(file_obj):
            yield line.decode()


def read_file(file_path: str, file_type: FileType, cache_type: CacheType) -> Union[Iterator[Dict[str, Any]], Image.Image, Iterator[Dict[str, Union[str, int, float]]], Iterator[str]]:
    file_readers = {
        FileType.JSON: read_json_lru if cache_type == CacheType.LRU else read_json_write_through,
        FileType.IMAGE: read_image_lru if cache_type == CacheType.LRU else read_image_write_through,
        FileType.CSV: read_csv_lru if cache_type == CacheType.LRU else read_csv_write_through,
        FileType.TEXT: read_text_lru if cache_type == CacheType.LRU else read_text_write_through
    }

    if file_type not in file_readers:
        raise ValueError(f"Unsupported file type '{file_type}'")

    return file_readers[file_type](file_path)


def process_file(file_path: str, file_type: str, cache_type: str):
    file_type_enum = FileType(file_type)
    cache_type_enum = CacheType(cache_type)
    data_iterator = read_file(file_path, file_type_enum, cache_type_enum)
    return data_iterator


if __name__ == '__main__':
    file_path = 'path/to/your/file.ext'
    file_type = 'json'  # Change this to 'image', 'csv', or 'text' to read other types of files
    cache_type = 'lru'  # Change this to 'write_through' to use the write-through cache instead

    data_iterator = process_file(file_path, file_type, cache_type)
    # Use the data_iterator as needed in your application