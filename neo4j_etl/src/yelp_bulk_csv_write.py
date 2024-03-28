import os
import logging
from retry import retry
from neo4j import GraphDatabase

USERS_CSV_PATH = os.getenv("USERS_CSV_PATH")
BUSINESS_CSV_PATH = os.getenv("BUSINESS_CSV_PATH")
REVIEWS_CSV_PATH = os.getenv("REVIEWS_CSV_PATH")

NEO4J_URI = os.getenv("NEO4J_URI")
NEO4J_USERNAME = os.getenv("NEO4J_USERNAME")
NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD")

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s]: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

LOGGER = logging.getLogger(__name__)

NODES = ["User", "Business", "Review"]

def _set_uniqueness_constraints(tx, node):
    query = f"""CREATE CONSTRAINT IF NOT EXISTS FOR (n:{node})
        REQUIRE n.id IS UNIQUE;"""
    _ = tx.run(query, {})


@retry(tries=100, delay=10)
def load_yelp_graph_from_csv() -> None:
    """Load structured Yelp CSV data following
    a specific ontology into Neo4j"""

    driver = GraphDatabase.driver(
        NEO4J_URI, auth=(NEO4J_USERNAME, NEO4J_PASSWORD)
    )

    LOGGER.info("Setting uniqueness constraints on nodes")
    with driver.session(database="neo4j") as session:
        for node in NODES:
            session.execute_write(_set_uniqueness_constraints, node)

    LOGGER.info("Loading business nodes")
    with driver.session(database="neo4j") as session:
        query = f"""
        LOAD CSV WITH HEADERS
        FROM '{BUSINESS_CSV_PATH}' AS business
        MERGE (b:Business {{id: business.business_id,
                            name: business.name,
                            address: business.address,
                            city: business.city,
                            state: business.state,
                            postal_code: business.postal_code,
                            stars: business.stars,
                            hours: business.hours,
                            attributes: business.attributes,
                            categories: business.categories,
                            is_open: business.is_open}});
        """
        _ = session.run(query, {})

    LOGGER.info("Loading user nodes")
    with driver.session(database="neo4j") as session:
        query = f"""
        LOAD CSV WITH HEADERS
        FROM '{USERS_CSV_PATH}' AS user
        MERGE (u:User {{id: user.user_id,
                            name: user.name,
                            friends: user.friends,
                            fans: user.fans,
                            review_count: user.review_count}});
        """
        _ = session.run(query, {})    

    LOGGER.info("Loading review nodes")
    with driver.session(database="neo4j") as session:
        query = f"""
        LOAD CSV WITH HEADERS
        FROM '{REVIEWS_CSV_PATH}' AS reviews
        MERGE (r:Review {{id: reviews.review_id,
                         stars: reviews.stars,
                         text: reviews.text,
                         date: reviews.date}});
        """
        _ = session.run(query, {})

    LOGGER.info("Loading 'WRITES' relationships")
    with driver.session(database="neo4j") as session:
        query = f"""
        LOAD CSV WITH HEADERS FROM '{REVIEWS_CSV_PATH}' AS reviews
        MATCH (u:User {{id: reviews.user_id}})
        MATCH (r:Review {{id: reviews.review_id}})
        MERGE (u)-[writes:WRITES]->(r)
        """
        _ = session.run(query, {})
        
    LOGGER.info("Loading 'HAS' relationships")
    with driver.session(database="neo4j") as session:
        query = f"""
        LOAD CSV WITH HEADERS FROM '{REVIEWS_CSV_PATH}' AS reviews
        MATCH (r:Review {{id: reviews.review_id}})
        MATCH (b:Business {{id: reviews.business_id}})
        MERGE (b)-[has:HAS]->(r)
        """
        _ = session.run(query, {})

if __name__ == '__main__':
    load_yelp_graph_from_csv()    
