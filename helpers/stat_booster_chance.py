import typing


def _get_yield_level_stat_booster_coefficient(yield_level_score: int) -> int:
    if (yield_level_score <= 20):
        return 1
    elif (yield_level_score <= 40):
        return 3
    elif (yield_level_score <= 60):
        return 5
    elif (yield_level_score <= 80):
        return 10
    elif (yield_level_score <= 90):
        return 15
    else:
        return 20


def get_stat_booster_chance(yield_level_score: int, grades: typing.List[int], cultivation_tier: int, blessing_of_the_land_event=False) -> int:
    stat_booster_chance = _get_yield_level_stat_booster_coefficient(yield_level_score)
    grade_chance = sum([(g - 1) * 5 for g in grades])    # TODO: Serenes forest's formula is vague here. Not sure if they mean the sum, or the lowest/highest grade.
    seed_count_chance = len(grades) * 6
    if (blessing_of_the_land_event):
        seed_count_chance += (5 * 6)
    cultivation_chance = cultivation_tier * 5

    return stat_booster_chance + grade_chance + seed_count_chance + cultivation_chance
