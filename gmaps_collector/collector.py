import time
from gmaps_collector.response import Response


class Collector:
    def __init__(self, task_progress, gmaps_token: str, type_: str, location: tuple[float, float], radius: int):
        self.response = Response(task_progress, gmaps_token, type_, radius, location)

    def collect(self):
        for item in self.response:
            print(item)
