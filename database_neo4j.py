from neo4j import GraphDatabase


driver = GraphDatabase.driver("neo4j+s://a673e1df.databases.neo4j.io:7687", 
                              auth=("neo4j", "danjon-3joBwy-dybwoz"))



def db_session():
    return driver.session()

def close_db():
    driver.close()
    
    



