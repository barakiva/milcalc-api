import pytest
from datetime import datetime
from idf_calc import (
    total_days_in_range,
    get_total_days_in_2023,
    special_grant_calculation,
    is_one_range_more_than_5_days,
    calculate_days,
    calculate_vacation,
)
from rates import *


@pytest.mark.parametrize(
    "service_days, has_children, is_combat, expected",
    [
        (59, False, False, 0), # 59 days is less than 60 days
        (59, True, True, 0), # 59 days is less than 60 days
        (60, False, False, 1500), # no children, non-combatant
        (60, True, False, 2000), # has children, non-combatant
        (60, False, True, 3500), # no children, combatant
        (60, True, True, 4500), # has children, combatant
    ],
)
def test_calculate_vacation(service_days, has_children, is_combat, expected):
    assert calculate_vacation(service_days, has_children, is_combat) == expected


def create_date_range(start_date, end_date):
    return {"startDate": datetime(*start_date), "endDate": datetime(*end_date)}


@pytest.mark.parametrize(
    "start_date, end_date, expected",
    [
        (datetime(2021, 1, 2), datetime(2020, 1, 1), 0),
        (datetime(2021, 1, 1), datetime(2021, 1, 1), 1),
        (datetime(2021, 1, 1), datetime(2021, 1, 31), 31),
    ],
)
def test_total_days_in_range(start_date, end_date, expected):
    assert total_days_in_range(start_date, end_date) == expected


@pytest.mark.parametrize(
    "date_ranges, expected",
    [
        (
            [
                create_date_range((2021, 1, 1), (2021, 1, 31)),
                create_date_range((2024, 1, 1), (2024, 1, 31)),
            ],
            0,
        ),
        (
            [
                create_date_range((2023, 12, 31), (2024, 1, 30)),
            ],
            1,
        ),
        (
            [
                create_date_range((2023, 1, 1), (2023, 1, 31)),
                create_date_range((2023, 2, 1), (2023, 2, 28)),
                create_date_range((2023, 12, 31), (2024, 12, 1)),
            ],
            60,
        ),
    ],
)
def test_get_total_days_in_2023(date_ranges, expected):
    assert get_total_days_in_2023(date_ranges) == expected


def test_special_grant_calculation():
    assert special_grant_calculation(0, 0, False) == {
        "totalDaysStraight": 0,
        "totalAdditional": 0,
        "totalSpecialDays": 0,
        "totalExtended": 0,
    }
    assert special_grant_calculation(10, 5, False) == {
        "totalDaysStraight": 0,
        "totalSpecialDays": 0,
        "totalExtended": 0,
        "totalAdditional": 2820,
    }
    assert special_grant_calculation(14, 0.5, True) == {
        "totalDaysStraight": 266,
        "totalSpecialDays": 0,
        "totalExtended": 0,
        "totalAdditional": 1410,
    }
    # Continue with other test cases...


def test_is_one_range_more_than_5_days():
    assert not is_one_range_more_than_5_days([])
    assert not is_one_range_more_than_5_days(
        [
            {"startDate": datetime(2021, 1, 1), "endDate": datetime(2021, 1, 4)},
            {"startDate": datetime(2021, 1, 6), "endDate": datetime(2021, 1, 9)},
        ]
    )
    assert is_one_range_more_than_5_days(
        [
            {"startDate": datetime(2021, 1, 1), "endDate": datetime(2021, 1, 4)},
            {"startDate": datetime(2021, 1, 6), "endDate": datetime(2021, 1, 11)},
        ]
    )


def test_calculate_days():
    assert calculate_days([]) == 0
    assert (
        calculate_days(
            [
                {
                    "startDate": datetime(2021, 1, 1),
                    "endDate": datetime(2021, 1, 4),
                },
                {
                    "startDate": datetime(2021, 1, 6),
                    "endDate": datetime(2021, 1, 11),
                },
            ]
        )
        == 10
    )
    assert (
        calculate_days(
            [{"startDate": datetime(2023, 10, 7), "endDate": datetime(2024, 1, 9)}]
        )
        == 95
    )
