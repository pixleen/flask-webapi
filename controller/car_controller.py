from flask import Blueprint, request, jsonify, render_template, url_for
from werkzeug.utils import redirect

from models.car import Car

car_blueprint = Blueprint('car_blueprint', __name__)

@car_blueprint.route('/create', methods=['POST'])
def create_car():
    # Handle JSON data for API requests
    if request.is_json:
        car_data = request.get_json()
        car = Car.create_from_json(car_data)
        return jsonify(car), 201  # car is already a dictionary, return it as JSON
    else:
        # Handle form data for form submissions
        car_data = request.form.to_dict()
        car = Car.create_from_json(car_data)  # Use the same method for form data
        return redirect(url_for('car_blueprint.get_cars'))


@car_blueprint.route('/', methods=['GET'])
def get_cars():
    cars = Car.get_all()
    return render_template('cars.html', cars=cars)

@car_blueprint.route('/<int:car_id>', methods=['PUT'])
def update_car(car_id):
    if request.is_json:
        Car.update(car_id, request.get_json())
        return jsonify({"success": "Car updated successfully"}), 200
    return jsonify({"error": "Request must be JSON"}), 415

@car_blueprint.route('/<int:car_id>', methods=['DELETE'])
def delete_car(car_id):
    Car.delete(car_id)
    return jsonify({"success": "Car deleted successfully"}), 200

