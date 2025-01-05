import os
import json

WATCHLIST_FILE = "watchlists.json"

# Global state variables
cached_courses = []
user_watchlists = {}
previous_filtered_data = {}
application = None


def load_watchlists():
    global user_watchlists
    if os.path.exists(WATCHLIST_FILE):
        try:
            with open(WATCHLIST_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
            # Convert lists back to sets
            for chat_id, watchlist in data.items():
                user_watchlists[chat_id] = set(watchlist)
        except Exception as e:
            print(f"Error loading watchlists: {e}")


def save_watchlists():
    global user_watchlists
    try:
        # Convert sets to lists
        serialized_watchlists = {
            chat_id: list(watchlist) for chat_id, watchlist in user_watchlists.items()
        }
        with open(WATCHLIST_FILE, "w", encoding="utf-8") as f:
            json.dump(serialized_watchlists, f)
    except Exception as e:
        print(f"Error saving watchlists: {e}")


load_watchlists()
