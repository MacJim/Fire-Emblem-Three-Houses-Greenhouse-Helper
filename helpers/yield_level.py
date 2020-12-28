"""
Yield level stuff.
"""

import math
import typing


# MARK: - Yield level calculation
def get_yield_level_score(ranks: typing.List[int], grades: typing.List[int], cultivation_tier: int) -> int:
    rank_score = (12 - sum(ranks) % 12) * 5
    grade_score = math.floor(sum(grades) / 5 * 4)
    cultivation_score = (cultivation_tier + 4) * 2

    return rank_score + grade_score + cultivation_score


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
