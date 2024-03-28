import os
from langchain_openai import ChatOpenAI
from langchain.agents import (
    create_openai_functions_agent,
    Tool,
    AgentExecutor,)
    
from tools.trip_times import get_trip_time, get_nearest_business
# from chains.yelp_review_chain import reviews_vector_chain
# from chains.yelp_cypher_chain import yelp_cypher_chain

YELP_AGENT_MODEL = os.getenv("YELP_AGENT_MODEL")

from langchain import hub
prompt = hub.pull("hwchase17/openai-functions-agent")
