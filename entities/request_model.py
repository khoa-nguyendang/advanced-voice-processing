from fastapi import FastAPI
from pydantic import BaseModel

class RequestModel(BaseModel):
    text: str
    speaker: str | None = None