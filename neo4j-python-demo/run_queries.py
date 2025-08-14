from neo4j import GraphDatabase
import logging
from neo4j.exceptions import ServiceUnavailable

# Define the connection details for our local Neo4j Docker container
URI = "neo4j://localhost:7687"
AUTH = ("neo4j", "password")

def run_query(session, query, message):
    """A reusable function to run a Cypher query and print the results."""
    print("---")
    print(message)
    print(query)
    print("---")
    
    result = session.run(query)
    
    count = 0
    for record in result:
        print(record.data())
        count += 1
    
    if count == 0:
        print("No records found.")
    
    print("\n")


def main():
    """The main function to connect to the database and run our custom queries."""
    
    # Define our custom Cypher queries
    query1 = """
    MATCH (p:Person {name: 'Rob Reiner'})-[:DIRECTED]->(m:Movie)
    RETURN p.name AS Director, m.title AS Movie
    """

    query2 = """
    MATCH (m:Movie {title: 'The Matrix Reloaded'})<-[:ACTED_IN]-(a:Person)
    RETURN a.name AS Actor
    """

    query3 = """
    MATCH (d:Person)-[:DIRECTED]->(m:Movie)
    RETURN d.name AS Director, COUNT(m) AS NumberOfMovies
    ORDER BY NumberOfMovies DESC
    LIMIT 5
    """

    query4 = """
    MATCH (actor:Person {name: 'Keanu Reeves'})-[:ACTED_IN]->(m:Movie)<-[:DIRECTED]-(director:Person)
    RETURN actor.name, m.title, director.name
    """

    query5_inception = """
    MATCH (m:Movie {title: 'Inception'})<-[:ACTED_IN]-(a:Person)
    RETURN a.name AS Actor
    """

    # Establish a connection to the database
    driver = GraphDatabase.driver(URI, auth=AUTH)

    try:
        # We use a session to run our queries
        with driver.session(database="neo4j") as session:
            
            # Run each of our custom queries using the reusable function
            run_query(session, query1, "Query 1: Find movies directed by Rob Reiner.")
            run_query(session, query2, "Query 2: Find actors in 'The Matrix Reloaded'.")
            run_query(session, query3, "Query 3: Find the top 5 most prolific directors.")
            run_query(session, query4, "Query 4: Find the directors of Keanu Reeves' movies.")
            run_query(session, query5_inception, "Query 5: Find the actors in 'Inception'.")

    except ServiceUnavailable as e:
        logging.error(f"Could not connect to Neo4j at {URI}. Is the database running?")
        print(f"Error: {e}")
    finally:
        if driver:
            driver.close()

if __name__ == "__main__":
    main()