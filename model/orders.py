from database_neo4j import db_session
from model.utils import node_to_dict, node_to_dict_2

class Order:
    @staticmethod
    def order_vehicle(customer_id, car_id):
        with db_session() as session:
            # Check car availability
            availability_check = session.run(
                """
                MATCH (car:Car)
                WHERE id(car) = $car_id
                RETURN car.status AS car_status
                """,
                car_id=car_id
            )
            
            car_status_record = availability_check.single()

            # Check if the car is available
            if car_status_record and car_status_record["car_status"] != "available":
                return {"Error": "Car is not available for booking"}
            
            # Create order if car is available
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
                RETURN ID(order) as internal_order_id, 
                    ID(customer) as customer_id, ID(car) as car_id, 
                    order.status as status, car.status as car_status
            """)
            
            return [{
                'internal_order_id': record['internal_order_id'],                    
                'customer_id': record['customer_id'],
                'car_id': record['car_id'],
                'status': record['status'],
                'car_status': record['car_status']
            } for record in result]



    @staticmethod
    def cancel_order_vehicle(customer_id, car_id):
        with db_session() as session:
            result = session.run(
                """
                MATCH (customer:Customer)-[:PLACED]->(order:Order)-[:FOR_CAR]->(car:Car)
                WHERE id(customer) = $customer_id AND id(car) = $car_id AND car.status <> 'available'
                DETACH DELETE order
                SET car.status = 'available'
                RETURN car.status as car_status
                """,
                customer_id=customer_id, car_id=car_id
            )

            record = result.single()

            if record:
                return {"Success": "Order canceled, car is now available"}
            else:
                return {"Error": "Cannot cancel order. The car is already available or has no active booking"}



    @staticmethod
    def rent_car(customer_id, car_id):
        with db_session() as session:
            # Check if there is a booked order for the specified car and customer
            order_check = session.run(
                """
                MATCH (customer:Customer)-[:PLACED]->(order:Order)-[:FOR_CAR]->(car:Car)
                WHERE id(customer) = $customer_id AND id(car) = $car_id AND order.status = 'booked' AND car.status = 'booked'
                RETURN order, car
                """,
                customer_id=customer_id, car_id=car_id
            )

            order_record = order_check.single()

            # No match, error
            if not order_record:
                return {"Error": "Car is not booked, so it cannot be rented"}

            # Set status in car and order nodes
            session.run(
                """
                MATCH (customer:Customer)-[:PLACED]->(order:Order)-[:FOR_CAR]->(car:Car)
                WHERE id(customer) = $customer_id AND id(car) = $car_id
                SET order.status = 'rented', car.status = 'rented'
                RETURN order, car
                """,
                customer_id=customer_id, car_id=car_id
            )

            return {"Success": "Car status updated to rented"}


    @staticmethod
    def return_car(customer_id, car_id):
        with db_session() as session:
            # Check if the car is currently rented
            rental_check = session.run(
                """
                MATCH (customer:Customer)-[:PLACED]->(order:Order)-[:FOR_CAR]->(car:Car)
                WHERE id(customer) = $customer_id AND id(car) = $car_id AND order.status = 'rented' AND car.status = 'rented'
                RETURN order, car
                """,
                customer_id=customer_id, car_id=car_id
            )

            rental_record = rental_check.single()

            # If no matching rental order is found, return an error message
            if not rental_record:
                return {"Error": "Car is not rented, so it cannot be returned"}

            # Update the car status to 'available' and detach delete the order
            deletion_result = session.run(
                """
                MATCH (customer:Customer)-[:PLACED]->(order:Order)-[:FOR_CAR]->(car:Car)
                WHERE id(customer) = $customer_id AND id(car) = $car_id
                SET car.status = 'available'
                DETACH DELETE order
                RETURN car, ID(car) as car_id, car.status as car_status
                """,
                customer_id=customer_id, car_id=car_id
            )

            deletion_record = deletion_result.single()

            if deletion_record:
                print("Order successfully deleted for car_id:", deletion_record["car_id"])
                return {"Success": "Car has been returned and is now available"}
            else:
                print("Failed to delete order or set car to available")
                return {"Error": "Failed to return car"}