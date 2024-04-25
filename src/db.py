from azure.cosmos import CosmosClient, PartitionKey
from dotenv import load_dotenv
import os
import requests

requests.packages.urllib3.disable_warnings()  # for local dev only to disable warnings for the cosmosdb emulator self-signed cert. NEVER do this in production
load_dotenv()

DB_NAME = "company_data"
COMPANY_CONTAINER = "company"
DEPARTMENT_CONTAINER = "department"

def get_db_client() -> CosmosClient:
    """Return the current"""
    if (os.getenv("COSMOSDB_ENDPOINT_URL") is None or os.getenv("COSMOSDB_MASTER_KEY") is None):
        raise KeyError("Environment Variables not set")
    
    client = CosmosClient(
        url=os.getenv("COSMOSDB_ENDPOINT_URL"),
        credential={"masterKey": os.getenv("COSMOSDB_MASTER_KEY")},
    )   

    return client
