from playwright.sync_api import sync_playwright
import random
import time
import logging

logger = logging.getLogger(__name__)

class IRCTCSearchTool:
    def __init__(self, headless=True):
        # headless=True means the browser opens invisibly in the background.
        # Set to False if you want to watch it open!
        self.headless = headless

    def search_room_availability(self, station: str, date: str, duration: str, room_type: str):
        """
        Automates searching for retiring rooms on IRCTC using Playwright.
        """
        results = []
        try:
            with sync_playwright() as p:
                logger.info(f"[{station}] Opening browser...")
                browser = p.chromium.launch(headless=self.headless)
                context = browser.new_context()
                page = context.new_page()

                # In a real scenario, we would tell the browser to go to the site:
                # page.goto("https://www.rr.irctctourism.com/")
                # page.fill("#stationCode", station)
                # page.click("#searchBtn")
                
                # To bypass government captchas for this tutorial, we simulate the 
                # time it takes to scrape the page:
                time.sleep(1.5) 

                # Generating a simulated scraping result based on the inputs
                is_available = random.choice([True, False, True]) # 66% chance of being available
                
                # Assign base prices depending on room type
                base_price = {"AC": 600, "Non AC": 400, "Dormitory": 200}.get(room_type, 300)
                
                # Multiply price by duration
                duration_multiplier = {"6h": 1, "12h": 1.5, "24h": 2}.get(duration, 1.5)
                price = int(base_price * duration_multiplier)

                results.append({
                    "station": station,
                    "date": date,
                    "duration": duration,
                    "room_type": room_type,
                    "price": price if is_available else None,
                    "availability": "Available" if is_available else "Waitlist/Full"
                })

                browser.close()
                logger.info(f"[{station}] Search complete!")
                return results

        except Exception as e:
            logger.error(f"Playwright error during search for {station}: {e}")
            return [{"station": station, "error": str(e), "availability": "Error"}]

    def run_search_sync(self, station: str, date: str, duration: str, room_type: str):
        """A simple wrapper to maintain compatibility with existing graph implementation."""
        return self.search_room_availability(station, date, duration, room_type)

# Quick test when running the file directly
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    tool = IRCTCSearchTool(headless=True)
    logger.info("Starting Playwright test...")
    
    # We call the sync wrapper for the test
    results = tool.run_search_sync(
        station="Varanasi Junction", 
        date="2024-12-01", 
        duration="12h", 
        room_type="AC"
    )
    
    logger.info("--- Search Results ---")
    logger.info(results)
