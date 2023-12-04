from pyrosm import get_data


class NoneFieldAtAddress(Exception):
    pass


def get_map(region: str) -> str:
    fp = get_data(region, update=True, directory='tmp_maps')
    return fp

