import os
import signal

import fastapi
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app import graceful_shutdown
from app.api.v1 import endpoint

graceful_shutdown.init()
app = FastAPI(title="FastAPI")


def shutdown():
    os.kill(os.getpid(), signal.SIGTERM)
    return fastapi.Response(status_code=200, content="Server shutting down...")


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(endpoint.router, prefix="/api/v1")


@app.get("/")
def read_root():
    return {"message": "Welcome to FastAPI!"}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080)
