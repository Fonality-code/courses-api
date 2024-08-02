from config.config import Settings
from fastapi.middleware.cors import CORSMiddleware
from fastapi_versioning import VersionedFastAPI
from fastapi import FastAPI
import asyncio


from database.mongod import init_db
from routes import init_router


def init_app():

    app_ = FastAPI(
        title=Settings().APP_NAME,
        version=Settings().APP_VERSION,
        description=Settings().APP_DESCRIPTION,
    )
    # Await the async init_db function
    init_db(app_)
    init_router(app_)

    app_ = VersionedFastAPI(
        app_, enable_latest=True, version_format="{major}", prefix_format="/v{major}"
    )

    app_.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_methods=["*"],
        allow_headers=["*"],
        allow_credentials=True,
    )

    @app_.get("/healthcheck", status_code=200)
    def api_healthcheck():
        return "OK 200 - app running successfully"

    return app_


# # register routers
# app.include_router(course.router)


app = init_app()
