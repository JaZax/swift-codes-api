from fastapi import FastAPI
from fastapi.responses import JSONResponse
from app.routes import router

app = FastAPI()

app.include_router(router, prefix="/v1/swift-codes")
