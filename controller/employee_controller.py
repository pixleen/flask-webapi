from flask import Blueprint, request, jsonify, render_template
from model.employee import Employee

employee_blueprint = Blueprint('employee_blueprint', __name__)

@employee_blueprint.route('/create', methods=['POST'])
def generate_employee():
    if request.is_json:
        employee_info = request.get_json()
        employee = Employee.create_from_json(employee_info)
        return jsonify(employee), 201
    else:
        employee_info = request.form.to_dict()
        employee = Employee.create_from_json(employee_info)
    return jsonify({"Error": "Request must be JSON"}), 415

@employee_blueprint.route('/', methods=['GET'])
def retrieve_employees():
    employees = Employee.get_all()
    return render_template('employees.html', employees=employees)

@employee_blueprint.route('/<int:employee_id>', methods=['PUT'])
def update_employee(employee_id):
    if request.is_json:
        Employee.update(employee_id, request.get_json())
        return jsonify({"Success": "Employee updated"}), 200
    return jsonify({"error": "Request must be JSON"}), 415

@employee_blueprint.route('/<int:employee_id>', methods=['DELETE'])
def remove_employee(employee_id):
    Employee.remove(employee_id)
    return jsonify({"Success": "Employee deleted"}), 200

