from motor.motor_asyncio import AsyncIOMotorClient
from pymongo.server_api import ServerApi
from fastapi import FastAPI
from pymongo import MongoClient
from config.config import Settings
from beanie import init_beanie
from mongomock_motor import AsyncMongoMockClient


# models


documents = []


def init_db(app: FastAPI, mock_data=False):

    async def startup_db():
        print("Starting up")
        # Create a new client and connect to the server

        client = (
            AsyncMongoMockClient()
            if Settings().TESTING
            else AsyncIOMotorClient(Settings().MONGODB_URL, server_api=ServerApi("1"))
        )

        app.mongodb_client = client
        # Send a ping to confirm a successful connection
        database = client[Settings().DATABASE_NAME]
        try:
            await init_beanie(database=database, document_models=documents)
            client.admin.command("ping")
            print("You successfully connected to Database!")
        except Exception as e:
            print(e)
            print("Database Not Connected!")

    async def shutdown_db():
        print("Shutting down")
        app.mongodb_client.close()
        print("Connection to Database Closed!")

    app.add_event_handler("startup", startup_db)
    app.add_event_handler("shutdown", shutdown_db)
