from datetime import datetime
from mvg import MvgApi


STATION_NAME = "Josephsplatz, München"
MAX_DEPARTURES_PER_TYPE = 6


def format_time(timestamp: int) -> str:
    """
    Convert Unix timestamp to HH:MM format.
    Example: 1778771700 -> 17:15
    """
    return datetime.fromtimestamp(timestamp).strftime("%H:%M")


def minutes_until(timestamp: int) -> int:
    """
    Calculate how many minutes are left until the departure.
    Negative values are returned as 0.
    """
    departure_time = datetime.fromtimestamp(timestamp)
    seconds_left = (departure_time - datetime.now()).total_seconds()
    minutes_left = round(seconds_left / 60)

    return max(minutes_left, 0)


def clean_departure(dep: dict) -> dict:
    """
    Convert the raw MVG departure dictionary into a cleaner format
    that is easier to use in the website.
    """
    return {
        "line": dep["line"],
        "destination": dep["destination"],
        "type": dep["type"],
        "time": format_time(dep["time"]),
        "minutes_left": minutes_until(dep["time"]),
        "platform": dep.get("platform"),
        "delay": dep.get("delay"),
        "realtime": dep.get("realtime"),
        "cancelled": dep.get("cancelled", False),
    }


def get_departures() -> dict:
    """
    Fetch departures for Josephsplatz and return separated Bus and U-Bahn lists.
    """
    station = MvgApi.station(STATION_NAME)
    station_id = station["id"]

    api = MvgApi(station_id)
    departures = api.departures()

    bus_departures = [
        clean_departure(dep)
        for dep in departures
        if dep["type"] == "Bus" and not dep["cancelled"]
    ]

    ubahn_departures = [
        clean_departure(dep)
        for dep in departures
        if dep["type"] == "U-Bahn" and not dep["cancelled"]
    ]

    return {
        "station_name": "Josephsplatz",
        "updated_at": datetime.now().strftime("%H:%M:%S"),
        "bus": bus_departures[:MAX_DEPARTURES_PER_TYPE],
        "ubahn": ubahn_departures[:MAX_DEPARTURES_PER_TYPE],
    }