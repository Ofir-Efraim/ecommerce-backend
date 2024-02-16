from bson import ObjectId

from src.handlers.base_handler import BaseHandler


class Clients(BaseHandler):
    def get_clients(self) -> list:
        data = self.db.get_clients()
        clients = [{key: str(value) if isinstance(value, ObjectId) else value for key, value in client.items()} for
                   client in data]
        return clients

    def delete_client(self, client_id: str) -> None:
        self.db.delete_client(client_id=client_id)
