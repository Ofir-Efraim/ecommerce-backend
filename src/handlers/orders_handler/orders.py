from datetime import datetime
from uuid import uuid4

import pytz
from bson import ObjectId

from src.handlers.base_handler import BaseHandler


class Orders(BaseHandler):
    def get_orders(self, page: int, rows_per_page: int) -> [list, int]:
        skip = (page - 1) * rows_per_page
        limit = rows_per_page
        data = self.db.get_orders(skip=skip, limit=limit)
        orders = []
        for order in data:
            # Convert timestamp to desired format
            order['date'] = datetime.fromtimestamp(timestamp=float(order['date']),
                                                   tz=pytz.timezone('Asia/Tel_Aviv')).strftime('%H:%M - %d/%m/%Y')
            # Convert ObjectId to string
            order = {key: str(value) if isinstance(value, ObjectId) else value for key, value in order.items()}
            orders.append(order)
        count = self.db.count_orders()
        return orders, count

    def get_new_orders(self, page: int, rows_per_page: int) -> [list, int]:
        skip = (page - 1) * rows_per_page
        limit = rows_per_page
        data = self.db.get_new_orders(skip=skip, limit=limit)
        orders = []
        for order in data:
            # Convert timestamp to desired format
            order['date'] = datetime.fromtimestamp(timestamp=float(order['date']),
                                                   tz=pytz.timezone('Asia/Tel_Aviv')).strftime('%H:%M - %d/%m/%Y')
            # Convert ObjectId to string
            order = {key: str(value) if isinstance(value, ObjectId) else value for key, value in order.items()}
            orders.append(order)
        count = self.db.count_new_orders()
        return orders, count

    def get_order(self, order_id: str) -> dict:
        order = self.db.get_order(order_id=order_id)
        order['_id'] = str(order['_id'])
        order['date'] = datetime.fromtimestamp(timestamp=float(order['date']),
                                               tz=pytz.timezone('Asia/Tel_Aviv')).strftime('%H:%M - %d/%m/%Y')
        return order

    def delete_order(self, order_id: str) -> None:
        self.db.delete_order(order_id=order_id)

    def mark_order_delivered(self, order_id: str) -> None:
        self.db.mark_order_delivered(order_id=order_id)

    def mark_order_new(self, order_id: str) -> None:
        self.db.mark_order_new(order_id=order_id)

    def mark_order_paid(self, order_id: str) -> None:
        self.db.mark_order_paid(order_id=order_id)

    def mark_order_unpaid(self, order_id: str) -> None:
        self.db.mark_order_unpaid(order_id=order_id)

    def add_order(self, order: dict) -> str:
        customer_email = order.get('email')
        if customer_email:
            order_summary = self.generate_order_summary(order=order, is_client=True)
            self.email_sender.send_email_notification(customer_email, 'אישור הזמנה צחם', order_summary)
        order_summary = self.generate_order_summary(order=order, is_client=False)
        self.email_sender.send_email_notification('zechem.gf@gmail.com', 'הזמנה חדשה בצחם',
                                                  order_summary)
        order_id = str(uuid4())
        order['id'] = order_id
        order_date = datetime.utcnow().timestamp()
        order['date'] = order_date
        self.db.insert_new_order(order_data=order)

        existing_customer = self.db.get_client(phone_number=order['phoneNumber'])

        if not existing_customer:
            new_customer_data = {
                'first_name': order.get('firstName'),
                'last_name': order.get('lastName'),
                'phone_number': order.get('phoneNumber'),
                'email': order.get('email'),
                'address': order.get('pickupSpot') or order.get('address'),
                "id": str(uuid4())
            }
            self.db.insert_new_client(client_data=new_customer_data)
        return order_id

    def generate_order_summary(self, order: dict, is_client: bool):
        if not is_client:
            phone_message = f"<p style='direction: rtl; text-align: right;'>מספר טלפון : {order['phoneNumber']}</p>"
        else:
            phone_message = ""

        # Generate items summary as an unordered list with RTL direction
        items_summary = ""
        for item in order['products']:
            items_summary += f"<p style='direction: rtl; text-align: right;'>{item['name']} כמות - {item['quantity']}</p>"

        # Determine location message and value
        if 'pickupSpot' in order:
            location_message = "מקום איסוף"
            location_value = order['pickupSpot']
        else:
            location_message = "כתובת משלוח"
            location_value = order['address']

        # Construct HTML-formatted order summary
        order_summary = f"""<html>
    <head>
        <style>
            body {{
                direction: rtl;
                text-align: right;
            }}
        </style>
    </head>
    <body>
        <p style='direction: rtl; text-align: right;'>שלום {order['firstName']} {order['lastName']},</p>

        <p style='direction: rtl; text-align: right;'>הזמנתך נקלטה בצחם:</p>

        {items_summary}

        <p style='direction: rtl; text-align: right;'>על סך: {order['totalPrice']} ש"ח</p>

        <p style='direction: rtl; text-align: right;'>{location_message}: {location_value}</p>

        {phone_message}

        <p style='direction: rtl; text-align: right;'>בברכה,</p>

        <p style='direction: rtl; text-align: right;'>צחם-לחם בריאות מצמחים</p>
        <img src='cid:logo' alt='logo'/>
    </body>
    </html>"""
        return order_summary
