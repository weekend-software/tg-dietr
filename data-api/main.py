import logging
import os
import sys
import yaml

from fastapi import FastAPI, HTTPException

from models.user import User
from models.metric import Metric

from helpers.user import UserHelper
from helpers.metric import MetricHelper

from influxdb_client import InfluxDBClient
from influxdb_client.client.write_api import SYNCHRONOUS

db_config_raw = os.environ.get("APP_DB_CONFIG")
try:
    db_config = yaml.load(db_config_raw, Loader=yaml.BaseLoader)
except Exception as e:
    logging.exception(f"Could not load config: {e}")
    sys.exit(1)

db_bucket = os.environ.get("APP_DB_BUCKET")

client = InfluxDBClient(**db_config)

db_write_api = client.write_api(write_options=SYNCHRONOUS)
db_query_api = client.query_api()

user_helper = UserHelper(query_api=db_query_api, write_api=db_write_api, bucket=db_bucket)
metric_helper = MetricHelper(query_api=db_query_api, write_api=db_write_api, bucket=db_bucket)

app = FastAPI()


@app.get("/")
async def root():
    return {"detail": "Hello World"}


@app.get("/health")
async def health():
    # TODO Implement
    return {"detail": "Hello World"}


@app.post("/users/register")
async def users_register(user: User):
    user_exists = user_helper.exists(user.id)

    if user_exists:
        user = user_helper.get(id=user.id)
        raise HTTPException(status_code=409, detail={"message": "User already exists", "user": user})

    user_helper.create_and_activate(id=user.id)

    return {
        "detail": "User created",
        "user": user,
    }


@app.get("/users/")
async def users_list():
    users = user_helper.list()

    # TODO Get count from DB
    users_count = len(list(users))

    return {"count": users_count, "users": users}


@app.get("/users/{user_id}")
async def users_get(user_id: int):
    user = user_helper.get(id=user_id)

    return {
        "user": user,
    }


@app.patch("/users/{user_id}/activate")
async def users_activate(user_id: int):
    user_helper.activate(id=user_id)

    user = user_helper.get(id=user_id)

    return {
        "detail": "User activated",
        "user": user,
    }


@app.patch("/users/{user_id}/deactivate")
async def users_deactivate(user_id: int):
    user_helper.deactivate(id=user_id)

    user = user_helper.get(id=user_id)

    return {
        "detail": "User deactivated",
        "user": user,
    }


@app.post("/users/{user_id}/metrics/")
async def users_add_metric(user_id: int, metric: Metric):
    metric_helper.write(user_id=user_id, metric=metric)

    return {
        "detail": "Metric added",
    }


@app.get("/users/{user_id}/metrics/")
async def users_list_metrics(user_id: int):
    metrics = metric_helper.list(user_id)
    metrics_count = len(metrics.keys())

    return {"count": metrics_count, "metrics": metrics}


@app.get("/users/{user_id}/metrics/{metric_name}")
async def users_get_metric_values(user_id: int, metric_name: str, limit: int = 30, offset: int = 0):
    values = metric_helper.get_values(user_id, metric_name, offset=offset, limit=limit)

    return {"user_id": user_id, "metric_name": metric_name, "values": values}
