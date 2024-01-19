from typing import Union
from fastapi import FastAPI
from pymongo import MongoClient
from dbconfig.dbconfig import conn
from routes.routes import route

app = FastAPI()
app.include_router(route)