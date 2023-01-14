from typing import Dict, Union, Any
from datetime import datetime


class CacheItem:
    def __init__(self, data, valid_to: datetime) -> None:
        self.data = data
        self.valid_to = valid_to

    def is_valid(self) -> bool:
        return self.data is not None and self.valid_to >= datetime.now()


class Cache:
    data: Dict[str, CacheItem] = dict()

    def add(self, key: str, data, valid_to: datetime) -> None:
        self.data[key] = CacheItem(data, valid_to)

    def delete(self, key: str) -> None:
        if key not in self.data:
            return
        del self.data[key]

    def get(self, key: str) -> Union[Any, None]:
        if key not in self.data or not self.data[key].is_valid():
            return None
        return self.data[key].data

cache = Cache()
