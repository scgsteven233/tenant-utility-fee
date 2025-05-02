from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from calculator import BillCalculator
import os

app = FastAPI()

# ✅ 根目錄回傳歡迎訊息（避免 404）
@app.get("/")
def read_root():
    return {"message": "Tenant Utility Fee API is running"}

# ✅ 計算 API，加上基本驗證
@app.post("/calculate")
async def calculate_bill(request: Request):
    try:
        data = await request.json()
        bill_data = data.get("bill")
        tenant_data = data.get("tenant")

        if not isinstance(bill_data, list) or not isinstance(tenant_data, list):
            return JSONResponse(status_code=400, content={"error": "Invalid input format: 'bill' and 'tenant' must be lists."})

        calculator = BillCalculator(bill_data, tenant_data)
        result = calculator.calculate()
        return result

    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})

# ✅ 支援 Render 本地/雲端啟動
if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("main:app", host="0.0.0.0", port=port)
