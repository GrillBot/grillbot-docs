from typing import Union
from src.api import build_api_description
import pathlib
from src.dotnet_deps import DotnetDependencyList
from src.source.node import NodeDependencyList
import requests
import logging

names = {
    "grillbot": "GrillBot",
    "graphics": "Graphics",
    "rubbergod": "RubbergodService",
    "file": "FileService",
    "points": "Points",
    "image-processing": "ImageProcessingService",
    "audit-log": "AuditLogService",
}

descriptions = {
    "grillbot": "Nejdůležitější služba. Jedná se o centrální bod celého systému. Všechna funkcionalita, která není "
    + "obsažena ve službách je zde. Také zajišťuje správu dat v databázi a konektivitu s Discord.",
    "graphics": "Vykreslovací služba. Stará se o vše co nějak souvisí s grafikou (grafy, obrázek bodů, ...)",
    "rubbergod": "Služba starající se o rozhraní mezi boty GrillBot a Rubbergod.",
    "file": "Služba řešící ukládání a získávání souborů mezi GrillBot a Azure Storage Blob.",
    "points": "Služba řesící správu bodů (transakcí, slučování, reporting, ...)",
    "image-processing": "Mezi služba pro vykreslování a caching obrázků.",
    "audit-log": "Služba pro logování provozu (evidence, prezentace, statistiky, ...)",
}

databases = {
    "grillbot": {"Databáze": "/static/database.svg", "Cache": "/static/cache.svg"},
    "graphics": None,
    "rubbergod": {"Databáze": "/static/rubbergod_db.svg"},
    "file": None,
    "points": {"Databáze": "/static/database_points.svg"},
    "image-processing": None,
    "audit-log": {"Databáze": "/static/database_audit-log.svg"},
}

