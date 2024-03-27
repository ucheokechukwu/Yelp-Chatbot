import os
from langchain_community.graphs import Neo4jGraph
from langchain.chains import GraphCypherQAChain
from langchain.openai import ChatOpenAI
from langchain.prompts import PromptTemplate

YELP_CYPHER_MODEL=os.getenv("YELP_CYPHER_MODEL")
YELP_QA_MODEL=os.getenv("YELP_QA_MODEL")

graph = Neo4jGraph(
    url=os.getenv("NEO4J_URI"),
    username=os.getenv("NEO4J_USERNAME"),
    password=os.getenv("NEO4J_PASSWORD"),
)
graph.refresh_schema() # to sync recent changes

cypher_generation_template="""
Task:
Generate Cypher query for a Neo4j graph database.

Instructions:
Use only the provided relationship types and properties in the schema.
Do not use any other relationship types or properties that are not provided.

Schema:
{schema}

Note:
Do not include any explanations or apologies in yoru responses.
Do not respond to any quyestions that might ask anything other than for you to construct a Cypher statement.
Do not include an text except the generated Cypher statement.
Make sure that the direction of the relationship is corect in your queries.
Make sure you alias both entities and relationships properly.
Do not run any queries that would add to or delete from the database.
Make sure to alias all statements that follow as with statement (e.g. WITH b as b.stars as stars).
If you need to divide numbers make sure to filter the denominator to non-zero.

Examples:
# What department stores in Arizona are closed?
MATCH (b:Business) WHERE b.state='AZ' AND b.categories CONTAINS 'Department Stores' AND b.is_open="0"
RETURN b.name LIMIT 2

String category values:
Use abbreviations when filtering on state names (e.g. "Texas" is "TX", "Arizona" is "AZ", etc)
Make sure to use IS NULL or IS NOT NULL when analyzing missing properties
You must never include the statement "GROUP BY" in your query. 
Make sure to alias all statements that follow as with statement (e.g. WITH b as business, b.state as
state)
If you need to divide numbers, make sure to filter the denominator to be non zero.

The question is:
{question}
"""


"""