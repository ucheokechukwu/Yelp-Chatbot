import os
from typing import Any
import numpy as np
from langchain_community.graphs import Neo4jGraph

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