from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from calculator import BillCalculator
import os

app = FastAPI()

# 根目錄回傳歡迎訊息
@app.get("/")
def read_root():
    return {"message": "Tenant Utility Fee API is running"}

# 計算 API，加上基本驗證
@app.post("/calculate")
async def calculate_bill(request: Request):
    try:
        data = await request.json()
        bill_data = data.get("bill")
        tenant_data = data.get("tenant")

        if not isinstance(bill_data, list) or not isinstance(tenant_data, list):
            return JSONResponse(status_code=400, content={"error": "Invalid input format: 'bill' and 'tenant' must be lists."})

        # 計算
        calculator = BillCalculator(bill_data, tenant_data)
        result = calculator.calculate()

        # 加入縮排格式
        return JSONResponse(
            content=jsonable_encoder(result),  # 格式化結果
            media_type="application/json",
            status_code=200
        )

    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})

# 讓程式可以本地或在 Render 上直接執行
if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))  # Render 會提供 PORT 環境變數
    uvicorn.run("main:app", host="0.0.0.0", port=port)
