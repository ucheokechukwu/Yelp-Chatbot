![Screenshot](images/Screenshot.png)

                This chatbot interfaces with a
                [LangChain](https://python.langchain.com/docs/get_started/introduction)
                agent designed to answer questions about a subset of users, businesses, 
                and reviews on [Yelp](https://www.yelp.com/). Dataset provided by [Yelp](https://www.yelp.com/dataset).
                The agent uses  retrieval-augment generation (RAG) over both
                structured and unstructured data. Data is hosted by [Neo4js](https://neo4j.com/) Graph Database Management System.


**To Do**:
1. Integrate `trip_time.py` with the `yelp_cypher_chain.py` to enhance query selection.
2. Deploy on streamlit community cloud
3. Fix integer type bug in `yelp_cypher_chain`
4. Scaling up data (< 10% total data currently deployed due to github file size limitations.) 