from typing import Iterable

from BaseClasses import Region
from ..game_data.general import scugs_all


class RainWorldRegion(Region):
    game = "Rain World"


class Room(RainWorldRegion):
    pass


class RoomData:
    def __init__(self, name: str, scugs: list[str]):
        self.name = name
        self.scugs = scugs


class ConnectionData:
    def __init__(self, source: str, dest: str, scugs: set[str] = None):
        self.source = source
        self.dest = dest
        self.scugs = scugs or scugs_all
