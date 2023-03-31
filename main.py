from routes import users, data
from fastapi import FastAPI
from fastapi.middleware import Middleware
from fastapi.middleware.cors import CORSMiddleware


origins = ["*"]
middleware = [
    Middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
]


app = FastAPI(middleware=middleware)


@app.get("/")
def home():
    return "Alephius API"


app.include_router(users.router)
app.include_router(data.router)
