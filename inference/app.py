from collections import defaultdict
from fastapi import Request, FastAPI
import os.path as osp
import pandas as pd
from pydantic import BaseModel
import sys
import uvicorn

sys.path.append(osp.dirname(osp.dirname(osp.abspath(__file__))))

from db.dbc import DataBaseConnection


app = FastAPI()

# we may want to dowload database or raw csv file from s3 bucket (can do it here wit boto)

# connect to the database
db_file = './db/test.db'
dbc = DataBaseConnection(db_file=db_file)

class QueryRequest(BaseModel):
    query: str

class MetaDataRequest(BaseModel):
    metric_codes: list[str] 


def run_query(payload: dict) -> dict:
    query = payload['query']
    try:
        result = dbc.query(query=query)
        return {'queryResult': str(result)}
    except Warning as e:
        return {'queryUnsucessful': str(e)}


def get_metadata(payload: dict) -> dict:
    metric_codes = payload['metric_codes']
    if len(metric_codes) < 1:
        return {'metadata': {}}
    
    # prepare the query string
    s = f"('{metric_codes[0]}'"
    for code in metric_codes:
        s += f",'{code}'"
    s += ")"
    query = f"SELECT metric.code, metric.description, value_definition.label, value_definition.type FROM metric JOIN value_definition ON metric.id=value_definition.metric_id WHERE metric.code IN {s};"
    try:
        result = dbc.query(query=query)
        result_df = defaultdict(list)
        cols = ['metric_code', 'metric_description', 'value_label', 'value_type']
        for r in result:
            for idx, c in enumerate(cols):
                result_df[c].append(r[idx])

        return {'metadata': result_df}
    except Warning as e:
        return {'metadataUnsucessful': str(e)}


@app.get('/')
async def home():
    return {"message": "Novisto Demo"}

@app.post("/query")
async def getsummary(user_request_in: QueryRequest):
    payload = {'query': user_request_in.query}
    response = run_query(payload)
    return response

@app.post("/getMetaData")
async def getsummary(user_request_in: MetaDataRequest):
    payload = {'metric_codes': user_request_in.metric_codes}
    response = get_metadata(payload)
    return response
