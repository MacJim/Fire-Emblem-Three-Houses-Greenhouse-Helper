"""
Yield level stuff.
"""

import math
import typing


# MARK: - Yield level calculation
def get_base_yield_level_score(ranks: typing.List[int], grades: typing.List[int]) -> int:
    """
    Get the yield level score without any cultivation methods.

    :param ranks: Seed ranks.
    :param grades: Seed grades.
    :return:
    """
    rank_score = (12 - sum(ranks) % 12) * 5
    grade_score = math.floor(sum(grades) / 5 * 4)

    return rank_score + grade_score


def get_minimum_cultivation_tier(current_score: int, target_score: int) -> int:
    if (current_score >= target_score):
        return 0

    deficit = target_score - current_score
    cultivation_tier = math.ceil(deficit / 2 - 4)

    return cultivation_tier


def get_cultivation_yield_level_score(cultivation_tier: int) -> int:
    cultivation_score = (cultivation_tier + 4) * 2

    return cultivation_score


def get_yield_level_score(ranks: typing.List[int], grades: typing.List[int], cultivation_tier: int) -> int:
    return get_base_yield_level_score(ranks, grades) + get_cultivation_yield_level_score(cultivation_tier)


# MARK: - Yield level string
def get_yield_level_indicator_from_yield_score(score: int) -> str:
    """
    Get a human-readable yield level indicator string.

    :param score:
    :return:
    """
    if (score <= 20):
        return "☆"
    elif (score <= 40):
        return "★"
    elif (score <= 60):
        return "★☆"
    elif (score <= 80):
        return "★★"
    elif (score <= 90):
        return "★★☆"
    else:
        return "★★★"


# print(get_yield_level_score([33] * 4, [1] * 4, 0))
