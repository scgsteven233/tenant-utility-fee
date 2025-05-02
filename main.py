from fastapi import FastAPI, Request
from calculator import BillCalculator

app = FastAPI()

@app.post("/calculate")
async def calculate_bill(request: Request):
    data = await request.json()
    bill_data = data.get("bill", [])
    tenant_data = data.get("tenant", [])
    calculator = BillCalculator(bill_data, tenant_data)
    result = calculator.calculate()
    return result
