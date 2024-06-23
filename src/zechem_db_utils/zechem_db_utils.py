import os
import re

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

    def get_orders(self, skip: int, limit: int, query: dict):
        try:
            table_name = os.environ.get("ORDERS_TABLE_NAME", "orders")
            return self.db.find(table_name=table_name, query=query, sort=[("date", -1)], skip=skip, limit=limit)
        except Exception as e:
            print(f"Error in ZechemDBUtils.get_orders: {e}")
            raise e

    def count_orders(self, query: dict):
        try:
            table_name = os.environ.get("ORDERS_TABLE_NAME", "orders")
            return self.db.count_documents(table_name=table_name, query=query)
        except Exception as e:
            print(f"Error in ZechemDBUtils.count_orders: {e}")
            raise e

    def sum_orders(self,query: dict):
        try:
            table_name = os.environ.get("ORDERS_TABLE_NAME", "orders")
            pipeline = [
                {"$match": query},  # Match documents based on the query
                {"$group": {
                    "_id": None,  # Group all documents into one group
                    "total_sum": {"$sum": "$totalPrice"}  # Sum the totalPrice field
                }}
            ]

            results = list(self.db.aggregate(table_name=table_name, pipeline=pipeline))
            if results:
                return results[0]['total_sum']  # Return the sum of totalPrice
            else:
                return 0  # Return 0 if no documents match the query

        except Exception as e:
            print(f"MongoDBUtils.sum_orders failed. Here's why: {type(e).__name__} - {e}")
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

    def mark_order_bagged(self, order_id: str):
        try:
            table_name = os.environ.get("ORDERS_TABLE_NAME", "orders")
            return self.db.update_one(table_name=table_name, query={"id": order_id}, new_data={"bagged": True})
        except Exception as e:
            print(f"Error in ZechemDBUtils.mark_order_bagged: {e}")
            raise e

    def mark_order_unbagged(self, order_id: str):
        try:
            table_name = os.environ.get("ORDERS_TABLE_NAME", "orders")
            return self.db.update_one(table_name=table_name, query={"id": order_id}, new_data={"bagged": False})
        except Exception as e:
            print(f"Error in ZechemDBUtils.mark_order_unbagged: {e}")
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

    def get_clients(self, skip: int, limit: int, search: str):
        try:
            table_name = os.environ.get("CLIENTS_TABLE_NAME", "clients")
            # Construct regex pattern for the search term
            regex_pattern = re.compile(f".*{search}.*", re.IGNORECASE)
            # Construct query with regex filters for first_name and last_name
            query = {
                "$or": [
                    {"first_name": {"$regex": regex_pattern}},
                    {"last_name": {"$regex": regex_pattern}}
                ]
            }
            return self.db.find(table_name=table_name, query=query, skip=skip, limit=limit)
        except Exception as e:
            print(f"Error in ZechemDBUtils.get_clients: {e}")
            raise e

    def count_clients(self, search: str):
        try:
            table_name = os.environ.get("CLIENTS_TABLE_NAME", "clients")
            # Construct regex pattern for the search term
            regex_pattern = re.compile(f".*{search}.*", re.IGNORECASE)
            # Construct query with regex filters for first_name and last_name
            query = {
                "$or": [
                    {"first_name": {"$regex": regex_pattern}},
                    {"last_name": {"$regex": regex_pattern}}
                ]
            }
            return self.db.count_documents(table_name=table_name, query=query)
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

    def transform_query(self, query: dict, search: str) -> dict:
        transformed_query = {}
        regex_pattern = re.compile(f".*{search}.*", re.IGNORECASE)

        # Construct query with regex filters for first_name and last_name
        name_query = {
            "$or": [
                {"firstName": {"$regex": regex_pattern}},
                {"lastName": {"$regex": regex_pattern}}
            ]
        }

        # Add name_query to the transformed_query
        transformed_query["$and"] = [name_query]

        # Add existing query conditions
        for key, value in query.items():
            if isinstance(value, list):
                transformed_list = []
                for item in value:
                    if isinstance(item, str) and item.lower() in ['true', 'false']:
                        transformed_list.append(item.lower() == 'true')
                    else:
                        transformed_list.append(item)
                transformed_query[key] = {"$in": transformed_list}
            elif isinstance(value, str) and value.lower() in ['true', 'false']:
                transformed_query[key] = value.lower() == 'true'
            else:
                transformed_query[key] = value

        return transformed_query
