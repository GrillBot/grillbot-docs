import os
import requests
from xml.etree import ElementTree
import logging


class DotnetDependencyList:
    @staticmethod
    def get_data(csproj: str) -> list:
        result = list()

        project_name = os.path.basename(csproj).replace(".csproj", "")
        logging.info(f"Loading .NET dependencies for {project_name}")

        packages = DotnetDependencyList.download_dependencies(csproj, project_name)
        for package in packages:
            version = packages[package]
            result.append(
                {
                    "name": package,
                    "version": version,
                    "url": f"https://nuget.org/packages/{package}/{version}",
                }
            )

        return result

    @staticmethod
    def download_dependencies(url: str, project_name: str) -> dict:
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
