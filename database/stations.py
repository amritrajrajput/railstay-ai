import psycopg2
from psycopg2.extras import RealDictCursor


class StationDatabase:
    def __init__(self, db_params):
        """Initialize the database connection"""
        self.db_params = db_params
        self._init_db()
        self._seed_data_if_empty()

    def _get_connection(self):
        return psycopg2.connect(**self.db_params)

    def _init_db(self):
        """Create tables if they don't exist"""
        try:
            with self._get_connection() as conn:
                with conn.cursor() as cur:
                    cur.execute('''
                        CREATE TABLE IF NOT EXISTS stations (
                            id SERIAL PRIMARY KEY,
                            city VARCHAR(100) NOT NULL,
                            station_name VARCHAR(150) NOT NULL,
                            station_code VARCHAR(10)
                        );
                    ''')
                conn.commit()
        except Exception:
            # Fail silently so the app can still run
            pass

    def _seed_data_if_empty(self):
        """Seed initial data if table is empty"""
        try:
            with self._get_connection() as conn:
                with conn.cursor() as cur:
                    cur.execute("SELECT COUNT(*) FROM stations")
                    if cur.fetchone()[0] == 0:
                        seeds = [
                            ("Varanasi", "Varanasi Junction", "BSB"),
                            ("Varanasi", "Banaras", "BSBS"),
                            ("Varanasi", "Kashi", "KEI"),
                            ("Varanasi", "Manduadih", "MUV"),
                            ("Varanasi", "Pt. Deen Dayal Upadhyay", "DDU")
                        ]

                        cur.executemany(
                            "INSERT INTO stations (city, station_name, station_code) VALUES (%s, %s, %s)",
                            seeds
                        )
                conn.commit()
        except Exception:
            pass

    def get_stations_for_city(self, city: str):
        """Returns a list of stations for a given city."""
        try:
            with self._get_connection() as conn:
                with conn.cursor(cursor_factory=RealDictCursor) as cur:
                    cur.execute(
                        "SELECT station_name, station_code FROM stations WHERE city ILIKE %s",
                        (city,)
                    )
                    return cur.fetchall()
        except Exception:
            return self._fallback_stations(city)

    def _fallback_stations(self, city: str):
        """Fallback mock data if DB is unavailable."""
        if city.lower() == "varanasi":
            return [
                {"station_name": "Varanasi Junction", "station_code": "BSB"},
                {"station_name": "Banaras", "station_code": "BSBS"},
                {"station_name": "Kashi", "station_code": "KEI"},
                {"station_name": "Manduadih", "station_code": "MUV"},
                {"station_name": "Pt. Deen Dayal Upadhyay", "station_code": "DDU"}
            ]
        return []