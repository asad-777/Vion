from fastapi import FastAPI #type: ignore
from fastapi.middleware.cors import CORSMiddleware #type: ignore
import time

app = FastAPI()

origins = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
      "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"Hello": "World is ours"}


@app.get("/input/{text}")
def input(text):
    time.sleep(3)
    return {"You sent": text}