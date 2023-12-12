from fastapi import FastAPI
from uvicorn import run

from endpoints.auth import router

app = FastAPI()

app.include_router(router)


if __name__ == "__main__":
    run(app, host="0.0.0.0", port=8086)
