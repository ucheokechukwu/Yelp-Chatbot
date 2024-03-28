#!/bin/bash

# Run any setup steps or preprocessing tasks here
echo "Running ETL to move yelp data from csvs on github to Neo4j database..."

# Run the ETL script
python yelp_bulk_csv_write.py
