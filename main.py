from fastapi import FastAPI
from controllers import AuthController, TaskController
from fastapi.middleware.cors import CORSMiddleware
import models

app = FastAPI()

origins = [
    "*"
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
