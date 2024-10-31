from database_neo4j import db_session
from .utils import node_to_dict_2  

class Vehicle:
    @staticmethod
    def generate_from_json(json_data):
        # Ensure required fields are present in the incoming JSON
        required_fields = ['make', 'model', 'year', 'location']
        if not all(field in json_data for field in required_fields):
            raise ValueError("Missing required fields in the input data")

        with db_session() as session:
            result = session.run(
                """
                CREATE (car:Car {make: $make, model: $model, year: $year, location: $location, status: 'available'})
                RETURN car
                """,
                make=json_data['make'],
                model=json_data['model'],
                year=json_data['year'],
                location=json_data['location']
            )
            node = result.single()[0] 
            return node_to_dict_2(node)  

    @staticmethod
    def retrieve_all():
        with db_session() as session:
            # Ensure we are using the correct node label
            result = session.run("MATCH (vehicle:Car) RETURN vehicle, ID(vehicle) as id") 
            vehicles = [dict(node_to_dict_2(record['vehicle']), id=record['id']) for record in result]
            # Debugging output to verify retrieved vehicles
            print("Retrieved vehicles:", vehicles)
            return vehicles

    @staticmethod
    def update(vehicle_id, json_data):
        with db_session() as session:
            # Use the correct node label ('Car' instead of 'Vehicle')
            session.run(
                "MATCH (vehicle:Car) WHERE id(vehicle) = $car_id SET vehicle += $properties",
                car_id=vehicle_id, properties=json_data
            )

    @staticmethod
    def delete(vehicle_id):
        with db_session() as session:
            # Ensure the correct label is used when deleting
            session.run("MATCH (vehicle:Car) WHERE id(vehicle) = $car_id DETACH DELETE vehicle", car_id=vehicle_id)

    def to_dict(self):
        return dict(self)