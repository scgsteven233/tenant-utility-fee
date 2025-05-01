from datetime import datetime, timedelta
from collections import defaultdict
from typing import List, Dict


def parse_date(date_str: str) -> datetime:
    """將字串轉換成 datetime 物件，只取日期部分"""
    return datetime.strptime(date_str[:10], "%Y-%m-%d")


def parse_month(month_str: str) -> datetime:
    """將 YYYY-MM 轉為該月第一天的 datetime"""
    return datetime.strptime(month_str, "%Y-%m")


def month_range(start: datetime, end: datetime) -> List[str]:
    """回傳 start 到 end 的所有月份（YYYY-MM）"""
    months = []
    current = start.replace(day=1)
    while current <= end:
        months.append(current.strftime("%Y-%m"))
        if current.month == 12:
            current = current.replace(year=current.year + 1, month=1)
        else:
            current = current.replace(month=current.month + 1)
    return months


def calculate_cross_month_fees(data: Dict) -> Dict:
    bills = {bill["month"]: bill for bill in data["bills"]}
    tenants = data["tenants"]

    # Step 1: 建立所有月份的人日統計資料
    per_day_costs = {}
    month_days = defaultdict(list)  # 每月每人佔幾天

    all_move_in = min(parse_date(t["move_in"]) for t in tenants)
    all_move_out = max(parse_date(t["move_out"]) for t in tenants)
    months = month_range(all_move_in, all_move_out)

    for month in months:
        bill = bills.get(month)
        if bill:
            start = parse_month(month)
            if start.month == 12:
                end = start.replace(year=start.year + 1, month=1) - timedelta(days=1)
            else:
                end = start.replace(month=start.month + 1) - timedelta(days=1)

            # 計算每位房客該月的居住天數
            total_days = 0
            for t in tenants:
                move_in = parse_date(t["move_in"])
                move_out = parse_date(t["move_out"])
                lived_start = max(move_in, start)
                lived_end = min(move_out, end)
                days = (lived_end - lived_start).days + 1
                if days > 0:
                    month_days[month].append({"name": t["name"], "days": days})
                    total_days += days

            if total_days > 0:
                per_day_costs[month] = {
                    "water": bill["water_fee"] / total_days,
                    "electricity": bill["electricity_fee"] / total_days,
                    "internet": bill["internet_fee"] / total_days
                }

    # Step 2: 計算每人每月費用（估算未出帳月份）
    tenant_monthly_fees = defaultdict(list)
    tenant_total = defaultdict(float)

    prev_cost = None
    for month in months:
        daily = per_day_costs.get(month, prev_cost)
        if not daily:
            continue  # 沒有資料也無法估算

        prev_cost = daily  # 儲存目前或上一個有效單價

        for record in month_days.get(month, []):
            name = record["name"]
            days = record["days"]
            water = round(daily["water"] * days, 2)
            electricity = round(daily["electricity"] * days, 2)
            internet = round(daily["internet"] * days, 2)
            total = round(water + electricity + internet, 2)
            tenant_monthly_fees[name].append({
                "month": month,
                "days": days,
                "water": water,
                "electricity": electricity,
                "internet": internet,
                "total": total
            })
            tenant_total[name] += total

    return {
        "per_day_costs": per_day_costs,
        "tenant_monthly_fees": tenant_monthly_fees,
        "tenant_total": [{"name": name, "total": round(total, 2)} for name, total in tenant_total.items()]
    }
