import time
from gmaps_collector.response import Response
from gmaps_collector.database import get_database


class Collector:
    def __init__(self, task_progress, gmaps_token: str, type_: str, location: tuple[float, float], radius: int) -> None:
        self.response = Response(task_progress, gmaps_token, type_, radius, location)
        self.db = get_database('gmaps')

    def collect(self) -> None:
        for item in self.response:
            self.db.add_item(item)