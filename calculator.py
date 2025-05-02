from datetime import datetime, timedelta
from collections import defaultdict
import calendar

class BillCalculator:
    def __init__(self, bill_data, tenant_data):
        self.bill_data = {item["month"]: item for item in bill_data}
        self.tenant_data = tenant_data
        self.tenants_by_month = defaultdict(list)
        self.person_day_counts = defaultdict(lambda: defaultdict(int))  # {month: {tenant: days}}
        self.total_person_days = defaultdict(int)  # {month: total_days}

    def calculate(self):
        self._distribute_days()
        person_day_results = self._calculate_person_day_costs()
        result_records = self._calculate_individual_costs()
        return {
            "person_day": person_day_results,
            "result": result_records
        }

    def _distribute_days(self):
        for tenant in self.tenant_data:
            name = tenant["name"]
            move_in = datetime.strptime(tenant["move_in"], "%Y/%m/%d")
            move_out = datetime.strptime(tenant["move_out"], "%Y/%m/%d")
            current = move_in

            while current <= move_out:
                year_month = f"{current.year}/{current.month}"
                _, days_in_month = calendar.monthrange(current.year, current.month)

                start_day = current.day if current.month == move_in.month and current.year == move_in.year else 1
                end_day = move_out.day if current.month == move_out.month and current.year == move_out.year else days_in_month
                days = end_day - start_day + 1

                self.person_day_counts[year_month][name] += days
                self.total_person_days[year_month] += days

                # move to next month
                next_month = current.replace(day=28) + timedelta(days=4)
                current = next_month.replace(day=1)

    def _calculate_person_day_costs(self):
        results = []
        for month, bill in self.bill_data.items():
            total_days = self.total_person_days.get(month, 0)
            if total_days == 0:
                continue
            water = round(bill["water"] / total_days, 2)
            electricity = round(bill["electricity"] / total_days, 2)
            internet = round(bill["internet"] / total_days, 2)
            total = round(water + electricity + internet, 2)
            results.append({
                "month": month,
                "water": water,
                "electricity": electricity,
                "internet": internet,
                "total": total
            })
        return results

    def _calculate_individual_costs(self):
        results = []
        for month, people in self.person_day_counts.items():
            total_days = self.total_person_days[month]
            bill = self.bill_data.get(month)
            if not bill or total_days == 0:
                continue
            unit_cost = {
                "water": bill["water"] / total_days,
                "electricity": bill["electricity"] / total_days,
                "internet": bill["internet"] / total_days,
            }
            for name, days in people.items():
                total = round(
                    (unit_cost["water"] + unit_cost["electricity"] + unit_cost["internet"]) * days,
                    2
                )
                results.append({
                    "name": name,
                    "month": month,
                    "居住天數": days,
                    "total_person_days": total_days,
                    "total": total
                })
        return results
