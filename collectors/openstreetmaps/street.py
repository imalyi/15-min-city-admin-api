from collectors.openstreetmaps.common import get_map, NoneFieldAtAddress
from collectors.database import get_database
from pyrosm import OSM


class Street:
    def __init__(self, country: str, progress) -> None:
        self.country = country
        self.db = get_database('address')
        self.osm = OSM(get_map(country))
        self.progress = progress

    def update(self):
        for address in self.addresses:
            self.db.add_item(address)

    @property
    def addresses(self):
        for index, row in self.osm.get_buildings().iterrows():
            try:
                address = {
                    'city': row.get('addr:city', ''),
                    'housenumber': row.get('addr:housenumber', ''),
                    'street': row.get('addr:street', ''),
                    'country': self.country,
                    'latitude': row.geometry.centroid.y,
                    'longitude': row.geometry.centroid.x
                }
                address['full'] = f"{address['city']}, {address['street']}, {address['housenumber']}, {address['country']}"

            except KeyError as err:
                self.progress.add_error(str(row), f"Cant get attribute {err}")
                print(f"Error with {row}. Can't get row: {err}")
                continue

            try:
                # Check if all fields are not None
                if any(field is None or field == '' for field in address.values()):
                    print("None field found: ", address)
                    raise NoneFieldAtAddress
                self.progress.update_progress(1)
                yield address
            except NoneFieldAtAddress:
                continue
