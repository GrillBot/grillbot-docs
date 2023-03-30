from .source import dotnet, node


class DataSource:
    def get_data(self) -> dict:
        raise NotImplementedError()


class DependencyDataSource(DataSource):
    def __init__(self) -> None:
        self.dotnet = dotnet.DotnetDependencyList()

    def get_data(self) -> dict:
        return {
            "dotnet": self.dotnet.get_data(),
            "graphics": node.NodeDependencyList(
                "https://raw.githubusercontent.com/GrillBot/GrillBot.Services/master/src/Graphics/package.json"
            ).get_data(),
            "private-web": node.NodeDependencyList(
                "https://raw.githubusercontent.com/GrillBot/GrillBot.Web/master/src/PrivateAdmin/package.json"
            ).get_data(),
            "public-web": node.NodeDependencyList(
                "https://raw.githubusercontent.com/GrillBot/GrillBot.Web/master/src/PublicAdmin/package.json"
            ).get_data(),
            "karma-web": node.NodeDependencyList(
                "https://raw.githubusercontent.com/GrillBot/GrillBot.Web/master/src/KarmaWeb/package.json"
            ).get_data(),
        }


page_to_data_source = {"dependency": DependencyDataSource()}
