from datetime import datetime, timedelta
from collections import defaultdict
import calendar
from dateutil import parser  # ⬅️ 新增

def parse_date_safe(date_str):
    """接受多種格式的日期字串並轉為 datetime 物件"""
    try:
        return datetime.strptime(date_str, "%Y/%m/%d")
    except ValueError:
        try:
            return parser.parse(date_str)
        except Exception as e:
            raise ValueError(f"無法解析日期字串：{date_str}") from e

def normalize_month_key(month_str):
    """將任意格式的月份（如 2025-01-31T00:00:00Z）統一成 'YYYY/M'"""
    dt = parse_date_safe(month_str)
    return f"{dt.year}/{dt.month}"

class BillCalculator:
    def __init__(self, bill_data, tenant_data):
        # ✅ 將月份 key 標準化成 "YYYY/M"
        self.bill_data = {
            normalize_month_key(item["month"]): {
                "water": item["water"],
                "electricity": item["electricity"],
                "internet": item["internet"]
            }
            for item in bill_data
        }
        self.tenant_data = tenant_data
        self.person_days_by_month = defaultdict(dict)   # {month: {tenant: days}}
        self.total_days_by_month = defaultdict(int)     # {month: total_days_all_people}

    def calculate(self):
        self._calculate_person_days()
        person_day_sheet = self._calculate_person_day_costs()
        result_sheet = self._calculate_individual_costs(person_day_sheet)
        return {
            "person_day": person_day_sheet,
            "result": result_sheet
        }

    def _calculate_person_days(self):
        for tenant in self.tenant_data:
            name = tenant["name"]
            move_in = parse_date_safe(tenant["move_in"])
            move_out = parse_date_safe(tenant["move_out"])

            current = move_in
            while current <= move_out:
                ym = f"{current.year}/{current.month}"
                _, days_in_month = calendar.monthrange(current.year, current.month)

                start_day = current.day if current.year == move_in.year and current.month == move_in.month else 1
                end_day = move_out.day if current.year == move_out.year and current.month == move_out.month else days_in_month
                days = end_day - start_day + 1

                self.person_days_by_month[ym][name] = self.person_days_by_month[ym].get(name, 0) + days
                self.total_days_by_month[ym] += days

                # Move to next month
                current = (current.replace(day=28) + timedelta(days=4)).replace(day=1)

    def _calculate_person_day_costs(self):
        results = []
        for month, bill in self.bill_data.items():
            total_days = self.total_days_by_month.get(month, 0)

            if total_days == 0:
                water_per_day = electricity_per_day = internet_per_day = total_per_day = 0
            else:
                water_per_day = round(bill["water"] / total_days, 2)
                electricity_per_day = round(bill["electricity"] / total_days, 2)
                internet_per_day = round(bill["internet"] / total_days, 2)
                total_per_day = round(water_per_day + electricity_per_day + internet_per_day, 2)

            results.append({
                "month": month,
                "water": water_per_day,
                "electricity": electricity_per_day,
                "internet": internet_per_day,
                "total": total_per_day
            })

        return results

    def _calculate_individual_costs(self, person_day_sheet):
        results = []
        # 快速查表：每月人/日總費用
        person_day_lookup = {item["month"]: item["total"] for item in person_day_sheet}

        for month, tenants in self.person_days_by_month.items():
            per_person_day_total = person_day_lookup.get(month, 0)

            for name, days in tenants.items():
                total_cost = round(per_person_day_total * days, 2)
                results.append({
                    "name": name,
                    "month": month,
                    "居住天數": days,
                    "total_person_days": per_person_day_total,
                    "total": total_cost
                })

        return results
