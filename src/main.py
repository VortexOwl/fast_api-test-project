from api import main_router
from config import host

from fastapi import FastAPI
from uvicorn import run as uvicorn_run


app = FastAPI()
app.include_router(main_router)

if __name__ == "__main__":
    uvicorn_run("main:app", host=host, reload=True)
