from typing import Union
from src.api import build_api_description
import pathlib
from src.dotnet_deps import DotnetDependencyList
from src.source.node import NodeDependencyList

names = {
    "grillbot": "GrillBot",
    "graphics": "Graphics",
    "rubbergod": "RubbergodService",
    "file": "FileService",
    "points": "Points",
}

descriptions = {
    "grillbot": "Nejdůležitější služba. Jedná se o centrální bod celého systému. Všechna funkcionalita, která není "
    + "obsažena ve službách je zde. Také zajišťuje správu dat v databázi a konektivitu s Discord.",
    "graphics": "Vykreslovací služba. Stará se o vše co nějak souvisí s grafikou (grafy, obrázek bodů, ...)",
    "rubbergod": "Služba starající se o rozhraní mezi boty GrillBot a Rubbergod.",
    "file": "Služba řešící ukládání a získávání souborů mezi GrillBot a Azure Storage Blob.",
    "points": "Služba řesící správu bodů (transakcí, slučování, reporting, ...)",
}

databases = {
    "grillbot": {"Databáze": "/static/database.svg", "Cache": "/static/cache.svg"},
    "graphics": None,
    "rubbergod": {
        "Databáze": "/static/rubbergod_db.svg",
    },
    "file": None,
    "points": {"Databáze": "/static/database_points.svg"},
}

di_graphs = {
    "grillbot": "/static/di-graph.svg",
    "graphics": None,
    "rubbergod": "/static/di-graph-rubbergod.svg",
    "file": "/static/di-graph-file.svg",
    "points": "/static/di-graph-points.svg",
}

api_descriptions = {
    "grillbot": None,
    "graphics": [
        build_api_description(
            "POST /chart",
            [200, 400, 500],
            ["image/png", "application/json"],
            "Vygenerování grafu. <b>Jediný podporovaný je spojnicový graf.</b>",
        ),
        build_api_description(
            "POST /image/without-accident",
            [200, 400, 500],
            ["image/png", "application/json"],
            "Vykreslení obrázku znělky ze seriálu The Simpsons s počtem dní od posledního incidentu.",
        ),
        build_api_description(
            "POST /image/points",
            [200, 400, 500],
            ["image/png", "application/json"],
            "Vykreslení obrázku s aktuálním stavem bodů uživatele.",
        ),
        build_api_description(
            "POST /image/peepo/angry",
            [200, 400, 500],
            ["application/json"],
            "Vykreslení obrázku naštvaně zírajícího peepo. Podporuje animované profilové "
            + "obrázky.<br>Vrací pole jednotlivých frames, které si volající musí sám poskládat.",
        ),
        build_api_description(
            "POST /image/peepo/love",
            [200, 400, 500],
            ["application/json"],
            "Vykreslení obrázku peepo držícího uživatele. Podporuje animované profilové "
            + "obrázky.<br>Vrací pole jednotlivých frames, které si volající musí sám posklídat.",
        ),
        build_api_description(
            "GET /health", [200], ["application/json"], "Kontrola životnosti služby."
        ),
        build_api_description(
            "GET /info", [200], ["application/json"], "Informace o běžící službě."
        ),
        build_api_description(
            "GET /metrics", [200], ["application/json"], "Stav procesu služby."
        ),
        build_api_description(
            "GET /stats",
            [200],
            ["application/json"],
            "Statistiky služby (počty požadavků, statistiky per endpoint, ...)",
        ),
    ],
    "rubbergod": [
        build_api_description(
            "GET /api/diag",
            [200],
            ["application/json"],
            "Vrací diagnostické informace o stavu služby (počty, využití paměti, statistiky, ...)",
        ),
        build_api_description(
            "GET /api/directapi/{service}",
            [200, 400],
            ["application/json", "text/plain"],
            "Odešle request na externí službu podporující DirectApi (RubberGod) a vrátí odpověď.",
        ),
        build_api_description(
            "POST /api/karma",
            [200, 400],
            ["application/json"],
            "Založí nový nebo upraví existující záznam o karmě uživatele.",
        ),
        build_api_description(
            "GET /api/karma",
            [200, 400],
            ["application/json"],
            "Vrací stránkovaný seznam karmy jednotlivých uživatelů.",
        ),
        build_api_description(
            "PATCH /api/user/{memberId}",
            [200],
            [],
            "Založí nový požadavek na synchronizaci uživatele v interní databázi.",
        ),
    ],
    "file": [
        build_api_description(
            "POST /api/data",
            [200, 409],
            ["application/json"],
            "Nahrání nového souboru. Pokud již soubor pod stejným jménem existuje, tak se vrací Conflcit.",
        ),
        build_api_description(
            "GET /api/data",
            [200, 404],
            ["*/*"],
            "Stažení obsahu souboru. Pokud neexistuje, tak se vrací Not Found",
        ),
        build_api_description(
            "DELETE /api/data", [200], [], "Fyzické smazání souboru."
        ),
        build_api_description(
            "GET /api/data/link",
            [200],
            ["text/plain"],
            "Vytvoření unikátního odkazu přímo na soubor.",
        ),
        build_api_description(
            "GET /api/diag",
            [200],
            ["application/json"],
            "Vrací diagnostické informace o stavu služby (počty, využití paměti, statistiky, ...)",
        ),
    ],
    "points": [
        build_api_description(
            "POST /api/admin/list",
            [200, 400],
            ["application/json"],
            "Seznam transakcí.",
        ),
        build_api_description(
            "POST /api/admin/create",
            [200, 400, 406],
            ["application/json"],
            "Servisní vytvoření transakce.",
        ),
        build_api_description(
            "GET /api/diag",
            [200],
            ["application/json"],
            "Vrací diagnostické informace o stavu služby (počty, využití paměti, statistiky, ...).",
        ),
        build_api_description(
            "POST /api/chart",
            [200, 400],
            ["application/json"],
            "Načtení statistik za jednotlivé dny pro graf.",
        ),
        build_api_description(
            "GET /api/leaderboard/{guildId}",
            [200, 400],
            ["application/json"],
            "TOP N statistika bodů.",
        ),
        build_api_description(
            "GET /api/leaderboard/{guildId}/count",
            [200, 400],
            ["application/json"],
            "Celkový počet dostupných záznamů v leaderboardu.",
        ),
        build_api_description(
            "POST /api/merge",
            [200, 204],
            ["application/json"],
            "Sloučení expirovaných transakcí.",
        ),
        build_api_description(
            "GET /api/status/{guildId}/{userId}",
            [200],
            ["application/json"],
            "Stav platných bodů uživatele",
        ),
        build_api_description(
            "GET /api/status/{guildId}/{userId}/image",
            [200],
            ["application/json"],
            "Stav platných bodů uživatele pro vykreslení obrázku.",
        ),
        build_api_description(
            "GET /api/status/{guildId}/{userId}/expired",
            [200],
            ["application/json"],
            "Stav expirovaných bodů uživatele",
        ),
        build_api_description(
            "POST /api/synchronization",
            [200, 400],
            ["application/json"],
            "Synchronizace provozních dat pro správné vytváření transakcí (uživatelé a kanály).",
        ),
        build_api_description(
            "POST /api/transaction",
            [200, 400, 406],
            ["application/json"],
            "Vytvoření transakce.",
        ),
        build_api_description(
            "DELETE /api/transaction/{guildId}/{messageId}",
            [200, 204],
            ["application/json"],
            "Smazání transakce zprávy a všech transakcí vzniklých z reakcí.",
        ),
        build_api_description(
            "DELETE /api/transaction/{guildId}/{messageId}/{reactionId}",
            [200, 204],
            ["application/json"],
            "Smazání transakce vycházející z reakce.",
        ),
        build_api_description(
            "POST /api/transaction/transfer",
            [200, 400],
            ["application/json"],
            "Převod bodů mezi uživateli.",
        ),
        build_api_description(
            "GET /api/transaction/{guildId}/{userId}",
            [200],
            ["text/plain"],
            "Indikace, zda pro daného uživatele existuje nějaká transakce.",
        ),
    ],
}

