import requests
import json
from .cache import cache
from typing import List
import re


class NodeDependencyList:
    def __init__(self, package: str) -> None:
        self.package = package
        self.cache = cache
        self.cache_key = f"node_{package}_dependency_list"

    def get_data(self) -> dict:
        return self.cache.get_or_load(self.cache_key, self._load)

    def _load(self) -> dict:
        data = self.download_dependencies()

        return {
            "development": self.process_dependencies(data["devDependencies"]),
            "production": self.process_dependencies(data["dependencies"]),
        }

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
        response = requests.get(self.package, timeout=10)
        if not response.ok:
            raise RuntimeError(
                f"Unable to find package.json file from url {self.package}"
            )
        return json.loads(response.text)
