from uuid import uuid4

from bson import ObjectId

from src.handlers.base_handler import BaseHandler


class Orders(BaseHandler):
    def get_orders(self) -> list:
        data = self.db.get_orders()
        orders = [{key: str(value) if isinstance(value, ObjectId) else value for key, value in order.items()} for
                  order in data]
        return orders

    def delete_order(self, order_id: str) -> None:
        self.db.delete_order(order_id=order_id)

    def add_order(self, order: dict) -> None:
        order['id'] = str(uuid4())
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
        order_summary = self.generate_order_summary(order=order, is_client=False)
        self.email_sender.send_email_notification('zechem.gf@gmail.com', 'New Order Notification',
                                                  order_summary)

        customer_email = order.get('email')
        if customer_email:
            order_summary = self.generate_order_summary(order=order, is_client=True)
            self.email_sender.send_email_notification(customer_email, 'הזמנתך נקלטה בצחם', order_summary)

    def generate_order_summary(self, order: dict, is_client: bool):
        if not is_client:
            phone_message = f"<p style='direction: rtl; text-align: right;'>מספר טלפון : {order['phoneNumber']}</p>"
        else:
            phone_message = ""
        # Generate items summary as an unordered list with RTL direction
        items_summary = "<div style='direction: rtl; text-align: right; display:flex; flex-direction:column; gap:5px;'>"
        for item in order['products']:
            items_summary += f"<span style='direction: rtl; text-align: right;'>{item['name']} כמות - {item['quantity']}</span>"
        items_summary += "</div>"

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
    </body>
    </html>"""
        return order_summary
