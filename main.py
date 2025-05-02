from fastapi import FastAPI, Request
from calculator import BillCalculator
import os

app = FastAPI()

@app.post("/calculate")
async def calculate_bill(request: Request):
    data = await request.json()
    bill_data = data.get("bill", [])
    tenant_data = data.get("tenant", [])
    calculator = BillCalculator(bill_data, tenant_data)
    result = calculator.calculate()
    return result

# ✅ 讓程式可以在本地或 Render 上執行 🚦
if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))  # Render 會提供 PORT 環境變數
    uvicorn.run("main:app", host="0.0.0.0", port=port)
