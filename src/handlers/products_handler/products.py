import json
from bson import ObjectId

from src.handlers.base_handler import BaseHandler
from uuid import uuid4


class Products(BaseHandler):
    def get_products(self) -> list:
        data = self.db.get_products()
        products = [{key: str(value) if isinstance(value, ObjectId) else value for key, value in product.items()} for
                    product in data]
        return products

    def add_product(self, product: dict) -> None:
        # Check if picture is present in the product dict
        if 'picture' in product:
            # Extract picture file and upload to S3
            picture = product.pop('picture')  # Remove picture from product dict
            picture_url = self.s3.upload_picture_to_s3(picture=picture)
            product['picture'] = picture_url  # Update product dict with picture URL
        product['id'] = str(uuid4())
        # Insert the updated product into the database
        self.db.insert_new_product(product_data=product)

    def delete_product(self, product_id: str) -> None:
        product = self.db.get_product(product_id=product_id)
        self.s3.delete_picture_from_s3(picture_url=product["picture"])
        self.db.delete_product(product_id=product_id)

    def get_product(self, product_id: str) -> dict:
        product = self.db.get_product(product_id=product_id)
        product['_id'] = str(product['_id'])
        return product

    def toggle_active(self, product_id: str) -> None:
        product = self.db.get_product(product_id=product_id)
        if product['active']:
            active = False
        else:
            active = True
        self.db.toggle_active(product_id=product_id, active=active)

    def edit_product(self, product: dict, picture_change: bool) -> None:
        old_product = self.db.get_product(product_id=product["id"])
        if picture_change:
            self.s3.delete_picture_from_s3(picture_url=old_product["picture"])
            picture = product.pop('picture')  # Remove picture from product dict
            picture_url = self.s3.upload_picture_to_s3(picture=picture)
            product['picture'] = picture_url  # Update product dict with picture URL
        # Insert the updated product into the database
        self.db.update_product(product_id=product["id"], product_data=product)
