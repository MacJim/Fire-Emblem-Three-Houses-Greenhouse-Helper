"""
Prof level related variables.
"""

import typing

from constants import cultivation


def get_maximum_seed_count(prof_level: str) -> int:
    prof_level_upper = prof_level.upper()
    if "E" in prof_level_upper:
        return 1
    elif "D" in prof_level_upper:
        return 2
    elif "C" in prof_level_upper:
        return 3
    elif "B" in prof_level_upper:
        return 4
    elif "A" in prof_level_upper:
        return 5
    else:
        raise ValueError(f'Invalid professor level "{prof_level}".')


def get_max_cultivation_tier(prof_level: str) -> cultivation.Method:
    prof_level_upper = prof_level.upper()
    if "E" in prof_level_upper:
        if "+" in prof_level_upper:
            return cultivation.Method.POUR_AIRMID_WATER
        else:
            return cultivation.Method.INFUSE_WITH_MAGIC
    elif "D" in prof_level_upper:
        return cultivation.Method.PRUNE
    elif "C" in prof_level_upper:
        return cultivation.Method.SCATTER_BONEMEAL
    elif "B" in prof_level_upper:
        return cultivation.Method.USE_CALEDONIAN_SOIL
    elif "A" in prof_level_upper:
        return cultivation.Method.SPREAD_PEGASUS_BLESSINGS
    else:
        raise ValueError(f'Invalid professor level "{prof_level}".')
