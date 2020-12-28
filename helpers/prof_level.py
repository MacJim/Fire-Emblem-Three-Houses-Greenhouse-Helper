"""
Prof level related variables.
"""

import typing

from constants import cultivation


def get_maximum_seed_count(prof_level: str) -> int:
    prof_level_upper = prof_level.upper()
    if ("E" in prof_level_upper):
        return 1
    elif ("D" in prof_level_upper):
        return 2
    elif ("C" in prof_level_upper):
        return 3
    elif ("B" in prof_level_upper):
        return 4
    elif ("A" in prof_level_upper):
        return 5
    else:
        raise ValueError(f"Invalid professor level \"{prof_level}\".")


def get_available_cultivation_method(prof_level: str) -> typing.List[typing.Dict[str, typing.Any]]:
    return_value = []

    prof_level_upper = prof_level.upper()
    if ("E" in prof_level_upper):
        return_value.append(cultivation.INFUSE_WITH_MAGIC)
        if ("+" in prof_level_upper):
            return_value.append(cultivation.POUR_AIRMID_WATER)
    elif ("D" in prof_level_upper):
        return_value.append(cultivation.PRUNE)
    elif ("C" in prof_level_upper):
        return_value.append(cultivation.SCATTER_BONEMEAL)
    elif ("B" in prof_level_upper):
        return_value.append(cultivation.USE_CALEDONIAN_SOIL)
    elif ("A" in prof_level_upper):
        return_value.append(cultivation.SPREAD_PEGASUS_BLESSINGS)
    else:
        raise ValueError(f"Invalid professor level \"{prof_level}\".")

    return return_value
