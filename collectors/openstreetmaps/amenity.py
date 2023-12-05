from pyrosm import OSM
from collectors.database import get_database
from collectors.openstreetmaps.common import get_map


class Amenity:
    def __init__(self, country: str, progress) -> None:
        self.country = country
        self.db = get_database('amenity')
        self.osm = OSM(get_map(country))
        self.progress = progress

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
                'location': [row.geometry.centroid.x, row.geometry.centroid.y]
            }
            self.progress.update_amenity_progress(1)
            yield amenity

    def update(self):
        for amenity in self.amenities:
            self.db.add_item(amenity)
