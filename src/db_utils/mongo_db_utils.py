from typing import List

from pymongo import MongoClient, CursorType, ReturnDocument

from src.db_utils.base_db_utils import BaseDBUtils


class MongoDBUtils(BaseDBUtils):
    def __init__(self, host: str, username: str, password: str, db_name: str):
        super().__init__(host=host, username=username, password=password, db_name=db_name)
        if not hasattr(self, 'client'):
            self._connect()

    def _connect(self):
        try:
            # self.client = MongoClient(host=self.host, port=self.port, username=self.username, password=self.password)
            print('Creating new connection to MongoDB')
            self.client = MongoClient(
                f'mongodb+srv://{self.username}:{self.password}@{self.host}/?retryWrites=true&w=majority')
            self.db = self.client[self.db_name]
            print('Created a new connection to MongoDB successfully')
        except Exception as e:
            print(f"MongoDBUtils._connect failed. Here's why: {type(e).__name__} - {e.__str__()}")
            raise e

    def _disconnect(self):
        try:
            self.client.close()
        except Exception as e:
            print(f"MongoDBUtils._disconnect failed. Here's why: {type(e).__name__} - {e.__str__()}")
            raise e

    def insert_one(self, table_name: str, document: dict):
        try:
            return self.db[table_name].insert_one(document=document)
        except Exception as e:
            print(f"MongoDBUtils.insert_one failed. Here's why: {type(e).__name__} - {e.__str__()}")
            raise e

    def insert_many(self, table_name: str, documents: list):
        try:
            return self.db[table_name].insert_many(documents=documents)
        except Exception as e:
            print(f"MongoDBUtils.insert_one failed. Here's why: {type(e).__name__} - {e.__str__()}")
            raise e

    def find(self, table_name: str, query: dict, skip: int = 0, limit: int = 0, sort: List[tuple] = None,
             projection: dict = None, cursor_type: int = CursorType.NON_TAILABLE):
        try:
            data = self.db[table_name].find(filter=query, skip=skip, limit=limit, sort=sort, cursor_type=cursor_type,
                                            projection=projection)
            return data if data else None
        except Exception as e:
            print(f"MongoDBUtils.find failed. Here's why: {type(e).__name__} - {e.__str__()}")
            raise e

    def find_one(self, table_name: str, query: dict):
        try:
            data = self.db[table_name].find_one(filter=query)
            return data if data else None
        except Exception as e:
            print(f"MongoDBUtils.find_one failed. Here's why: {type(e).__name__} - {e.__str__()}")
            raise e

    def find_one_and_update(self, table_name: str, query: dict, new_data: dict, operator: str = '$set',
                            sort: List[tuple] = None, upsert: bool = False,
                            return_document: bool = ReturnDocument.BEFORE):
        try:
            if operator:
                operator_query = {operator: new_data}
                return self.db[table_name].find_one_and_update(filter=query, update=operator_query, upsert=upsert,
                                                               sort=sort, return_document=return_document)
            return self.db[table_name].find_one_and_update(filter=query, update=new_data, upsert=upsert, sort=sort,
                                                           return_document=return_document)
        except Exception as e:
            print(
                f"MongoDBUtils.find_one_and_update failed. Here's why: {type(e).__name__} - {e.__str__()}")
            raise e

    def update_many(self, table_name: str, query: dict, new_data: dict, operator: str = '$set', upsert: bool = False):
        try:
            if operator:
                operator_query = {operator: new_data}
                return self.db[table_name].update_many(filter=query, update=operator_query, upsert=upsert)
            return self.db[table_name].update_many(filter=query, update=new_data, upsert=upsert)
        except Exception as e:
            print(f"MongoDBUtils.update_many failed. Here's why: {type(e).__name__} - {e.__str__()}")
            raise e

    def update_one(self, table_name: str, query: dict, new_data: dict, operator: str = '$set', upsert: bool = False):
        try:
            if operator:
                operator_query = {operator: new_data}
                return self.db[table_name].update_one(filter=query, update=operator_query, upsert=upsert)
            return self.db[table_name].update_many(filter=query, update=new_data, upsert=upsert)
        except Exception as e:
            print(f"MongoDBUtils.update_one failed. Here's why: {type(e).__name__} - {e.__str__()}")
            raise e

    def aggregate(self, table_name: str, pipeline: list, max_time: int = 60000, batch_size: int = 100,
                  allow_disk_use: bool = False):
        try:
            return self.db[table_name].aggregate(pipeline=pipeline, maxTimeMS=max_time, batchSize=batch_size,
                                                 allowDiskUse=allow_disk_use)
        except Exception as e:
            print(f"MongoDBUtils.update_one failed. Here's why: {type(e).__name__} - {e.__str__()}")
            raise e

    def delete_one(self, table_name: str, query: dict):
        try:
            return self.db[table_name].delete_one(filter=query)
        except Exception as e:
            print(f"MongoDBUtils.delete_one failed. Here's why: {type(e).__name__} - {e}")
            raise e

    def delete_many(self, table_name: str, query: dict):
        try:
            return self.db[table_name].delete_many(filter=query)
        except Exception as e:
            print(f"MongoDBUtils.delete_many failed. Here's why: {type(e).__name__} - {e}")
            raise e

    def count_documents(self, table_name: str, query: dict):
        try:
            return self.db[table_name].count_documents(filter=query)
        except Exception as e:
            print(f"MongoDBUtils.count_documents failed. Here's why: {type(e).__name__} - {e}")
            raise e
