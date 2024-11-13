
import os
import importlib
from fastapi import FastAPI, Request, Depends, HTTPException
from fastapi.responses import JSONResponse
from datetime import datetime
from fastapi.security import APIKeyHeader

app = FastAPI()

# 使用有序字典来存储函数和创建时间
functions = {}
function_creation_times = {}

# API Key Header
API_KEY = "your_secret_api_key"  # 替换为你的 API 密钥
api_key_header = APIKeyHeader(name="X-API-Key")

# Token 验证依赖
async def verify_api_key(api_key: str = Depends(api_key_header)):
    if api_key != API_KEY:
        raise HTTPException(status_code=403, detail="Forbidden")

def load_functions():
    functions_dir = "functions"
    for filename in os.listdir(functions_dir):
        if filename.endswith(".py") and filename != "__init__.py":
            module_name = filename[:-3]  # 去掉 .py 后缀
            try:
                module = importlib.import_module(f"{functions_dir}.{module_name}")
                create_time =  datetime.fromtimestamp(os.path.getctime(f"{functions_dir}/{filename}")).isoformat()
                update_time =  datetime.fromtimestamp(os.path.getmtime(f"{functions_dir}/{filename}")).isoformat()
                # 保存函数run参数信息 module.run.__annotations__
                args = module.run.__code__.co_varnames
                functions[module_name] = dict(
                    module=module,
                    args=args,
                    create_time=create_time,
                    update_time=update_time
                )
                print(f"Loaded {module_name}")
            except Exception as e:
                print(f"Failed to load {module_name}: {e}")

load_functions()

@app.get("/functions", dependencies=[Depends(verify_api_key)])
async def list_functions():
    return {
        "functions": [
            {
                "name": name, 
                "args": functions[name]["args"], 
                "create_time": functions[name]["create_time"],
                "update_time": functions[name]["update_time"],
            }
            for name in functions
        ]
    }

@app.get("/func/{function_name}")
async def get_function(function_name: str, request: Request):
    if function_name not in functions:
        # 导入函数
        try:
            # 检测文件是否存在
            if not os.path.exists(f"functions/{function_name}.py"):
                return JSONResponse(content={"error": "Function not found"}, status_code=404)
            module = importlib.import_module(f"functions.{function_name}")
            create_time =  datetime.fromtimestamp(os.path.getctime(f"functions/{function_name}.py")).isoformat()
            update_time =  datetime.fromtimestamp(os.path.getmtime(f"functions/{function_name}.py")).isoformat()
            # 保存函数run参数信息 module.run.__annotations__
            args = module.run.__code__.co_varnames
            functions[function_name] = dict(
                module=module,
                args=args,
                create_time=create_time,
                update_time=update_time
            )
            print(f"Loaded {function_name}")
        except Exception as e:
            return JSONResponse(content={"error": f"Failed to load {function_name}"}, status_code=500)
    if function_name in functions:
        func = getattr(functions[function_name]["module"], "run", None)
        if callable(func):
            return func(request)
    
    return JSONResponse(content={"error": "Function not found"}, status_code=404)

@app.post("/func/{function_name}")
async def post_function(function_name: str, request: Request):
    if function_name not in functions:
        # 导入函数
        try:
            # 检测文件是否存在
            if not os.path.exists(f"functions/{function_name}.py"):
                return JSONResponse(content={"error": "Function not found"}, status_code=404)
            module = importlib.import_module(f"functions.{function_name}")
            create_time =  datetime.fromtimestamp(os.path.getctime(f"functions/{function_name}.py")).isoformat()
            update_time =  datetime.fromtimestamp(os.path.getmtime(f"functions/{function_name}.py")).isoformat()
            # 保存函数run参数信息 module.run.__annotations__
            args = module.run.__code__.co_varnames
            functions[function_name] = dict(
                module=module,
                args=args,
                create_time=create_time,
                update_time=update_time
            )
            print(f"Loaded {function_name}")
        except Exception as e:
            return JSONResponse(content={"error": f"Failed to load {function_name}"}, status_code=500)
    if function_name in functions:
        func = getattr(functions[function_name]["module"], "run", None)
        if callable(func):
            return func(request)
    
    return JSONResponse(content={"error": "Function not found"}, status_code=404)


if __name__ == "__main__":
    import uvicorn
    # 生产环境 uvicorn main:app --host 0.0.0.0 --port 36000
    uvicorn.run(app, host="127.0.0.1", port=36000)