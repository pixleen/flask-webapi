from flask import Blueprint, request, jsonify, render_template
from model.orders import Order

order_blueprint = Blueprint('order_blueprint', __name__)

@order_blueprint.route('/order-car', methods=['POST'])
def order_vehicle():
    if request.is_json:
        data = request.get_json()
        order_details = Order.order_vehicle(data['customer_id'], data['car_id'])
        print(order_details)
        
        if "Error" in order_details:
            return jsonify(order_details), 400 
        elif order_details:
            return jsonify({"Success": "Car ordered", "Order": order_details}), 200
        else:
            return jsonify({"Error": "Car could not be ordered. Vehicle may not be available."}), 400
    return jsonify({"Error": "Request must be JSON"}), 415



@order_blueprint.route('/', methods=['GET'])
def retrieve_orders():
    orders = Order.retrieve_all()
    return render_template('orders.html', orders=orders)
 
@order_blueprint.route('/cancel-order-car', methods=['POST'])
def cancel_order_vehicle():
    if request.is_json:
        data = request.get_json()
        result = Order.cancel_order_vehicle(data['customer_id'], data['car_id'])
        
        if "Error" in result:
            return jsonify(result), 400 
        else:
            return jsonify(result), 200  
    return jsonify({"Error": "Request must be JSON"}), 415


@order_blueprint.route('/rent-car', methods=['POST'])
def rent_car():
    if request.is_json:
        data = request.get_json()
        result = Order.rent_car(data['customer_id'], data['car_id'])
        
        if "Error" in result:
            return jsonify(result), 400 
        else:
            return jsonify(result), 200 
    
    return jsonify({"Error": "Request must be JSON"}), 415


@order_blueprint.route('/return-car', methods=['POST'])
def return_vehicle():
    if request.is_json:
        data = request.get_json()
        result = Order.return_car(data['customer_id'], data['car_id'])
        
        if "Error" in result:
            return jsonify(result), 400 
        else:
            return jsonify(result), 200 
    
    return jsonify({"Error": "Request must be JSON"}), 415

