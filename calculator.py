from datetime import datetime, timedelta
from collections import defaultdict

def parse_date(date_str):
    """轉換日期字串為 datetime 物件，只取日期部分"""
    return datetime.strptime(date_str[:10], "%Y-%m-%d")

def calculate_fees(data):
    tenants = data["tenants"]
    month_start = parse_date(data["month_start"])
    month_end = parse_date(data["month_end"])
    water_fee = data["water_fee"]
    internet_fee = data["internet_fee"]
    electricity_fee = data["electricity_fee"]
    total_fee = water_fee + internet_fee + electricity_fee

    # 計算當月內每人實際居住天數
    total_lived_days = 0
    days_map = []
    for t in tenants:
        move_in = max(parse_date(t["move_in"]), month_start)
        move_out = min(parse_date(t["move_out"]), month_end)
        days = (move_out - move_in).days + 1
        days = max(days, 0)
        days_map.append(days)
        total_lived_days += days

    # 若本月總人日為 0，避免除以 0 錯誤
    per_day_fee = total_fee / total_lived_days if total_lived_days > 0 else 0

    results = []
    tenant_total_map = defaultdict(float)

    for i, t in enumerate(tenants):
        days = days_map[i]
        month_fee = round(per_day_fee * days, 2)
        results.append({
            "name": t["name"],
            "days": days,
            "fee": month_fee
        })
        tenant_total_map[t["name"]] += month_fee

    # ⭐ 額外：計算遷出前的總費用（跨月）
    # 根據前一月的人日單價估算未出帳月份
    prev_per_day_fee = per_day_fee  # 預估單價（若未來要查詢歷史紀錄可改進）

    for t in tenants:
        move_in = parse_date(t["move_in"])
        move_out = parse_date(t["move_out"])
        current = month_end + timedelta(days=1)
        while current <= move_out:
            start = current.replace(day=1)
            if current.month == 12:
                end = current.replace(year=current.year + 1, month=1, day=1) - timedelta(days=1)
            else:
                end = current.replace(month=current.month + 1, day=1) - timedelta(days=1)

            # 這個月居住的天數
            lived_start = max(move_in, start)
            lived_end = min(move_out, end)
            days = (lived_end - lived_start).days + 1
            days = max(days, 0)
            estimate = round(prev_per_day_fee * days, 2)
            tenant_total_map[t["name"]] += estimate
            current = end + timedelta(days=1)

    return {
        "month_result": results,
        "total_until_move_out": [
            {"name": name, "total_fee": round(fee, 2)} for name, fee in tenant_total_map.items()
        ]
    }