di_graphs = {
    "grillbot": "/static/di-graph.svg",
    "graphics": None,
    "rubbergod": "/static/di-graph-rubbergod.svg",
    "file": "/static/di-graph-file.svg",
    "points": "/static/di-graph-points.svg",
    "image-processing": "/static/di-graph-image-processing.svg",
    "audit-log": "/static/di-graph-audit-log.svg",
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
            "DELETE /api/pins/{guildId}/{channelId}",
            [200],
            [],
            "Smaže všechny piny z cache.",
        ),
        build_api_description(
            "GET /api/pins/{guildId}/{channelId}?markdown={markdown}",
            [200],
            [],
            "Získání pinů. Možné vygenerovat JSON obsah nebo markdown.",
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
    "image-processing": [
        build_api_description(
            "GET /api/diag",
            [200],
            ["application/json"],
            "Vrací diagnostické informace o stavu služby (počty, využití paměti, statistiky, ...).",
        ),
        build_api_description(
            "POST /api/image/peepolove",
            [200, 400],
            ["image/png", "image/gif", "application/json"],
            "Vytvoří obrázek peepa držícího profilovku uživatele.",
        ),
        build_api_description(
            "POST /api/image/peepoangry",
            [200, 400],
            ["image/png", "image/gif", "application/json"],
            "Vytvoří obrázek peepa naštvaně zírajícího na profilovku uživatele.",
        ),
        build_api_description(
            "POST /api/image/points",
            [200, 400],
            ["image/png", "application/json"],
            "Vykreslení obrázku s aktuálním stavem bodů uživatele.",
        ),
        build_api_description(
            "POST /api/image/without-accident",
            [200, 400],
            ["image/png", "application/json"],
            "Vykreslení obrázku znělky ze seriálu The Simpsons s počtem dní od posledního incidentu.",
        ),
        build_api_description(
            "POST /api/image/chart",
            [200, 400],
            ["image/png", "application/json"],
            "Vygenerování grafu. <b>Jediný podporovaný je spojnicový graf.</b>",
        ),
    ],
    "audit-log": [
        build_api_description(
            "POST /api/archivation",
            [200, 204],
            ["application/json"],
            "Archivace starých logů. Pokud není k archivaci alespoň 5000 záznamů, tak se vrací 204 No Content.",
        ),
        build_api_description(
            "GET /api/diag",
            [200],
            ["application/json"],
            "Vrací diagnostické informace o stavu služby (počty, využití paměti, statistiky, ...).",
        ),
        build_api_description(
            "POST /api/info/jobs",
            [200],
            ["application/json"],
            "Informace o bězích naplánovaných úloh (počet spuštění, poslední běh, časy, ...)",
        ),
        build_api_description(
            "GET /api/info/dashboard",
            [200],
            ["application/json"],
            "Informace o voláních služeb, příkazech, atd. pro hlavní scénu webové administrace.",
        ),
        build_api_description(
            "POST /api/logItem",
            [200, 400],
            ["application/json"],
            "Požadavek na vytvoření nového záznamu v logu.",
        ),
        build_api_description(
            "DELETE /api/logItem/{id}",
            [200, 404],
            ["application/json"],
            "Smazání záznamu z logu (vč. informací o existujících souborech).<br>Vrací příznak, zda smazání proběhlo "
            + "úspěšně a seznam souborů, které se mají smazat z úložiště.",
        ),
        build_api_description(
            "GET /api/logItem/{id}",
            [200, 404],
            ["application/json"],
            "Získání detailu záznamu. Pokud záznam neexistuje, nebo k němu neexistuje detail, tak se vrátí 404 Not Found.",
        ),
        build_api_description(
            "GET /api/logItem/search",
            [200, 400],
            ["application/json"],
            "Vyhledávání v logu a vyčítání formou seznamu.",
        ),
        build_api_description(
            "GET /api/statistics/auditLog",
            [200],
            ["application/json"],
            "Statistika audit logu (počty záznamů, počty a objemy souborů)",
        ),
        build_api_description(
            "GET /api/statistics/interactions/list",
            [200],
            ["application/json"],
            "Seznam provedených příkazů a jejich statistika.",
        ),
        build_api_description(
            "GET /api/statistics/interactions/userstats",
            [200],
            ["application/json"],
            "Statistika provádění příkazů křížem přes uživatele.",
        ),
        build_api_description(
            "GET /api/statistics/api/stats",
            [200],
            ["application/json"],
            "Statistika volání API",
        ),
        build_api_description(
            "GET /api/statistics/api/userstats/{criteria}",
            [200],
            ["application/json"],
            "Statistika volání API křížem přes uživatele.<br>Vyžadováno kritérium. "
            + "Povolené hodnoty jsou <code>v1-private</code>, <code>v1-public</code>, <code>v2</code>",
        ),
        build_api_description(
            "GET /api/statistics/avgtimes",
            [200],
            ["application/json"],
            "Statistika průměrných časů za dny.",
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
    "image-processing": "https://raw.githubusercontent.com/GrillBot/GrillBot.Services/master/src/ImageProcessingService/ImageProcessingService.csproj",  # noqa: E501
    "audit-log": "https://raw.githubusercontent.com/GrillBot/GrillBot.Services/master/src/AuditLogService/AuditLogService.csproj",  # noqa: E501
}

healthcheck_endpoints = {
    "grillbot": None,
    "graphics": "https://grillbot.cloud/graphics/health",
    "rubbergod": "https://grillbot.cloud/rubbergod/health",
    "file": "https://grillbot.cloud/file/health",
    "points": "https://grillbot.cloud/points/health",
    "image-processing": "https://grillbot.cloud/image-processing/health",
    "audit-log": "https://grillbot.cloud/audit-log/health"
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

        if self.service_name in databases and databases[self.service_name] is not None:
            result["database"] = databases[self.service_name]

        if self.service_name in di_graphs and di_graphs[self.service_name] is not None:
            result["di_graph"] = di_graphs[self.service_name]

        if (
            self.service_name in api_descriptions
            and api_descriptions[self.service_name] is not None
        ):
            result["api_description"] = api_descriptions[self.service_name]

        if self.service_name == "grillbot":
            result["swagger_url"] = "https://grillbot.cloud/swagger"

        if (
            self.service_name in project_files
            and project_files[self.service_name] is not None
        ):
            deps = self.download_deps(project_files[self.service_name])
            if deps is not None:
                result["dependencies"] = deps

        if self.service_name in healthcheck_endpoints and healthcheck_endpoints[self.service_name] is not None:
            logging.info(f'Checking online status of {self.service_name}')
            result["is_online"] = requests.head(healthcheck_endpoints[self.service_name]).status_code == 200

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
