import json
import awsgi
from botocore.exceptions import ClientError
from flask import Flask, jsonify, request
from flask_cors import CORS
from src.handlers.products_handler.products import Products
from src.handlers.locations_handler.locations import Locations
from src.handlers.orders_handler.orders import Orders
from src.handlers.clients_handler.clients import Clients
from src.handlers.coupon_codes_handler.coupon_codes import CouponCodes

app = Flask(__name__)
CORS(app)

products_handler = Products()
locations_handler = Locations()
orders_handler = Orders()
clients_handler = Clients()
coupon_codes_handler = CouponCodes()


@app.route('/get_products', methods=['GET'])
def get_products():
    products = products_handler.get_products()
    return jsonify({'products': products}), 200


@app.route('/get_active_products', methods=['GET'])
def get_active_products():
    products = products_handler.get_active_products()
    return jsonify({'products': products}), 200


@app.route('/add_product', methods=['POST'])
def add_product():
    # Check if the request contains form data
    if request.method == 'POST' and 'picture' in request.files:
        # Extract form data
        name = request.form.get('name')
        description = request.form.get('description')
        price = request.form.get('price')
        active = bool(request.form.get('active'))
        picture = request.files['picture']
        nutritional_values_json = request.form.get('nutritionalValues')

        # Convert nutritionalValues back to dictionary
        nutritional_values = json.loads(nutritional_values_json)

        # Construct product object
        product = {
            'name': name,
            'description': description,
            'price': price,
            'picture': picture,
            'active': active,
            'nutritionalValues': nutritional_values
        }

        # Handle the product using your products_handler module
        products_handler.add_product(product=product)

        return jsonify({'message': 'Product added successfully'}), 201
    else:
        return jsonify({'error': 'Invalid request'}), 400


@app.route('/delete_product/<string:product_id>', methods=['DELETE'])
def delete_product(product_id):
    try:
        products_handler.delete_product(product_id=product_id)
        return jsonify({'message': 'Product deleted successfully'}), 200
    except:
        return jsonify({'message': 'Product not found'}), 404


@app.route('/get_product/<string:product_id>', methods=['GET'])
def get_product(product_id):
    try:
        product = products_handler.get_product(product_id=product_id)
        return jsonify({'product': product}), 200
    except:
        return jsonify({'message': 'Product not found'}), 404


@app.route('/toggle_active/<string:product_id>', methods=['POST'])
def toggle_active(product_id):
    try:
        products_handler.toggle_active(product_id=product_id)
        return jsonify({'message': 'Product toggle successful'}), 200
    except:
        return jsonify({'message': 'Product not found'}), 404


@app.route('/edit_product', methods=['POST'])
def edit_product():
    try:
        # Check if the request contains form data
        if 'picture' in request.files:
            picture_change = True
            picture = request.files['picture']
        else:
            picture_change = False
            picture = request.form.get('picture')
        name = request.form.get('name')
        description = request.form.get('description')
        price = request.form.get('price')
        product_id = request.form.get('product_id')
        active = bool(request.form.get('active'))

        nutritional_values_json = request.form.get('nutritionalValues')

        # Convert nutritionalValues back to dictionary
        nutritional_values = json.loads(nutritional_values_json)

        # Construct product object
        product = {
            'name': name,
            'description': description,
            'price': price,
            'picture': picture,
            'active': active,
            'nutritionalValues': nutritional_values,
            'id': product_id
        }

        # Handle the product using your products_handler module
        products_handler.edit_product(product=product, picture_change=picture_change)

        return jsonify({'message': 'Product added successfully'}), 201
    except:
        return jsonify({'error': 'Invalid request'}), 400


@app.route('/get_locations', methods=['GET'])
def get_locations():
    locations = locations_handler.get_locations()
    return jsonify({'locations': locations}), 200


@app.route('/add_location', methods=['POST'])
def add_location():
    data = request.json
    location_name = data.get('location_name')
    if location_name:
        locations_handler.add_location(location_name=location_name)
        return jsonify({'message': 'Location added successfully'}), 201
    else:
        return jsonify({'error': 'Missing location_name parameter'}), 400


@app.route('/delete_location/<string:location_id>', methods=['DELETE'])
def delete_location(location_id):
    try:
        locations_handler.delete_location(location_id=location_id)
        return jsonify({'message': f'Location with ID {location_id} deleted successfully'}), 200
    except:
        return jsonify({'error': 'Location not found'}), 404


@app.route('/get_orders', methods=['GET'])
def get_orders():
    page = int(request.args.get('page'))
    rows_per_page = int(request.args.get('rows_per_page'))
    query = json.loads(request.args.get('query'))
    search = request.args.get('search')
    orders, count, sum_price = orders_handler.get_orders(page=page, rows_per_page=rows_per_page, query=query,
                                                         search=search)
    return jsonify({'orders': orders, 'total': count, "sum_price": sum_price}), 200


@app.route('/get_order/<string:order_id>', methods=['GET'])
def get_order(order_id):
    order = orders_handler.get_order(order_id=order_id)
    return jsonify({'order': order}), 200


@app.route('/mark_order_delivered/<string:order_id>', methods=['POST'])
def mark_order_delivered(order_id):
    try:
        orders_handler.mark_order_delivered(order_id=order_id)
        return jsonify({'message': f'Order with ID {order_id} marked as delivered'}), 200
    except:
        return jsonify({'error': 'Order not found'}), 404


