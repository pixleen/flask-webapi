from database_neo4j import db_session
from model.utils import node_to_dict


class Order:
    @staticmethod
    def order_vehicle(customer_id, car_id):
        with db_session() as session:
            session.run(
                "MATCH (customer:Customer) WHERE id(customer) = $customer_id "
                "MATCH (vehicle:Vehicle) WHERE id(vehicle) = $car_id AND vehicle.status = 'available' "
                "MERGE (customer)-[:BOOKED]->(vehicle) "
                "SET vehicle.status = 'booked'",
                customer_id=customer_id, car_id=car_id
            )

    @staticmethod
    def retrieve_all():
        with db_session() as session:
            result = session.run("""
                MATCH (order:Order)-[:FOR_CUSTOMER]->(customer:Customer)
                      -[:WITH_VEHICLE]->(vehicle:Vehicle)
                RETURN ID(order) as order_id, ID(customer) as customer_id, ID(vehicle) as vehicle_id, order.status as status
                """)
            return [{
                'id': record['order_id'],
                'customer_id': record['customer_id'],
                'vehicle_id': record['vehicle_id'],
                'status': record['status']
            } for record in result]

    @staticmethod
    def cancel_order_vehicle(customer_id, vehicle_id):
        with db_session() as session:
            session.run(
                "MATCH (customer:Customer)-[r:BOOKED]->(vehicle:Vehicle) WHERE id(customer) = $customer_id AND id(vehicle) = $vehicle_id "
                "DELETE r "
                "SET vehicle.status = 'available'",
                customer_id=customer_id, vehicle_id=vehicle_id
            )

    @staticmethod
    def rent_car(customer_id, vehicle_id):
        with db_session() as session:
            session.run(
                "MATCH (customer:Customer)-[:BOOKED]->(vehicle:Vehicle) WHERE id(customer) = $customer_id AND id(car) = $vehicle_id "
                "SET vehicle.status = 'rented'",
                customer_id=customer_id, vehicle_id=vehicle_id
            )

    @staticmethod
    def return_car(customer_id, vehicle_id, status):
        with db_session() as session:
            tx = session.start_transaction()
            try:
                # Match the booking relationship
                result = tx.run(
                    """
                    MATCH (customer:Customer)-[booking:BOOKED]->(car:Car)
                    WHERE id(customer) = $customer_id AND id(car) = $car_id
                    SET car.status = $status
                    DELETE booking  // Correct keyword to delete the relationship
                    RETURN car
                    """,
                    customer_id=customer_id, car_id=vehicle_id, status=status
                )
                vehicle = result.single()[0]

                tx.commit()
                return vehicle
            except Exception as e:
                
                tx.rollback()
                raise e