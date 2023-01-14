import requests
import json
from datetime import datetime, timedelta
from .cache import cache
from typing import List
import re


class NodeDependencyList:
    def __init__(self, package: str) -> None:
        self.package = package
        self.cache = cache
        self.cache_key = f"node_{package}_dependency_list"

    def get_data(self) -> dict:
        cached_data: dict = self.cache.get(self.cache_key)
        if cached_data is not None:
            return cached_data
        data = self.download_dependencies()

        result = {
            "development": self.process_dependencies(data["devDependencies"]),
            "production": self.process_dependencies(data["dependencies"]),
        }

        self.cache.add(self.cache_key, result, datetime.now() + timedelta(days=1))
        return result

    def process_dependencies(self, data: dict) -> List[dict]:
        result = list()
        for package_name in data:
            version = re.sub(r'r">|=|<|~|\^', "", data[package_name])
            result.append(
                {
                    "name": package_name,
                    "version": version,
                    "url": f"https://npmjs.com/package/{package_name}/v/{version}",
                }
            )
        return result

    def download_dependencies(self) -> dict:
        response = requests.get(self.package)
        if not response.ok:
            raise RuntimeError(
                f"Unable to find package.json file from url {self.package}"
            )
        return json.loads(response.text)
