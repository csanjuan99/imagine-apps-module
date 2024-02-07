from fastapi import FastAPI
from controllers import AuthController, TaskController
from fastapi.middleware.cors import CORSMiddleware
import models

app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:5173",
    "http://localhost:8080",
    "http://127.0.0.1:8080",
    "http://imagine-apps.com.s3-website-us-east-1.amazonaws.com"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

models.__init__()


@app.get("/")
def read_root():
    return {"Hello": "World"}


app.include_router(AuthController.router)
app.include_router(TaskController.router)
