from neo4j import GraphDatabase


driver = GraphDatabase.driver("neo4j+s://6f5270e8.databases.neo4j.io", auth=("zRaR1f3SAqAMIgBAVJ9Th3z5u_1wLiZjAoan2arpmrA"))



def db_session():
    return driver.session()

def close_db():
    driver.close()
    
    



