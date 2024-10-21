from database_neo4j import db_session
from .utils import node_to_dict_2  # Import the utility function

class Car:
    @staticmethod
    def create_from_json(json_data):
        with db_session() as session:
            result = session.run(
                """
                CREATE (car:Car {make: $make, model: $model, year: $year, location: $location, status: 'available'})
                RETURN car
                """,
                **json_data
            )
            node = result.single()[0]  # Get the Node object from the result
            return node_to_dict_2(node)  # Convert it to a dictionary using the helper function

    @staticmethod
    def get_all():
        with db_session() as session:
            result = session.run("MATCH (car:Car) RETURN car, ID(car) as id")
            return [dict(node_to_dict_2(record['car']), id=record['id']) for record in result]

    @staticmethod
    def update(car_id, json_data):
        with db_session() as session:
            session.run(
                "MATCH (car:Car) WHERE id(car) = $car_id SET car += $properties",
                car_id=car_id, properties=json_data
            )

    @staticmethod
    def delete(car_id):
        with db_session() as session:
            session.run("MATCH (car:Car) WHERE id(car) = $car_id DETACH DELETE car", car_id=car_id)

    def to_dict(self):
        return dict(self)