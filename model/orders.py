from database_neo4j import db_session
from model.utils import node_to_dict


class Order:
    @staticmethod
    def order_vehicle(customer_id, car_id):
        with db_session() as session:
            result = session.run(
                """
                MATCH (customer:Customer) WHERE id(customer) = $customer_id
                MATCH (car:Car) WHERE id(car) = $car_id AND car.status = 'available'
                CREATE (order:Order {status: 'booked', created_at: datetime()})
                MERGE (customer)-[:PLACED]->(order)-[:FOR_CAR]->(car)
                SET car.status = 'booked'
                RETURN ID(order) as order_id, ID(customer) as customer_id, ID(car) as car_id, order.status as order_status, car.status as car_status
                """,
                customer_id=customer_id, car_id=car_id
            )
            
            record = result.single()
            
            if record:
                # Return order details as a dictionary if successfully created
                return {
                    'order_id': record['order_id'],
                    'customer_id': record['customer_id'],
                    'car_id': record['car_id'],
                    'order_status': record['order_status'],
                    'car_status': record['car_status']
                }
            
            return None



    @staticmethod
    def retrieve_all():
        with db_session() as session:
            result = session.run("""
                MATCH (customer:Customer)-[:PLACED]->(order:Order)-[:FOR_CAR]->(car:Car)
                RETURN ID(order) as order_id, ID(customer) as customer_id, ID(car) as car_id, order.status as status, car.status as car_status
            """)
            return [{
                'order_id': record['order_id'],
                'customer_id': record['customer_id'],
                'car_id': record['car_id'],
                'status': record['status'],
                'car_status': record['car_status']
            } for record in result]

    @staticmethod
    def cancel_order_vehicle(customer_id, vehicle_id):
        with db_session() as session:
            session.run(
                """
                MATCH (customer:Customer)-[:PLACED]->(order:Order)-[:FOR_VEHICLE]->(vehicle:Vehicle)
                WHERE id(customer) = $customer_id AND id(vehicle) = $vehicle_id
                DETACH DELETE order
                SET vehicle.status = 'available'
                """,
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