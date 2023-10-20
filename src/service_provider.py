from typing import Union
from src.api import build_api_description, create_grillbot_swagger_spec
import pathlib
from src.dotnet_deps import DotnetDependencyList
from src.source.node import NodeDependencyList
import requests
import logging
import json

cached_services: Union[dict, None] = None


class ServiceProvider:
    def __init__(self, service_name: str) -> None:
        global cached_services
        self.service_name = service_name
        if cached_services is None:
            cached_services = self.read_services_from_json()

    def read_services_from_json(self) -> dict:
        logging.info("Loading services.json into cache.")
        with open("/static/services.json") as stream:
            return json.load(stream)

    def get_data(self) -> Union[dict, None]:
        if self.service_name not in cached_services:
            return None
        service = cached_services[self.service_name]

        result = {
            "name": service["name"],
            "description": service["description"],
            "is_public": self.service_name == "grillbot",
        }

        if "databases" in service and service["databases"] is not None:
            result["database"] = service["databases"]

        if "di_graph" in service and service["di_graph"] is not None:
            result["di_graph"] = service["di_graph"]

        if "api" in service and service["api"] is not None:
            result["api_description"] = []
            for endpoint in service["api"]:
                description = endpoint["description"]
                if (
                    "api_spec_version" in endpoint
                    and endpoint["api_spec_version"] is not None
                    and "api_spec" in endpoint
                    and endpoint["api_spec"] is not None
                ):
                    description += "<br>" + create_grillbot_swagger_spec(
                        endpoint["api_spec"], endpoint["api_spec_version"]
                    )
                result["api_description"].append(
                    build_api_description(
                        endpoint["endpoint"],
                        endpoint["status_codes"],
                        endpoint["content_types"],
                        description,
                    )
                )
            if "api_note" in service and service["api_note"] is not None:
                result["api_description_note"] = service["api_note"]

        if "swagger_url" in service and service["swagger_url"] is not None:
            result["swagger_url"] = service["swagger_url"]

        if "project_files" in service and service["project_files"] is not None:
            deps = self.download_deps(service["project_files"])
            if deps is not None:
                result["dependencies"] = deps

        if "healthcheck" in service and service["healthcheck"] is not None:
            logging.info(f"Checking online status of {self.service_name}")
            result["is_online"] = (
                requests.head(service["healthcheck"]).status_code == 200
            )

        return result

    def download_deps(self, project: Union[list, str, None]) -> Union[list, None]:
        if project is None:
            return None

        if isinstance(project, list):
            deps_list = dict()

            for proj in project:
                deps = self._deps_download(proj)
                if deps is None:
                    continue
                for dep in deps:
                    if not dep["name"] in deps_list:
                        deps_list[dep["name"]] = dep
            return list(deps_list.values())
        else:
            return self._deps_download(project)

    def _deps_download(self, project: str) -> Union[list, None]:
        extension = pathlib.Path(project).suffix
        if extension == ".csproj":
            result = DotnetDependencyList.get_data(project)
            for dep in filter(lambda x: x["name"] == "GrillBot.Core" or x["name"] == "GrillBot.Core.Services", result):
                dep[
                    "url"
                ] = "https://github.com/GrillBot/GrillBot.Core/pkgs/nuget/GrillBot.Core"
            return result
        elif extension == ".json":
            result = NodeDependencyList(project).get_data()
            return result["production"] + result["development"]
        return None
