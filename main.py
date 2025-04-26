from fastapi import FastAPI, Request
from calculator import calculate_fees
import uvicorn
import os

app = FastAPI()

@app.post("/api/calculate")
async def calculate(request: Request):
    data = await request.json()
    result = calculate_fees(data)
    return result

# 加這段，讓程式可以直接 run 起來
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))  # Render 會給 PORT，不然預設 8000
    uvicorn.run("main:app", host="0.0.0.0", port=port)