project_files = {
    "grillbot": [
        "https://raw.githubusercontent.com/GrillBot/grillbot/master/src/GrillBot.App/GrillBot.App.csproj",
        "https://raw.githubusercontent.com/GrillBot/grillbot/master/src/GrillBot.Cache/GrillBot.Cache.csproj",
        "https://raw.githubusercontent.com/GrillBot/grillbot/master/src/GrillBot.Common/GrillBot.Common.csproj",
        "https://raw.githubusercontent.com/GrillBot/grillbot/master/src/GrillBot.Data/GrillBot.Data.csproj",
        "https://raw.githubusercontent.com/GrillBot/grillbot/master/src/GrillBot.Database/GrillBot.Database.csproj",
    ],
    "graphics": "https://raw.githubusercontent.com/GrillBot/GrillBot.Services/master/src/Graphics/package.json",
    "rubbergod": "https://raw.githubusercontent.com/GrillBot/GrillBot.Services/master/src/RubbergodService/RubbergodService/RubbergodService.csproj",  # noqa: E501
    "file": "https://raw.githubusercontent.com/GrillBot/GrillBot.Services/master/src/FileService/FileService/FileService.csproj",  # noqa: E501
    "points": "https://raw.githubusercontent.com/GrillBot/GrillBot.Services/master/src/PointsService/PointsService.csproj",  # noqa: E501
}


class ServiceProvider:
    def __init__(self, service_name: str) -> None:
        self.service_name = service_name

    def get_data(self) -> Union[dict, None]:
        if self.service_name not in names:
            return None

        result = {
            "name": names[self.service_name],
            "description": descriptions[self.service_name],
            "is_public": self.service_name == "grillbot",
        }

        database = databases[self.service_name]
        if database is not None:
            result["database"] = database

        di_graph = di_graphs[self.service_name]
        if di_graph is not None:
            result["di_graph"] = di_graph

        api_description = api_descriptions[self.service_name]
        if api_description is not None:
            result["api_description"] = api_description

        if self.service_name == "grillbot":
            result["swagger_url"] = "https://grillbot.cloud/swagger"

        project_file = project_files[self.service_name]
        if project_file is not None:
            deps = self.download_deps(project_file)
            if deps is not None:
                result["dependencies"] = deps

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
            for dep in filter(lambda x: x["name"] == "GrillBot.Core", result):
                dep[
                    "url"
                ] = "https://github.com/GrillBot/GrillBot.Core/pkgs/nuget/GrillBot.Core"
            return result
        elif extension == ".json":
            result = NodeDependencyList(project).get_data()
            return result["production"] + result["development"]
        return None
