from uuid import uuid4

from bson import ObjectId

from src.handlers.base_handler import BaseHandler


class CouponCodes(BaseHandler):
    def get_coupon_codes(self) -> list:
        data = self.db.get_coupon_codes()
        coupon_codes = [
            {key: str(value) if isinstance(value, ObjectId) else value for key, value in coupon_code.items()} for
            coupon_code in data]
        return coupon_codes

    def add_coupon_code(self, coupon_code: str) -> None:
        coupon_code = {
            "coupon_code": coupon_code,
            "id": str(uuid4()),
            "active": True,
        }
        self.db.insert_new_coupon_code(coupon_code_data=coupon_code)

    def delete_coupon_code(self, coupon_code_id: str) -> None:
        self.db.delete_coupon_code(coupon_code_id=coupon_code_id)

    def toggle_coupon_code_active(self, coupon_code_id: str) -> None:
        coupon_code = self.db.get_coupon_code_by_id(coupon_code_id=coupon_code_id)
        if coupon_code['active']:
            active = False
        else:
            active = True
        self.db.toggle_coupon_code_active(coupon_code_id=coupon_code_id, active=active)

    def is_coupon_code_valid(self, coupon_code: str) -> bool:
        coupon_code = self.db.get_coupon_code_by_code(coupon_code=coupon_code)
        if coupon_code and coupon_code['active']:
            return True
        return False
