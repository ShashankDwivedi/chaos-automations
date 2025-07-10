# The purpose of this code is to provide the Python client example to fetch data from ELK using Elastic Search
from elasticsearch import Elasticsearch

# Connect to Elasticsearch
es = Elasticsearch(
    hosts=["http://localhost:9200"],  # Replace with your ELK host
    http_auth=("username", "password"),  # Optional, if authentication is enabled
    verify_certs=False  # Set True if using HTTPS with valid certs
)

# Define the index and query
index_name = "your-index-name"

query = {
    "query": {
        "match": {
            "message": "error"
        }
    }
}

# Execute the search
response = es.search(index=index_name, body=query)

# Print the results
for hit in response['hits']['hits']:
    print(hit['_source'])
