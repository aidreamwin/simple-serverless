# functions/add.py
from fastapi.responses import JSONResponse
from fastapi import Request

def run(request: Request):
    a = int(request.query_params.get("a", 0))
    b = int(request.query_params.get("b", 0))
    return JSONResponse(content={"result": a + b})
