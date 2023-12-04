import logging
import time
from datetime import datetime, timezone
import googlemaps

logger = logging.getLogger(f"{__name__}_Request")
SLEEP = 3


def generate_date() -> datetime:
    current_utc_datetime = datetime.now(timezone.utc)
    today_utc = datetime(current_utc_datetime.year, current_utc_datetime.month, current_utc_datetime.day, 0, 0, 0,
                         tzinfo=timezone.utc)
    return today_utc


class GmapsAPIError(Exception):
    pass


class InvalidAPIKey(Exception):
    pass


class Response:
    def __init__(self, task_progress: 'TaskResult', token: str, type_: str, radius: int, location: tuple) -> None:
        self.type_ = type_
        self.location = location
        self.radius = radius
        self._current = 0
        self._response = {}
        self._data = []
        self.token = token

        logger.debug(f"Creating Request {str(self)}")
        self.task_progress = task_progress
        self.task_progress.change_status_to_running()

    def _create_gmaps_client(self):
        try:
            self.client = googlemaps.Client(key=self.token)
        except ValueError:
            error = f"Invalid API key {self.token[0:10]}..."
            logger.error(error)
            raise InvalidAPIKey(error)

    def __str__(self) -> str:
        return f"type: {self.type_}, location: {self.location}, radius: {self.radius}, next page token: {self._next_page}"

    def _make_request(self):
        logger.debug(f"Send request({str(self)})")
        try:
            if self.type_ and self.location and not self._next_page:
                self._response = self.client.places_nearby(location=self.location, type=self.type_, radius=self.radius)
            else:
                self._response = self.client.places(page_token=self._next_page)
            self._data.extend(self._response.get('results', []))
            logger.debug(f"Collected {len(self._response.get('results', []))} items. Request {str(self)}")
            self.task_progress.update_progress(len(self._response.get('results', [])))
            time.sleep(SLEEP)
        except googlemaps.exceptions.Timeout:
            error = f"Request timeout error. Check api limit {str(self)}"
            logger.error(error)
            raise GmapsAPIError(error)
        except googlemaps.exceptions.ApiError as err:
            error = f"Request api error: {str(err)}  With Request: {str(self)}"
            logger.error(error)
            raise GmapsAPIError(error)

    @property
    def _next_page(self) -> str:
        return self._response.get('next_page_token', '')

    def __iter__(self):
        return self

    def __collect_all(self) -> None:
        try:
            self._create_gmaps_client()
            self._make_request()
            while self._next_page:
                self._make_request()
            self.task_progress.change_status_to_done()
        except GmapsAPIError as err:
            self.task_progress.change_status_to_error(error=str(err))
        except InvalidAPIKey as err:
            self.task_progress.change_status_to_error(error=str(err))

    def __next__(self) -> str:
        if not self._data:
            self.__collect_all()
        if self._current < len(self._data) - 1:
            self._data[self._current]['collected_date'] = generate_date()
            current = self._data[self._current]
            self._current += 1
            return current
        raise StopIteration
