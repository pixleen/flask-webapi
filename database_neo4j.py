from neo4j import GraphDatabase, Driver, AsyncGraphDatabase, AsyncDriver
from neo4j.exceptions import ServiceUnavailable, AuthError, Neo4jError

# Connection setup
uri = "neo4j+ssc://6f5270e8.databases.neo4j.io"
user = "neo4j"
password = "zRaR1f3SAqAMIgBAVJ9Th3z5u_1wLiZjAoan2arpmrA"

# Initializing the driver
try:
    driver = GraphDatabase.driver(uri, auth=(user, password))
    # Optional connection test to verify immediately
    with driver.session() as session:
        session.run("RETURN 1")
    print("Connection established successfully.")
except AuthError:
    print("Authentication error: Check your username or password.")
except ServiceUnavailable:
    print("Service unavailable: Verify that Neo4j is running and accessible.")
except Neo4jError as e:
    print(f"Neo4j error: {e}")
except Exception as e:
    print(f"Unexpected error: {e}")

# Database session management functions
def db_session():
    try:
        return driver.session()
    except Exception as e:
        print(f"Error creating session: {e}")
        return None

def close_db():
    if driver:
        driver.close()
        print("Database connection closed.")



#from neo4j import GraphDatabase


#driver = GraphDatabase.driver("neo4j+s://6f5270e8.databases.neo4j.io", auth=("neo4j", "zRaR1f3SAqAMIgBAVJ9Th3z5u_1wLiZjAoan2arpmrA"))



#def db_session():
    return driver.session()

#def close_db():
 #   driver.close()
    
    



