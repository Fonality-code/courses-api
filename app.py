from config.config import Settings
from fastapi.middleware.cors import CORSMiddleware
from fastapi_versioning import VersionedFastAPI
from fastapi import FastAPI, HTTPException, Request
from pydantic import ValidationError as PydanticValidationError
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError

from database.mongod import init_db


app = FastAPI(
    title=Settings().APP_NAME,
    version=Settings().APP_VERSION,
    description=Settings().APP_DESCRIPTION,
)


@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"error": exc.detail},
    )

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=422,
        content={
            "error": "Validation error",
            "details": exc.errors()
        }
    )




app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True
)



async def startup():
    print("Starting up")
    await init_db()


app.add_event_handler("startup", startup)

@app.get('/')
def index():
    return {
        "API": {
            "version": Settings().APP_VERSION,
            "description": Settings().APP_DESCRIPTION
        }
    }


@app.get("/healthcheck")
def api_healthcheck():
    return "OK 200 - app running successfully"


app = VersionedFastAPI(app, enable_latest=True, version_format='{major}',
    prefix_format='/v{major}')

