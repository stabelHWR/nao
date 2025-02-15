from webserver.neo4j_connection import Neo4jConnection

def getDbConnection()->Neo4jConnection:
    connection = Neo4jConnection()
    connection.open()
    return connection