@app.route('/mark_order_new/<string:order_id>', methods=['POST'])
def mark_order_new(order_id):
    try:
        orders_handler.mark_order_new(order_id=order_id)
        return jsonify({'message': f'Order with ID {order_id} marked as new'}), 200
    except:
        return jsonify({'error': 'Order not found'}), 404


@app.route('/mark_order_bagged/<string:order_id>', methods=['POST'])
def mark_order_bagged(order_id):
    try:
        orders_handler.mark_order_bagged(order_id=order_id)
        return jsonify({'message': f'Order with ID {order_id} marked as bagged'}), 200
    except:
        return jsonify({'error': 'Order not found'}), 404


@app.route('/mark_order_unbagged/<string:order_id>', methods=['POST'])
def mark_order_unbagged(order_id):
    try:
        orders_handler.mark_order_unbagged(order_id=order_id)
        return jsonify({'message': f'Order with ID {order_id} marked as unbagged'}), 200
    except:
        return jsonify({'error': 'Order not found'}), 404


@app.route('/mark_order_paid/<string:order_id>', methods=['POST'])
def mark_order_paid(order_id):
    try:
        orders_handler.mark_order_paid(order_id=order_id)
        return jsonify({'message': f'Order with ID {order_id} marked as paid'}), 200
    except:
        return jsonify({'error': 'Order not found'}), 404


@app.route('/mark_order_unpaid/<string:order_id>', methods=['POST'])
def mark_order_unpaid(order_id):
    try:
        orders_handler.mark_order_unpaid(order_id=order_id)
        return jsonify({'message': f'Order with ID {order_id} marked as unpaid'}), 200
    except:
        return jsonify({'error': 'Order not found'}), 404


@app.route('/delete_order/<string:order_id>', methods=['DELETE'])
def delete_order(order_id):
    try:
        orders_handler.delete_order(order_id=order_id)
        return jsonify({'message': f'Order with ID {order_id} deleted successfully'}), 200
    except:
        return jsonify({'error': 'Order not found'}), 404


@app.route('/submit_order', methods=['POST'])
def submit_order():
    data = request.json
    order = data.get('order')
    try:
        order_id = orders_handler.add_order(order=order)
        return jsonify({'message': 'order sent successfully', "order_id": order_id}), 200
    except ClientError as e:
        return jsonify({'error': "כתובת מייל לא מורשה, אנא נסה כתובת אחרת"}), 400


@app.route('/get_clients', methods=['GET'])
def get_clients():
    page = int(request.args.get('page'))
    rows_per_page = int(request.args.get('rows_per_page'))
    search = request.args.get('search')
    clients, count = clients_handler.get_clients(page=page, rows_per_page=rows_per_page, search=search)
    return jsonify({'clients': clients, 'total': count}), 200


@app.route('/delete_client/<string:client_id>', methods=['DELETE'])
def delete_client(client_id):
    try:
        clients_handler.delete_client(client_id=client_id)
        return jsonify({'message': f'Client with ID {client_id} deleted successfully'}), 200
    except:
        return jsonify({'error': 'Client not found'}), 404


@app.route('/get_coupon_codes', methods=['GET'])
def get_coupon_codes():
    coupon_codes = coupon_codes_handler.get_coupon_codes()
    return jsonify({'coupon_codes': coupon_codes}), 200


@app.route('/add_coupon_code', methods=['POST'])
def add_coupon_code():
    data = request.json
    coupon_code = data.get('coupon_code')
    discount_percentage = data.get('discount_percentage')
    if coupon_code and discount_percentage:
        coupon_codes_handler.add_coupon_code(coupon_code=coupon_code, discount_percentage=discount_percentage)
        return jsonify({'message': 'Coupon Code added successfully'}), 201
    else:
        return jsonify({'error': 'Missing coupon_code or discount_percentage parameter'}), 400


@app.route('/delete_coupon_code/<string:coupon_code_id>', methods=['DELETE'])
def delete_coupon_code(coupon_code_id):
    try:
        coupon_codes_handler.delete_coupon_code(coupon_code_id=coupon_code_id)
        return jsonify({'message': f'Coupon Code with ID {coupon_code_id} deleted successfully'}), 200
    except:
        return jsonify({'error': 'Coupon Code not found'}), 404


@app.route('/toggle_coupon_code_active/<string:coupon_code_id>', methods=['POST'])
def toggle_coupon_code_active(coupon_code_id):
    try:
        coupon_codes_handler.toggle_coupon_code_active(coupon_code_id=coupon_code_id)
        return jsonify({'message': 'Coupon Code toggle successful'}), 200
    except:
        return jsonify({'message': 'Coupon Code not found'}), 404


@app.route('/is_coupon_code_valid', methods=['POST'])
def is_coupon_code_valid():
    data = request.json
    coupon_code = data.get('coupon_code')
    discount_percentage = coupon_codes_handler.is_coupon_code_valid(coupon_code=coupon_code)
    if discount_percentage:
        return jsonify({'is_coupon_code_valid': True, "discount_percentage": discount_percentage}), 200
    else:
        return jsonify({'is_coupon_code_valid': False, "discount_percentage": 0}), 200


def lambda_handler(event, context):
    return awsgi.response(app, event, context, base64_content_types={"image/png", "image/jpg", "image/jpeg"})


if __name__ == '__main__':
    app.run()
