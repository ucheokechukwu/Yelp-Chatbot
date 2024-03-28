import os
from typing import Any
import numpy as np
from langchain_community.graphs import Neo4jGraph
import pandas as pd
from chatbot_api.src.tools import geolocator


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
    
    return pd.DataFrame(current_businesses)
    
def get_trip_time(start_location: str, business: str) -> (float, str):
    """Get the current trip time to businesses from a given location in seconds."""
    
    current_businesses = _get_current_businesses()
    b = current_businesses[current_businesses.name==business].iloc[0]

    business_location = ' '.join([b['address'], b['city'], b['state'], b['postal_code']])                
    return geodistance.main(start_location=start_location,
                            end_location=business_location)
    
def get_nearest_business(start_location: str, current_businesses: pd.Series) -> dict[str, float]:
    pass
    return None # placeholder for dictionary of business_name, trip_time