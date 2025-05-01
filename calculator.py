from datetime import datetime

def parse_date(date_str):
    # 避免萬一某個欄位真的不是字串，導致 date_str[:10] 報錯
    if not isinstance(date_str, str):
        date_str = str(date_str)
    # 把 "2025-04-09T16:00:00.000Z" 變成 "2025-04-09"
    return datetime.strptime(date_str[:10], "%Y-%m-%d")

def calculate_fees(data):
    tenants = data["tenants"]  # list of {name, move_in, move_out}
    total_fee = data["total_fee"]
    start_date = parse_date(data["month_start"])
    end_date = parse_date(data["month_end"])
    total_days = (end_date - start_date).days + 1

    result = []
    total_lived_days = 0
    days_map = []

    for t in tenants:
        move_in = max(parse_date(t["move_in"]), start_date)
        move_out = min(parse_date(t["move_out"]), end_date)
        days = (move_out - move_in).days + 1
        days = max(days, 0)
        days_map.append(days)
        total_lived_days += days

    for i, t in enumerate(tenants):
        if total_lived_days == 0:
            fee = 0
        else:
            fee = round(total_fee * days_map[i] / total_lived_days, 2)
        result.append({"name": t["name"], "days": days_map[i], "fee": fee})

    return {"result": result}
