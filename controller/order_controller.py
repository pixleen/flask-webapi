from flask import Blueprint, request, jsonify, render_template
from model.orders import Order

order_blueprint = Blueprint('order_blueprint', __name__)

@order_blueprint.route('/order-car', methods=['POST'])
def order_vehicle():
    if request.is_json:
        data = request.get_json()
        Order.order_vehicle(data['customer_id'], data['car_id'])
        return jsonify({"Success": "Car ordered"}), 200
    return jsonify({"Error": "Request must be JSON"}), 415

@order_blueprint.route('/', methods=['GET'])
def retrieve_orders():
    orders = Order.retrieve_all()
    return render_template('orders.html', orders=orders)

@order_blueprint.route('/cancel-order-car', methods=['POST'])
def cancel_order_vehicle():
    if request.is_json:
        data = request.get_json()
        Order.cancel_order_vehicle(data['customer_id'], data['car_id'])
        return jsonify({"Success": "Car order canceled"}), 200
    return jsonify({"Error": "Request must be JSON"}), 415

@order_blueprint.route('/rent-car', methods=['POST'])
def rent_vehicle():
    if request.is_json:
        data = request.get_json()
        Order.rent_car(data['customer_id'], data['car_id'])
        return jsonify({"Success": "Car rented"}), 200
    return jsonify({"Error": "Request must be JSON"}), 415

@order_blueprint.route('/return-car', methods=['POST'])
def return_vehicle():
    if request.is_json:
        data = request.get_json()
        Order.return_car(data['customer_id'], data['car_id'], data['status'])
        return jsonify({"Success": "Car returned"}), 200
    return jsonify({"Error": "Request must be JSON"}), 415
