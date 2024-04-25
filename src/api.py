from fastapi import FastAPI, Body
from pydantic import BaseModel

company_db = [
    {"ticker": "AAPL", "name": "Apple", "website": "www.apple.com"},
    {"ticker": "MSFT", "name": "Microsoft", "website": "www.microsoft.com"},
    {"ticker": "AMZN", "name": "Amazon", "website": "www.amazon.com"},
]

app = FastAPI()


class Company(BaseModel):
    ticker: str
    name: str
    website: str


@app.get("/")
def root():
    return {"company": "app"}


@app.get("/companies/")
def get_companies():
    return company_db


@app.get("/companies/{ticker}")
def get_company_by_ticker(ticker: str):
    for item in company_db:
        if item["ticker"] == ticker:
            return item


# Alternative way to send request body without Pydantic model
# @app.post("/companies/")
# def add_company(
#     ticker: str = Body(), name: str = Body(), website: str = Body()
# ):
#     new_company = {}
#     new_company["ticker"] = ticker
#     new_company["name"] = name
#     new_company["website"] = website
#     company_db.append(new_company)
#     return new_company


@app.post("/companies/")
def add_company(company: Company):
    added_company = company.dict()
    company_db.append(added_company)
    return added_company


@app.put("/companies/{ticker}")
def update_company_by_ticker(ticker: str, company: Company):
    updated_company = company.dict()
    for n, item in enumerate(company_db):
        if item["ticker"] == ticker:
            company_db[n] = updated_company
            return updated_company


@app.delete("/companies/{ticker}")
def delete_company_by_ticker(ticker: str):
    for n, item in enumerate(company_db):
        if item["ticker"] == ticker:
            deleted_company = company_db.pop(n)
            return deleted_company