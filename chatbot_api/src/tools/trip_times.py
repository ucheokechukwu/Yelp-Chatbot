import os
from typing import Any
import numpy as np
from langchain_community.graphs import Neo4jGraph
import pandas as pd
from chatbot_api.src.tools import geodistance


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
    
    if type(business) == str:
        try:
            current_businesses = _get_current_businesses()
            b = current_businesses[current_businesses.name==business].iloc[0]
        except:
            return -1, f"{business} not found in the database."
    else:
        b = business
    business_location = ' '.join([b['address'], b['city'], b['state'], b['postal_code']])               
    return geodistance.main(start_location=start_location,
                            end_location=business_location)
                            
                            
def get_nearest_business(start_location: str) -> dict[str, [float, float]]:
    """Find the business with the shortest trip time."""
    current_businesses = _get_current_businesses()

    current_businesses["duration"], current_businesses["trip_time"] = zip(
                        *current_businesses.apply(
                        get_trip_time, axis=1, start_location=start_location))

    shortest_time_idx = current_businesses["duration"].idxmin()
    nearest_business = current_businesses['name'][shortest_time_idx]
    shortest_duration = current_businesses['duration'][shortest_time_idx]

    return {nearest_business: [shortest_duration]}