from fastapi import FastAPI, Request
from calculator import calculate_fees

app = FastAPI()

@app.post("/api/calculate")
async def calculate(request: Request):
    data = await request.json()
    result = calculate_fees(data)
    return result
