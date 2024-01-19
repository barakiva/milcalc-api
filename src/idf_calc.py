from calendar import c
from datetime import datetime
import math
from rates import *

# Vacation rates
def calculate_vacation(total_days, has_children, is_combat):
    if total_days < VACATION_COMPENSATION_DAILY_THRESHOLD:
        return 0
    children_bonus = VACATION_CHILD_BONUS_COMBATANT if is_combat else VACATION_CHILD_BONUS_NON_COMBATANT
    base_vacation = VACATION_RATE_COMBATANT if is_combat else VACATION_RATE_NON_COMBATANT
    return base_vacation + children_bonus if has_children else base_vacation

# Days
def calculate_days(date_ranges):
    total = 0
    for date_range in date_ranges:
        total += total_days_in_range(date_range["startDate"], date_range["endDate"])
    return total


def calculate_monthly_compensation(is_combat, days):
    if days < 40:
        return 0
    rate = COMBAT_RATE if is_combat else NON_COMBAT_RATE
    return math.floor((days - 30) / 10) * rate


def calculate_children_compensation(is_combat, days):
    if days < 40:
        return 0
    rate = 833 if is_combat else 500
    return math.floor((days - 30) / 10) * rate


def operation24_calculation(operation24_days):
    if operation24_days <= 0:
        return 0
    total_amount = 0
    first_tier_days = min(operation24_days, 10)
    total_amount += first_tier_days * 100
    if operation24_days > 10:
        second_tier_days = min(operation24_days - 10, 10)
        total_amount += second_tier_days * 150
    if operation24_days > 20:
        third_tier_days = operation24_days - 20
        total_amount += third_tier_days * 200
    return total_amount


def total_days_in_range(start_date, end_date):
    return max((end_date - start_date).days + 1, 0)


def is_one_range_more_than_5_days(date_ranges):
    return any(
        total_days_in_range(date_range["startDate"], date_range["endDate"]) >= 5
        for date_range in date_ranges
    )


def get_total_days_in_2023(date_ranges):
    total_days = 0
    start_2023 = datetime(2023, 1, 1)
    end_2023 = datetime(2023, 12, 31)
    for date_range in date_ranges:
        if date_range["endDate"] < start_2023 or date_range["startDate"] > end_2023:
            continue
        if date_range["startDate"].year < 2023:
            continue
        start = max(start_2023, date_range["startDate"])
        end = min(end_2023, date_range["endDate"])
        total_days += total_days_in_range(start, end)
    return total_days


def special_grant_calculation(days_before, days_in_war, days_straight):
    total_days = days_before + days_in_war
    total_additional = 0
    if 10 <= total_days <= 14.5:
        total_additional = 1410
    elif 15 <= total_days <= 19.5:
        total_additional = 2820
    elif 20 <= total_days <= 36.5:
        total_additional = 4230
    elif total_days >= 37:
        total_additional = 5640
    special_days = min(max(days_before - 32, 0), 28)
    total_special_days = special_days * GRANT_DAILY_RATE
    extended_days = 0
    if days_before >= 60:
        extended_days = days_in_war
    elif days_before > 32:
        extended_days = max(days_in_war - special_days, 0)
    else:
        extended_days = max(days_in_war - (31 - days_before), 0)
    total_extended = extended_days * GRANT_DAILY_RATE
    total_days_straight = 266 if days_straight else 0
    return {
        "totalDaysStraight": total_days_straight,
        "totalSpecialDays": total_special_days,
        "totalExtended": total_extended,
        "totalAdditional": total_additional,
    }


def calculate_compensation(inputs):
    date_ranges = [
        {
            "startDate": datetime.fromisoformat(date_range["startDate"]),
            "endDate": datetime.fromisoformat(date_range["endDate"]),
        }
        for date_range in inputs["dateRanges"]
    ]
    service_before = float(inputs["serviceBefore"])
    operation24_days = float(inputs["operation24Days"])
    is_days_straight_in_war = is_one_range_more_than_5_days(date_ranges)
    days_in_war = calculate_days(date_ranges)
    result = special_grant_calculation(
        service_before, days_in_war, inputs["isDaysStraight"] or is_days_straight_in_war
    )
    total_per_month = calculate_monthly_compensation(
        inputs["isCombat"], max(days_in_war, 0)
    )
    days_war_in_2023 = get_total_days_in_2023(date_ranges)
    total_operation24 = operation24_calculation(operation24_days)
    total_more_than45 = 2500 if inputs["isCombat"] and days_in_war > 45 else 1250
    total_from_children = (
        calculate_children_compensation(inputs["isCombat"], days_war_in_2023)
        if inputs["hasChildren"]
        else 0
    )
    total_vacation = calculate_vacation(
        days_in_war, inputs["hasChildren"], inputs["isCombat"]
    )
    total_special_children = (
        SPECIAL_NEEDS_COMPENSATION if inputs["hasChildrenSpecial"] else 0
    )
    total_mental = MENTAL_HEALTH_COMPENSATION if days_in_war > 30 else 0
    total_family_care = FAMILY_CARE_COMPENSATION
    total_dedication = 0
    return {
        "totalPerMonth": total_per_month,
        "totalMoreThan45": total_more_than45,
        "totalOperation24": total_operation24,
        "totalFromChildren": total_from_children,
        "totalVacation": total_vacation,
        "totalSpecialChildren": total_special_children,
        "totalMental": total_mental,
        "totalFamilyCare": total_family_care,
        "totalDedication": total_dedication,
        **result,
    }
