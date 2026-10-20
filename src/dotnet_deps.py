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
        central_versions = None
        result = dict()
        for elem in xml.iter():
            if elem.tag != "PackageReference":
                continue
            package = elem.attrib["Include"]
            version = DotnetDependencyList._read_version(elem)

            # Central Package Management: the version is declared in Directory.Packages.props, not in the project.
            if version is None:
                if central_versions is None:
                    central_versions = DotnetDependencyList.download_central_versions(url)
                version = central_versions.get(package, "")

            result[package] = version

        return result

    @staticmethod
    def download_central_versions(project_url: str) -> dict:
        """Find the nearest Directory.Packages.props above the project, as MSBuild does, and read its versions."""
        directory = project_url.rsplit("/", 1)[0]
        while directory.count("/") > 2:
            directory = directory.rsplit("/", 1)[0]
            response = requests.get(f"{directory}/Directory.Packages.props")
            if not response.ok:
                continue

            xml = ElementTree.fromstring(response.text)
            return {
                elem.attrib["Include"]: elem.attrib.get("Version", "")
                for elem in xml.iter()
                if elem.tag == "PackageVersion" and "Include" in elem.attrib
            }

        logging.warning(f"Cannot find Directory.Packages.props for {project_url}")
        return dict()

    @staticmethod
    def _read_version(elem: ElementTree.Element) -> str | None:
        version = elem.attrib.get("VersionOverride") or elem.attrib.get("Version")
        if version is None:
            child = elem.find("Version")
            version = child.text if child is not None else None
        return version
