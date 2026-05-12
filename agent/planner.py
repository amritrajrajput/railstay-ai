import logging
from database.stations import StationDatabase

logger = logging.getLogger(__name__)

class SearchPlanner:
    def __init__(self, db_params):
        """Initialize with database parameters to fetch stations."""
        self.db = StationDatabase(db_params)

    def generate_combinations(self, city: str, date: str, duration: str, room_type: str):
        """
        Generates all possible combinations for the search space.
        E.g., Stations in City x Given Room Type x Given Duration x Given Date.
        """
        stations = self.db.get_stations_for_city(city)
        if not stations:
            logger.warning(f"No stations found in DB for {city}.")
            return []

        combinations = []
        for station in stations:
            comb = {
                "station_name": station.get("station_name"),
                "station_code": station.get("station_code"),
                "date": date,
                "duration": duration,
                "room_type": room_type
            }
            combinations.append(comb)
            
        return combinations