from flask import Blueprint, request, jsonify, render_template
from models.order import Order

order_blueprint = Blueprint('order_blueprint', __name__)

@order_blueprint.route('/order-car', methods=['POST'])
def order_car():
    if request.is_json:
        data = request.get_json()
        Order.order_car(data['customer_id'], data['car_id'])
        return jsonify({"success": "Car ordered successfully"}), 200
    return jsonify({"error": "Request must be JSON"}), 415

@order_blueprint.route('/', methods=['GET'])
def get_orders():
    orders = Order.get_all()
    return render_template('orders.html', orders=orders)

@order_blueprint.route('/cancel-order-car', methods=['POST'])
def cancel_order_car():
    if request.is_json:
        data = request.get_json()
        Order.cancel_order_car(data['customer_id'], data['car_id'])
        return jsonify({"success": "Car order canceled successfully"}), 200
    return jsonify({"error": "Request must be JSON"}), 415

@order_blueprint.route('/rent-car', methods=['POST'])
def rent_car():
    if request.is_json:
        data = request.get_json()
        Order.rent_car(data['customer_id'], data['car_id'])
        return jsonify({"success": "Car rented successfully"}), 200
    return jsonify({"error": "Request must be JSON"}), 415

@order_blueprint.route('/return-car', methods=['POST'])
def return_car():
    if request.is_json:
        data = request.get_json()
        Order.return_car(data['customer_id'], data['car_id'], data['status'])
        return jsonify({"success": "Car returned successfully"}), 200
    return jsonify({"error": "Request must be JSON"}), 415
