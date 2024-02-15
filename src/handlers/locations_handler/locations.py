import json
from bson import ObjectId

from src.handlers.base_handler import BaseHandler
from uuid import uuid4


class Locations(BaseHandler):
    def get_locations(self) -> list:
        data = self.db.get_locations()
        locations = [{key: str(value) if isinstance(value, ObjectId) else value for key, value in location.items()} for
                     location in data]
        return locations

    def add_location(self, location_name: str) -> None:
        location = {
            "name": location_name,
            "id": str(uuid4())
        }
        self.db.insert_new_location(location_data=location)

    def delete_location(self, location_id: str) -> None:
        self.db.delete_location(location_id=location_id)
