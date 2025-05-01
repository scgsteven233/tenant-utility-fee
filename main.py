from fastapi import FastAPI
from pydantic import BaseModel, Field
from typing import List, Dict, Any
from calculator import calculate_cross_month_fees
import uvicorn
import os

# ----- Pydantic 輸入模型 ----- #
class Bill(BaseModel):
    month: str                    = Field(..., pattern=r"^\d{4}-\d{2}$", description="月份，格式 YYYY-MM")
    water_fee: float              = Field(..., ge=0, description="本月水費 💧")
    electricity_fee: float        = Field(..., ge=0, description="本月電費 ⚡")
    internet_fee: float           = Field(..., ge=0, description="本月網路費 🌐")

class Tenant(BaseModel):
    name: str
    move_in: str                  = Field(..., pattern=r"^\d{4}-\d{2}-\d{2}$", description="入住日期，格式 YYYY-MM-DD")
    move_out: str                 = Field(..., pattern=r"^\d{4}-\d{2}-\d{2}$", description="遷出日期，格式 YYYY-MM-DD")

class CrossMonthRequest(BaseModel):
    bills: List[Bill]
    tenants: List[Tenant]

# ----- FastAPI App ----- #
app = FastAPI()

@app.post("/api/cross-month", response_model=Dict[str, Any])
async def cross_month(req: CrossMonthRequest):
    """
    跨月費用計算
    - per_day_costs: 每月各項人/日單價
    - tenant_monthly_fees: 每位租客每月分項費用
    - tenant_total: 每位租客總費用
    """
    data = req.model_dump()  # 使用 Pydantic v2 的 model_dump()
    result = calculate_cross_month_fees(data)
    return result

# ----- 啟動 ----- #
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("main:app", host="0.0.0.0", port=port)
