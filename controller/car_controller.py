from flask import Blueprint, request, jsonify, render_template, url_for
from werkzeug.utils import redirect

from model.vehicle import Vehicle

vehicle_blueprint = Blueprint('vehicle_blueprint', __name__)

@vehicle_blueprint.route('/create', methods=['POST'])
def generate_vehicle():
    if request.is_json:
        vehicle_data = request.get_json()
        vehicle = Vehicle.generate_from_json(vehicle_data)
        return jsonify(vehicle), 201  
    else:
        vehicle_data = request.form.to_dict()
        vehicle = Vehicle.generate_from_json(vehicle_data)  
        return redirect(url_for('vehicle_blueprint.get_vehicles'))


@vehicle_blueprint.route('/', methods=['GET'])
def generate_vehicles():
    vehicles = Vehicle.retrieve_all()
    return render_template('vehicles.html', vehicles=vehicles)


@vehicle_blueprint.route('/<int:vehicle_id>', methods=['PUT'])
def update_vehicle(vehicle_id):
    if request.is_json:
        Vehicle.update(vehicle_id, request.get_json())
        return jsonify({"success": "Vehicle updated successfully"}), 200
    return jsonify({"error": "Request must be JSON"}), 415


@vehicle_blueprint.route('/<int:vehicle_id>', methods=['DELETE'])
def delete_vehicle(vehicle_id):
    Vehicle.delete(vehicle_id)
    return jsonify({"success": "Vehicle deleted successfully"}), 200

