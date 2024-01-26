from fastapi import FastAPI
from uvicorn import run

from endpoints.auth import router as auth_router
from endpoints.chat import router as chat_router

app = FastAPI()

app.include_router(auth_router)
app.include_router(chat_router)


if __name__ == "__main__":
    run(app, host="0.0.0.0", port=8086)
