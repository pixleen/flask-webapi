from flask import Blueprint, request, jsonify, render_template, url_for
from werkzeug.utils import redirect

from models.customer import Customer

customer_blueprint = Blueprint('customer_blueprint', __name__)

@customer_blueprint.route('/', methods=['POST'])
def create_customer():
    if request.is_json:
        customer_data = request.get_json()
        customer = Customer.create_from_json(customer_data)
        # Check if the client accepts HTML responses
        if 'text/html' in request.accept_mimetypes:
            return redirect(url_for('customer_blueprint.get_customers'))
        else:
            # Return JSON response for API clients
            return jsonify(customer), 201
    else:
        return jsonify({"error": "Request must be JSON"}), 415


@customer_blueprint.route('/', methods=['GET'])
def get_customers():
    customers = Customer.get_all()
    return render_template('customers.html', customers=customers)

@customer_blueprint.route('/<int:customer_id>', methods=['PUT'])
def update_customer(customer_id):
    if request.is_json:
        Customer.update(customer_id, request.get_json())
        return jsonify({"success": "Customer updated successfully"}), 200
    return jsonify({"error": "Request must be JSON"}), 415

@customer_blueprint.route('/<int:customer_id>', methods=['DELETE'])
def delete_customer(customer_id):
    Customer.delete(customer_id)
    return jsonify({"success": "Customer deleted successfully"}), 200

