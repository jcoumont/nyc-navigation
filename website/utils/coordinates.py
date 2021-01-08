from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut


class LocationUnknownException(Exception):
    pass


class LocationNotInNyException(Exception):
    pass


def __do_geocode(address: str, attempt: int = 1, max_attempts: int = 5) -> object:
    geolocator = Nominatim(user_agent="nyc-navigation")
    try:
        return geolocator.geocode(address)
    except GeocoderTimedOut:
        if attempt <= max_attempts:
            return __do_geocode(address, attempt=attempt + 1)
        raise


def get_coordinates(address: str):
    location = __do_geocode(address)
    if location == None:
        # return "unknown address"
        raise LocationUnknownException
    elif "New York" not in location.address:
        raise LocationNotInNyException
    else:
        return (location.latitude, location.longitude)  # , location.address)


if __name__ == "__main__":
    try:
        print(get_coordinates("175 5th Avenue NYC"))
        print(get_coordinates("uguugvuv"))
        print(get_coordinates("Liège"))

        print(get_coordinates("5 Ave"))
        print(get_coordinates("5 Ave NYC"))
        print(get_coordinates("5th Avenue NYC"))
        print(get_coordinates("5th Avenue New York"))
        print(get_coordinates("40.8147478, -73.9361291"))
    except LocationUnknownException:
        print("Unknown address")
    except LocationNotInNyException:
        print("Address not in New York")

# (40.741059199999995, -73.98964162240998)
# unknown address
# address not in New York

# (40.753821, -73.9819629) -> metro 42nd Street
# (40.753821, -73.9819629)
# address not in New York
# (40.8147478, -73.9361291)
# (40.8147478, -73.9361291)
