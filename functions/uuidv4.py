# functions/uuidv4.py

from fastapi.responses import JSONResponse
from fastapi import Request

import uuid

def run(request: Request):
    return JSONResponse(content={"uuid": str(uuid.uuid4())})