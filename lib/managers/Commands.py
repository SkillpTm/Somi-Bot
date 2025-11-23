import json
import typing

from lib.managers.Config import Config
from lib.managers.Singleton import Singleton



class Commands(metaclass=Singleton):
    """Holds all the commands.json data on it"""

    def __init__(self):
        with open("./commands.json", "r", encoding="UTF-8") as file:
            commands_data = json.load(file)

        self.data: dict[str, Command] = {}
        self.overview: dict[str, str] = {}

        for command_data in commands_data:
            new_command = Command(command_data)
            self.data[new_command.full_name] = new_command
            if new_command.parent.name != "sudo" and new_command.name != "rules":
                self.overview[f"/{new_command.full_name}"] = new_command.full_name

        self.overview = dict(sorted(self.overview.items()))

class Command():
    def __init__(self, data: dict[str, typing.Any]) -> None:
        self.parent: CommandParent = CommandParent(data["parent"])
        self.name: str = data["name"]
        self.alias: str = data["alias"]
        self.description: str = data["description"]
        self.example: str = data["example"].replace("APPLICATION_NAME", str(Config().APPLICATION_NAME))
        self.parameters: dict[str, CommandParameter] = {key: CommandParameter(value) for key, value in data["parameters"].items()}
        self.permissions: list[str] = data["permissions"]

        self.full_name = f"{self.parent.name} {self.name}".strip()
        if len(self.parameters) > 0:
            self.structure = f"/{self.full_name} {' '.join([f'[{parameter.name}]' for _, parameter in self.parameters.items()])}"
        else:
            self.structure = f"/{self.full_name} (no parameters)"

class CommandParent():
    def __init__(self, data: dict[str, str]) -> None:
        self.name: str = data.get("name", "")
        self.alias: str = data.get("alias", "")

class CommandParameter():
    def __init__(self, data: dict[str, typing.Any]) -> None:
        self.name: str = data["name"]
        self.description: str = data["description"]
        self.type: str = data["type"]
        self.required: bool = data["required"]
        self.default: str = data["default"]