from bson import ObjectId

from src.handlers.base_handler import BaseHandler


class Clients(BaseHandler):
    def get_clients(self, page: int, rows_per_page: int) -> [list, int]:
        skip = (page - 1) * rows_per_page
        limit = rows_per_page
        data = self.db.get_clients(skip=skip, limit=limit)
        clients = [{key: str(value) if isinstance(value, ObjectId) else value for key, value in client.items()} for
                   client in data]
        count = self.db.count_clients()
        return clients, count

    def delete_client(self, client_id: str) -> None:
        self.db.delete_client(client_id=client_id)
