# functions/greet.py
from fastapi.responses import JSONResponse
from fastapi import Request

def run(request: Request):
    name = request.query_params.get("name", "World")
    return JSONResponse(content={"message": f"Hello, {name}!"})
