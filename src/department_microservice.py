from fastapi import FastAPI, Body
from pydantic import BaseModel
from contextlib import asynccontextmanager
from azure.cosmos import CosmosClient, PartitionKey
import logging
import logging.config
import json
import requests
import db
import os
import data

requests.packages.urllib3.disable_warnings()  # for local dev only to disable warnings for the cosmosdb emulator self-signed cert. NEVER do this in production

logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Connect to cosmos and setup the database and containers
    logger.info("Connecting to Cosmos Instance")
    
    try:
        client = db.get_db_client()
    except KeyError as error:
        raise Exception(f"CosmosDB Environment Variables missing: {error}")

    logger.info("Creating database")
    database = client.create_database_if_not_exists(id=db.DB_NAME, offer_throughput=400)

    partition_key_path = PartitionKey(path="/id")
    container = database.create_container_if_not_exists(
        id=db.DEPARTMENT_CONTAINER,
        partition_key=partition_key_path,
    )

    for company in data.companies:
        for department in company["departments"]:
            logger.info(
                f"Upserting data for department: {department['name']} for company: {company['name']}"
            )
            department["company_id"] = company["id"]
            container.upsert_item(department)
    yield


app = FastAPI(lifespan=lifespan, debug=True)


@app.get("/departments")
async def departments(company_id: str | None = None):
    database = db.get_db_client().get_database_client(db.DB_NAME)
    if company_id is None:
        logger.info("Getting list of all departments")
        departments = list(
            database.get_container_client(db.DEPARTMENT_CONTAINER).read_all_items()
        )

        return json.dumps(departments)
    else:
        logger.info(f"Getting list of departments for company: {company_id}")
        departments = list(
            database.get_container_client(db.DEPARTMENT_CONTAINER).query_items(
                query="SELECT * FROM d WHERE d.company_id=@company_id",
                parameters=[{"name": "@company_id", "value": company_id}],
                enable_cross_partition_query=True,
            )
        )
        return json.dumps(departments)


@app.get("/department/{id}")
async def get_department_by_id(id: str):
    logger.info("Get company by Id")

    database = db.get_db_client().get_database_client(db.DB_NAME)

    department = database.get_container_client(db.DEPARTMENT_CONTAINER).read_item(
        id, partition_key=id
    )

    return department
