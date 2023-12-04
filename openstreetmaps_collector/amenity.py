from pyrosm import OSM
from gmaps_collector.database import get_database
from openstreetmaps_collector.common import get_map


class Amenities:
    def __init__(self, country: str) -> None:
        self.country = country
        self.db = get_database('amenity')
        self.osm = OSM(get_map(country))

    @property
    def amenities(self):
        for index, row in self.osm.get_pois({'amenity': True}).iterrows():
            amenity = {
                'name': row['name'],
                'amenity': row['amenity'],
                'city': row['addr:city'],
                'housenumber': row['addr:housenumber'],
                'street': row['addr:street'],
                'country': self.country,
                'latitude': row.geometry.centroid.y,
                'longitude': row.geometry.centroid.x
            }
            yield amenity

    def update(self):
        for amenity in self.amenities:
            self.db.add_item(amenity)
