import requests
from rich.prompt import Prompt, IntPrompt
from rich.console import Console
from rich.table import Table
from rich import print
from rich.panel import Panel
from rich.traceback import install
from rich.columns import Columns
from typing import Type

install(show_locals=True)
console: Type[Console] = Console()


class Anime:
    def __init__(self, name: str) -> None:
        self.BASE_URL = "https://api.jikan.moe/v4/"
        self.name = name
        self.id = self.anime_id()

    def request(self, url: str, **kwargs) -> dict:
        url = self.BASE_URL + url
        try:
            response = requests.get(url, **kwargs)
            response.raise_for_status()
            data = response.json()
            return data
        except Exception as e:
            raise e

    def anime_id(self) -> int:
        data = {"q": self.name, "page": "1", "limit": "1"}
        response = self.request("anime", params=data)
        try:
            id = response["data"][0]["mal_id"]
            return id
        except KeyError:
            raise Exception("Could not find the anime ", self.name)

    def _suggestions(self) -> list:
        suggestions_title = []
        param = {"q": self.name, "page": "1", "limit": "10"}
        data = self.request(f"anime", params=param)
        for anime in data["data"]:
            if anime["title_english"]:
                suggestions_title.append(anime["title_english"])
            elif anime["title"]:
                suggestions_title.append(anime["title"])
        return suggestions_title

    def anime(self) -> dict:
        data = self.request(f"anime/{self.id}")
        return data["data"]

    def characters(self) -> list:
        data = self.request(f"anime/{self.id}/characters")
        return data["data"]

    def episodes(self) -> list:
        data = self.request(f"anime/{self.id}/episodes")
        return data["data"]

    def statistics(self) -> list:
        data = self.request(f"anime/{self.id}/statistics")
        return data["data"]

    def streaming(self):
        data = self.request(f"anime/{self.id}/streaming")
        return data["data"]


table = Table(
    title="Anime",
    row_styles=["cyan"],
    show_lines=True,
    highlight=True,
    title_style="bold magenta",
)

table.add_column("Key", justify="center")
table.add_column("Value", justify="left")


def add_to_table(table, data, parent_key=""):
    if isinstance(data, dict):
        for key, value in data.items():
            current_key = (
                f"{parent_key} >> {str(key).capitalize()}" if parent_key else key
            )
            if isinstance(value, dict):
                add_to_table(table, value, current_key)
            elif isinstance(value, list):
                for item in value:
                    if isinstance(item, dict):
                        add_to_table(table, item, current_key)
                    else:
                        table.add_row(current_key.capitalize(), str(item))
            else:
                table.add_row(current_key.capitalize(), str(value))
    elif isinstance(data, list):
        for item in data:
            if isinstance(item, dict):
                add_to_table(table, item, parent_key)
            else:
                table.add_row(parent_key.capitalize(), str(item))


def prompt() -> Type[Anime]:
    print(Panel("Anime Information", title="Welcome to", subtitle="Anime world"))
    try:
        anime = Prompt.ask("Search anime ", default="Attack on titan")
        anime = Anime(anime)
        suggestion_list = anime._suggestions()
        suggestions = [f"[{i + 1}] {v}" for i, v in enumerate(suggestion_list)]
        columns = Columns(suggestions, expand=True, equal=True)
        print(columns)
        confirmed_anime_index = IntPrompt.ask("\nChoose an anime", default=1)
        print("\nChoosen anime: ", suggestion_list[confirmed_anime_index - 1])
        confirmation = Anime(suggestion_list[confirmed_anime_index - 1])
        return confirmation
    except KeyboardInterrupt:
        exit(0)


def displayMethods(anime: Type[Anime]) -> str:
    name: str = anime.name
    _: int = name.find("]")
    name: str = name[_ + 1 :]
    methods: list = [
        "Restart",
        name,
        "characters",
        "episodes",
        "statistics",
        "streaming",
    ]
    methods: list = [f"[{i}] {v.capitalize()}" for i, v in enumerate(methods)]
    columns = Columns(methods, expand=True, equal=True)
    print(columns)
    try:
        choosen_method = IntPrompt.ask("\nChoose a method", default=1)
    except KeyboardInterrupt:
        exit(0)
    match choosen_method:
        case 0:
            anime = displayMethods(prompt())
        case 1:
            add_to_table(table, anime.anime())
            console.print(table)
        case 2:
            add_to_table(table, anime.characters())
            console.print(table)
        case 3:
            add_to_table(table, anime.episodes())
            console.print(table)
        case 4:
            add_to_table(table, anime.statistics())
            console.print(table)
        case 5:
            add_to_table(table, anime.streaming())
            console.print(table)
        case _:
            print("Invalid input")


if __name__ == "__main__":
    x = prompt()
    while 1:
        displayMethods(x)
