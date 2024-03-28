import os
from typing import Any
import numpy as np
from langchain_community.graphs import Neo4jGraph
from pandas import Series

def _get_current_businesses() -> list[str]:
    """Fetch a list of current business names from a Neo4j database."""
    graph = Neo4jGraph(
        url=os.getenv("NEO4J_URI"),
        username=os.getenv("NEO4J_USERNAME"),
        password=os.getenv("NEO4J_PASSWORD"),
        )

    current_businesses = graph.query(
        """
        MATCH (b:Business)
        RETURN b.name AS name, 
            b.address as address, 
            b.city as city,
            b.state as state,
            b.postal_code as postal_code 
        """
    )
    
    return current_businesses
    
def get_trip_time(start_location: str, business: str) -> (float, str):
    pass
    return None # placeholder for trip_time in seconds
    
def get_nearest_business(start_location: str, current_businesses: Series) -> dict[str, float]:
    pass
    return None # placeholder for dictionary of business_name, trip_time