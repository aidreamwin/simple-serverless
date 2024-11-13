# simple-serverless

超级轻量级的python serverless，用于开发超轻量级的应用

## 快速开始

### 启动程序
```bash
python main.py
```

### 添加一个函数

`functions/add.py`
```python
# functions/add.py
from fastapi.responses import JSONResponse
from fastapi import Request

def run(request: Request):
    a = int(request.query_params.get("a", 0))
    b = int(request.query_params.get("b", 0))
    return JSONResponse(content={"result": a + b})

```

### 请求函数

浏览器访问：`http://127.0.0.1:36000/func/add?a=1&b=2`

或者使用curl访问
```bash
curl http://127.0.0.1:36000/func/add?a=1&b=2
```

## API

### 查看函数列表
```bash
curl 'http://127.0.0.1:36000/functions' \
  -H 'X-API-Key: your_secret_api_key' \
  --compressed
```

## 说明

### 路由

`functions`下的每一个文件都会自动路由成`http://127.0.0.1:36000/func/[filename]`。
如`functions/add.py`访问的路由为`/func/add`

```
functions/add.py --> /func/add
functions/greet.py --> /func/greet
```

### 入口

每个文件都需要实现一个`def run(request: Request):`方法，函数的必要入口