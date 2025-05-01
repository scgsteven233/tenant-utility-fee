from fastapi import FastAPI, Request
from pydantic import BaseModel, Field
from typing import List
from calculator import calculate_fees
import uvicorn
import os

# 建立資料模型，讓 FastAPI 幫我們驗證輸入資料 🧱
class Tenant(BaseModel):
    name: str
    move_in: str  # 日期格式預期為 "YYYY-MM-DD" 或包含時間的 ISO 格式
    move_out: str

class CalculationRequest(BaseModel):
    month_start: str  # "YYYY-MM-DD"
    month_end: str
    water_fee: float = Field(..., ge=0, description="本月水費 💧")
    internet_fee: float = Field(..., ge=0, description="本月網路費 🌐")
    electricity_fee: float = Field(..., ge=0, description="本月電費 ⚡")
    tenants: List[Tenant]

app = FastAPI()

@app.post("/api/calculate")
async def calculate(payload: CalculationRequest):
    try:
        # 轉為 dict 傳進 calculator 模組 🚀
        result = calculate_fees(payload.dict())
        return result
    except Exception as e:
        # 捕捉其他非驗證錯誤 🐞
        return {"error": str(e)}

# 讓程式可以本地或在 Render 上直接執行 🚦
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))  # Render 會給 PORT，不然預設 8000
    uvicorn.run("main:app", host="0.0.0.0", port=port)
