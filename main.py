from fastapi import FastAPI
from pydantic import BaseModel, Field
from typing import List, Dict, Any
from calculator import calculate_cross_month_fees
import uvicorn
import os

class Bill(BaseModel):
    month: str = Field(..., pattern=r"^\d{4}-\d{2}$")
    water_fee: float = Field(..., ge=0, description="水費 💧")
    electricity_fee: float = Field(..., ge=0, description="電費 ⚡")
    internet_fee: float = Field(..., ge=0, description="網路費 🌐")


class Tenant(BaseModel):
    name: str
    move_in: str                  = Field(..., regex=r"^\d{4}-\d{2}-\d{2}")
    move_out: str                 = Field(..., regex=r"^\d{4}-\d{2}-\d{2}")

class CrossMonthRequest(BaseModel):
    bills: List[Bill]
    tenants: List[Tenant]

app = FastAPI()

@app.post("/api/cross-month", response_model=Dict[str, Any])
async def cross_month(req: CrossMonthRequest):
    """
    跨月費用計算
    - per_day_costs: 每月各項人/日單價
    - tenant_monthly_fees: 每位租客每月分項費用
    - tenant_total: 每位租客總費用
    """
    data = req.model_dump()  # 改用 model_dump() 取代舊的 dict()
    result = calculate_cross_month_fees(data)
    return result

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("main:app", host="0.0.0.0", port=port)
