import os

from src.db_utils.get_db_instance import get_db_instance


class ZechemDBUtils:

    def __init__(self):
        self.db = get_db_instance()

    def get_products(self):
        try:
            table_name = os.environ.get("PRODUCTS_TABLE_NAME", "products")
            return self.db.find(table_name=table_name, query={})
        except Exception as e:
            print(f"Error in ZechemDBUtils.get_products: {e}")
            raise e

    def get_active_products(self):
        try:
            table_name = os.environ.get("PRODUCTS_TABLE_NAME", "products")
            return self.db.find(table_name=table_name, query={"active": True})
        except Exception as e:
            print(f"Error in ZechemDBUtils.get_products: {e}")
            raise e

    def get_product(self, product_id: str):
        try:
            table_name = os.environ.get("PRODUCTS_TABLE_NAME", "products")
            return self.db.find_one(table_name=table_name, query={"id": product_id})
        except Exception as e:
            print(f"Error in ZechemDBUtils.get_product: {e}")
            raise e

    def insert_new_product(self, product_data: dict):
        try:
            table_name = os.environ.get("PRODUCTS_TABLE_NAME", "products")
            return self.db.insert_one(table_name=table_name, document=product_data)
        except Exception as e:
            print(f"Error in ZechemDBUtils.insert_new_product: {e}")
            raise e

    def delete_product(self, product_id: str):
        try:
            table_name = os.environ.get("PRODUCTS_TABLE_NAME", "products")
            return self.db.delete_one(table_name=table_name, query={"id": product_id})
        except Exception as e:
            print(f"Error in ZechemDBUtils.delete_product: {e}")
            raise e

    def toggle_active(self, product_id: str, active: bool):
        try:
            table_name = os.environ.get("PRODUCTS_TABLE_NAME", "products")
            product_data = {"active": active}  # Constructing the data to update
            return self.db.update_one(table_name=table_name, query={"id": product_id}, new_data=product_data)
        except Exception as e:
            print(f"Error in ZechemDBUtils.toggle_active: {e}")
            raise e

    def update_product(self, product_id: str, product_data: dict):
        try:
            table_name = os.environ.get("PRODUCTS_TABLE_NAME", "products")
            return self.db.update_one(table_name=table_name, query={"id": product_id}, new_data=product_data)
        except Exception as e:
            print(f"Error in ZechemDBUtils.update_product: {e}")
            raise e

    def get_locations(self):
        try:
            table_name = os.environ.get("LOCATIONS_TABLE_NAME", "locations")
            return self.db.find(table_name=table_name, query={})
        except Exception as e:
            print(f"Error in ZechemDBUtils.get_locations: {e}")
            raise e

    def insert_new_location(self, location_data: dict):
        try:
            table_name = os.environ.get("LOCATIONS_TABLE_NAME", "locations")
            return self.db.insert_one(table_name=table_name, document=location_data)
        except Exception as e:
            print(f"Error in ZechemDBUtils.insert_new_location: {e}")
            raise e

    def delete_location(self, location_id: str):
        try:
            table_name = os.environ.get("LOCATIONS_TABLE_NAME", "locations")
            return self.db.delete_one(table_name=table_name, query={"id": location_id})
        except Exception as e:
            print(f"Error in ZechemDBUtils.delete_location: {e}")
            raise e

    def get_orders(self, skip: int, limit: int):
        try:
            table_name = os.environ.get("ORDERS_TABLE_NAME", "orders")
            return self.db.find(table_name=table_name, query={}, sort=[("date", -1)], skip=skip, limit=limit)
        except Exception as e:
            print(f"Error in ZechemDBUtils.get_orders: {e}")
            raise e

    def count_orders(self):
        try:
            table_name = os.environ.get("ORDERS_TABLE_NAME", "orders")
            return self.db.count_documents(table_name=table_name, query={})
        except Exception as e:
            print(f"Error in ZechemDBUtils.count_orders: {e}")
            raise e

    def get_new_orders(self, skip: int, limit: int):
        try:
            table_name = os.environ.get("ORDERS_TABLE_NAME", "orders")
            return self.db.find(table_name=table_name, query={"status": "new"}, sort=[("date", -1)], skip=skip,
                                limit=limit)
        except Exception as e:
            print(f"Error in ZechemDBUtils.get_new_orders: {e}")
            raise e

    def count_new_orders(self):
        try:
            table_name = os.environ.get("ORDERS_TABLE_NAME", "orders")
            return self.db.count_documents(table_name=table_name, query={"status": "new"})
        except Exception as e:
            print(f"Error in ZechemDBUtils.count_new_orders: {e}")
            raise e

    def get_order(self, order_id: str):
        try:
            table_name = os.environ.get("ORDERS_TABLE_NAME", "orders")
            return self.db.find_one(table_name=table_name, query={"id": order_id})
        except Exception as e:
            print(f"Error in ZechemDBUtils.get_order: {e}")
            raise e

    def mark_order_delivered(self, order_id: str):
        try:
            table_name = os.environ.get("ORDERS_TABLE_NAME", "orders")
            return self.db.update_one(table_name=table_name, query={"id": order_id}, new_data={"status": "delivered"})
        except Exception as e:
            print(f"Error in ZechemDBUtils.mark_order_delivered: {e}")
            raise e

    def mark_order_new(self, order_id: str):
        try:
            table_name = os.environ.get("ORDERS_TABLE_NAME", "orders")
            return self.db.update_one(table_name=table_name, query={"id": order_id}, new_data={"status": "new"})
        except Exception as e:
            print(f"Error in ZechemDBUtils.mark_order_new: {e}")
            raise e

    def mark_order_paid(self, order_id: str):
        try:
            table_name = os.environ.get("ORDERS_TABLE_NAME", "orders")
            return self.db.update_one(table_name=table_name, query={"id": order_id}, new_data={"paid": True})
        except Exception as e:
            print(f"Error in ZechemDBUtils.mark_order_paid: {e}")
            raise e

    def mark_order_unpaid(self, order_id: str):
        try:
            table_name = os.environ.get("ORDERS_TABLE_NAME", "orders")
            return self.db.update_one(table_name=table_name, query={"id": order_id}, new_data={"paid": False})
        except Exception as e:
            print(f"Error in ZechemDBUtils.mark_order_unpaid: {e}")
            raise e

    def delete_order(self, order_id: str):
        try:
            table_name = os.environ.get("ORDERS_TABLE_NAME", "orders")
            return self.db.delete_one(table_name=table_name, query={"id": order_id})
        except Exception as e:
            print(f"Error in ZechemDBUtils.delete_order: {e}")
            raise e

    def insert_new_order(self, order_data: dict):
        try:
            table_name = os.environ.get("ORDERS_TABLE_NAME", "orders")
            return self.db.insert_one(table_name=table_name, document=order_data)
        except Exception as e:
            print(f"Error in ZechemDBUtils.insert_new_order: {e}")
            raise e

    def get_clients(self, skip: int, limit: int):
        try:
            table_name = os.environ.get("CLIENTS_TABLE_NAME", "clients")
            return self.db.find(table_name=table_name, query={}, skip=skip, limit=limit)
        except Exception as e:
            print(f"Error in ZechemDBUtils.get_clients: {e}")
            raise e

    def count_clients(self):
        try:
            table_name = os.environ.get("CLIENTS_TABLE_NAME", "clients")
            return self.db.count_documents(table_name=table_name, query={})
        except Exception as e:
            print(f"Error in ZechemDBUtils.count_clients: {e}")
            raise e

    def delete_client(self, client_id: str):
        try:
            table_name = os.environ.get("CLIENTS_TABLE_NAME", "clients")
            return self.db.delete_one(table_name=table_name, query={"id": client_id})
        except Exception as e:
            print(f"Error in ZechemDBUtils.delete_client: {e}")
            raise e

    def get_client(self, phone_number: str):
        try:
            table_name = os.environ.get("CLIENTS_TABLE_NAME", "clients")
            return self.db.find_one(table_name=table_name, query={"phone_number": phone_number})
        except Exception as e:
            print(f"Error in ZechemDBUtils.get_client: {e}")
            raise e

    def insert_new_client(self, client_data: dict):
        try:
            table_name = os.environ.get("CLIENTS_TABLE_NAME", "clients")
            return self.db.insert_one(table_name=table_name, document=client_data)
        except Exception as e:
            print(f"Error in ZechemDBUtils.insert_new_client: {e}")
            raise e
