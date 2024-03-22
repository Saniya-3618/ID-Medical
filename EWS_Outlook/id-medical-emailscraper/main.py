import uvicorn
from fastapi import FastAPI
from typing import List
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime
from app.emailscrapper.route import sub_router
from fastapi.middleware.cors import CORSMiddleware
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


# app.include_router(sub_router,prefix='/user', tags=['user'])

app.include_router(sub_router)
if __name__ == "__main__":
    uvicorn.run("main:app", host='172.16.16.75', port=9001)