from database_neo4j import db_session
from model.utils import node_to_dict


class Order:
    @staticmethod
    def order_car(customer_id, car_id):
        with db_session() as session:
            session.run(
                "MATCH (customer:Customer) WHERE id(customer) = $customer_id "
                "MATCH (car:Car) WHERE id(car) = $car_id AND car.status = 'available' "
                "MERGE (customer)-[:BOOKED]->(car) "
                "SET car.status = 'booked'",
                customer_id=customer_id, car_id=car_id
            )

    @staticmethod
    def get_all():
        with db_session() as session:
            result = session.run("""
                MATCH (order:Order)-[:FOR_CUSTOMER]->(customer:Customer)
                      -[:WITH_CAR]->(car:Car)
                RETURN ID(order) as order_id, ID(customer) as customer_id, ID(car) as car_id, order.status as status
                """)
            return [{
                'id': record['order_id'],
                'customer_id': record['customer_id'],
                'car_id': record['car_id'],
                'status': record['status']
            } for record in result]

    @staticmethod
    def cancel_order_car(customer_id, car_id):
        with db_session() as session:
            session.run(
                "MATCH (customer:Customer)-[r:BOOKED]->(car:Car) WHERE id(customer) = $customer_id AND id(car) = $car_id "
                "DELETE r "
                "SET car.status = 'available'",
                customer_id=customer_id, car_id=car_id
            )

    @staticmethod
    def rent_car(customer_id, car_id):
        with db_session() as session:
            session.run(
                "MATCH (customer:Customer)-[:BOOKED]->(car:Car) WHERE id(customer) = $customer_id AND id(car) = $car_id "
                "SET car.status = 'rented'",
                customer_id=customer_id, car_id=car_id
            )

    @staticmethod
    def return_car(customer_id, car_id, status):
        with db_session() as session:
            # Begin transaction
            tx = session.begin_transaction()
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
                    customer_id=customer_id, car_id=car_id, status=status
                )
                car = result.single()[0]
                # Commit transaction
                tx.commit()
                return car
            except Exception as e:
                # Rollback transaction on error
                tx.rollback()
                raise e