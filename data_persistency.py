import os
import json
import logging

logger = logging.getLogger(__name__)


class SavedData:
    FILE = "cache/data.json"

    DEFAULTS = {
        "artists": []
    }

    def __init__(self):
        self.data = self.load()

    def load(self):
        os.makedirs(os.path.dirname(self.FILE), exist_ok=True)

        if not os.path.exists(self.FILE):
            self.data = self.DEFAULTS.copy()
            self.save()
            return self.data

        try:
            with open(self.FILE, "r", encoding="utf-8") as f:
                data = json.load(f)

            for key, value in self.DEFAULTS.items():
                data.setdefault(key, value)

            return data

        except (json.JSONDecodeError, OSError) as e:
            logger.error(f"Failed to load data file: {e}")
            return self.DEFAULTS.copy()

    def save(self):
        os.makedirs(os.path.dirname(self.FILE), exist_ok=True)

        with open(self.FILE, "w", encoding="utf-8") as f:
            json.dump(self.data, f, indent=4, ensure_ascii=False)

    # -------------------------
    # generic access
    # -------------------------

    def get(self, key):
        return self.data.get(key)

    def set(self, key, value):
        self.data[key] = value
        self.save()

    # -------------------------
    # artist helpers
    # -------------------------

    def _find_artist_index(self, name):
        for i, artist in enumerate(self.data["artists"]):
            if artist.get("name") == name:
                return i
        return None

    def add_artist(self, name, notes=""):
        if self._find_artist_index(name) is not None:
            logger.warning(f'Artist "{name}" already exists')
            return

        self.data["artists"].append({
            "name": name,
            "notes": notes
        })

        self.save()

    def get_artist(self, name):
        idx = self._find_artist_index(name)
        if idx is None:
            return None

        return self.data["artists"][idx]

    def remove_artist(self, name):
        idx = self._find_artist_index(name)
        if idx is None:
            logger.warning(f'Artist "{name}" not found')
            return

        del self.data["artists"][idx]
        self.save()

    def get_all_artists(self):
        return self.data["artists"]

    def set_artist_notes(self, name, notes):
        idx = self._find_artist_index(name)
        if idx is None:
            logger.warning(f'Artist "{name}" not found')
            return

        self.data["artists"][idx]["notes"] = notes
        self.save()

    def move_artist(self, initial_index, target_index):
        artists = self.data["artists"]

        if target_index < 0 or target_index >= len(artists):
            return

        artists[initial_index], artists[target_index] = (
            artists[target_index],
            artists[initial_index]
        )

        self.save()