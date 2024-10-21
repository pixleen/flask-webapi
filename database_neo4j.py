from neo4j import GraphDatabase


driver = GraphDatabase.driver("bolt://localhost:7687", auth=("neo4j", "danjon-3joBwy-dybwoz"))



def db_session():
    return driver.session()

def close_db():
    driver.close()
    
    



