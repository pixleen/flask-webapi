from database_neo4j import db_session
from .utils import node_to_dict_2  

class Vehicle:
    @staticmethod
    def generate_from_json(json_data):
        with db_session() as session:
            result = session.run(
                """
                CREATE (car:Car {make: $make, model: $model, year: $year, location: $location, status: 'available'})
                RETURN car
                """,
                **json_data
            )
            node = result.single()[0] 
            return node_to_dict_2(node)  

    @staticmethod

    def retrieve_all():
        with db_session() as session:
        # Change 'Vehicle' to 'Car' if your node labels are indeed 'Car'
            result = session.run("MATCH (vehicle:Car) RETURN vehicle, ID(vehicle) as id") 
            vehicles = [dict(node_to_dict_2(record['vehicle']), id=record['id']) for record in result]
        # Debugging output to verify retrieved vehicles
        print("Retrieved vehicles:", vehicles)
        return vehicles
    
    
    # def retrieve_all():
    #     with db_session() as session:
    #         result = session.run("MATCH (vehicle:Vehicle) RETURN vehicle, ID(vehicle) as id") # HER LIGGER FEILEN(?)
    #         return [dict(node_to_dict_2(record['vehicle']), id=record['id']) for record in result]


    @staticmethod
    def update(vehicle_id, json_data):
        with db_session() as session:
            session.run(
                "MATCH (vehicle:Vehicle) WHERE id(vehicle) = $car_id SET car += $properties",
                car_id=vehicle_id, properties=json_data
            )

    @staticmethod
    def delete(vehicle_id):
        with db_session() as session:
            session.run("MATCH (vehicle:Vehicle) WHERE id(vehicle) = $car_id DETACH DELETE car", car_id=vehicle_id)

    def to_dict(self):
        return dict(self)