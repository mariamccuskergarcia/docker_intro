from fastapi import FastAPI, Body
from pydantic import BaseModel
from contextlib import asynccontextmanager
from azure.cosmos import CosmosClient, PartitionKey
import logging
import logging.config
import json
import requests
import db
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
    database = client.create_database_if_not_exists(id=db.DB_NAME, offer_throughput=800)

    partition_key_path = PartitionKey(path="/id")
    container = database.create_container_if_not_exists(
        id=db.COMPANY_CONTAINER,
        partition_key=partition_key_path,
    )

    for company in data.companies:
        local_copy = company
        logger.info(f"Upserting data for company: {company['name']}")
        del local_copy["departments"]
        container.upsert_item(company)
    yield


app = FastAPI(lifespan=lifespan, debug=True)


@app.get("/db_info")
async def db_info():
    logger.info("Getting database properties")

    database = db.get_db_client().get_database_client(db.DB_NAME)

    properties = database.read()

    return {json.dumps(properties)}


@app.get("/companies")
async def get_companies():
    logger.info("Getting list of companies")

    database = db.get_db_client().get_database_client(db.DB_NAME)

    companies = list(
        database.get_container_client(db.COMPANY_CONTAINER).read_all_items()
    )

    return json.dumps(companies)


@app.get("/company/{id}")
async def get_company_by_id(id: str):
    logger.info("Get company by Id")

    database = db.get_db_client().get_database_client(db.DB_NAME)

    company = database.get_container_client(db.COMPANY_CONTAINER).read_item(
        id, partition_key=id
    )

    return company

@app.get("/healthz")
async def liveness_readiness():
    return {"Service up and running!"}
