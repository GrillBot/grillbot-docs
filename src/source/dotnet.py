from datetime import datetime, timedelta
from .cache import cache
from xml.etree import ElementTree
import requests

import os


class DotnetDependencyList:
    def __init__(self) -> None:
        self.csproj_files = [
            "https://raw.githubusercontent.com/GrillBot/grillbot/master/src/GrillBot.App/GrillBot.App.csproj",
            "https://raw.githubusercontent.com/GrillBot/grillbot/master/src/GrillBot.Cache/GrillBot.Cache.csproj",
            "https://raw.githubusercontent.com/GrillBot/grillbot/master/src/GrillBot.Common/GrillBot.Common.csproj",
            "https://raw.githubusercontent.com/GrillBot/grillbot/master/src/GrillBot.Data/GrillBot.Data.csproj",
            "https://raw.githubusercontent.com/GrillBot/grillbot/master/src/GrillBot.Database/GrillBot.Database.csproj",
            "https://raw.githubusercontent.com/GrillBot/grillbot/master/src/GrillBot.Tests/GrillBot.Tests.csproj",
        ]
        self.cache = cache
        self.cache_key = "dotnet_dependency_list"

    def get_data(self) -> dict:
        cached_data: dict = self.cache.get(self.cache_key)
        if cached_data is not None:
            return cached_data
        result = dict()

        for project in self.csproj_files:
            project_name = os.path.basename(project).replace(".csproj", "")
            packages = self.download_dependencies(project, project_name)
            result[project_name] = {
                "link": project.replace("raw", "blob", 1),
                "packages": list(),
            }
            for package in packages:
                version = packages[package]
                result[project_name]["packages"].append(
                    {
                        "name": package,
                        "version": version,
                        "url": f"https://nuget.org/packages/{package}/{version}",
                    }
                )

        self.cache.add(self.cache_key, result, datetime.now() + timedelta(days=1))
        return result

    def download_dependencies(self, url: str, project_name: str) -> dict:
        response = requests.get(url)
        if not response.ok:
            raise RuntimeError(f"Cannot find project {project_name}")
        xml = ElementTree.fromstring(response.text)
        result = dict()
        for elem in xml.iter():
            if elem.tag != "PackageReference":
                continue
            package = elem.attrib["Include"]
            version = elem.attrib["Version"]
            result[package] = version

        return result
