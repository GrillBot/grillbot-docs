import os
import requests
from datetime import datetime, timedelta
from xml.etree import ElementTree


class DataSource:
    def get_data(self) -> dict:
        raise NotImplementedError()


class DependencyDataSource(DataSource):
    def __init__(self) -> None:
        self.csproj_files = [
            "https://gitlab.com/grillbot/grillbot/-/raw/master/src/GrillBot/GrillBot.App/GrillBot.App.csproj",
            "https://gitlab.com/grillbot/grillbot/-/raw/master/src/GrillBot/GrillBot.Data/GrillBot.Data.csproj",
            "https://gitlab.com/grillbot/grillbot/-/raw/master/src/GrillBot/GrillBot.Database/GrillBot.Database.csproj",
            "https://gitlab.com/grillbot/grillbot/-/raw/master/src/GrillBot/GrillBot.Cache/GrillBot.Cache.csproj",
            "https://gitlab.com/grillbot/grillbot/-/raw/master/src/GrillBot/GrillBot.Common/GrillBot.Common.csproj",
            "https://gitlab.com/grillbot/grillbot/-/raw/master/src/GrillBot/GrillBot.Tests/GrillBot.Tests.csproj",
        ]
        self.cached_data = None
        self.cache_valid_to = datetime.min

    def get_data(self) -> dict:
        if self.is_cache_valid():
            return self.cached_data
        result = dict()

        for project in self.csproj_files:
            project_name = os.path.basename(project).replace(".csproj", "")
            packages = self.download_dependencies(project, project_name)
            result[project_name] = {"link": project.replace('raw', 'blob', 1), "packages": list()}
            for package in packages:
                version = packages[package]
                result[project_name]["packages"].append(
                    {
                        "name": package,
                        "version": version,
                        "url": f"https://nuget.org/packages/{package}/{version}",
                    }
                )

        return self.process_cache({"dependencies": result})

    def is_cache_valid(self) -> bool:
        return self.cached_data is not None and self.cache_valid_to >= datetime.now()

    def process_cache(self, data: dict) -> dict:
        self.cached_data = data
        self.cache_valid_to = datetime.now() + timedelta(days=1)
        return data

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


page_to_data_source = {"dependency": DependencyDataSource()}
