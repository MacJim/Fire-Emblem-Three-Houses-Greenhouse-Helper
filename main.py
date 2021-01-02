import itertools
import typing
import multiprocessing
from collections import defaultdict

from helpers.prof_level import get_maximum_seed_count, get_max_cultivation_tier
from helpers.yield_level import get_base_yield_level_score, get_minimum_cultivation_tier, MAX_YIELD_LEVEL, YIELD_LEVEL_SCORE_THRESHOLDS
from constants import seeds, cultivation
import config


# MARK: - Workers
def get_base_yield_score(seed_combinations: typing.List[typing.Tuple[typing.Dict[str, typing.Union[str, int]], int]]) -> int:
    ranks = [s[seeds.SEED_RANK_KEY] for s in seed_combinations]
    grades = [s[seeds.SEED_GRADE_KEY] for s in seed_combinations]

    base_yield_score = get_base_yield_level_score(ranks, grades)
    return base_yield_score


def worker(seed_combination: typing.List[typing.Tuple[typing.Dict[str, typing.Union[str, int]], int]], min_target_yield_level: int, max_cultivation_tier: cultivation.Method) -> typing.Tuple[typing.List[typing.Tuple[typing.Dict[str, typing.Union[str, int]], int]], typing.Dict[int, int]]:
    """
    1. Get base yield score
    2. For each target yield level, calculate the feasibility and minimum cultivation tier
    3. Return (seed combination, {target yield level: minimum cultivation tier})

    :return:
    """
    base_yield_score = get_base_yield_score(seed_combination)

    return_value = {}

    for level in range(min_target_yield_level, MAX_YIELD_LEVEL + 1):
        min_cultivation_tier = get_minimum_cultivation_tier(base_yield_score, YIELD_LEVEL_SCORE_THRESHOLDS[level])
        if (min_cultivation_tier > max_cultivation_tier.value):
            # This and higher target yield levels are not achievable.
            break
        else:
            # This target yield level can be achieved with a cultivation method.
            return_value[level] = min_cultivation_tier

    return (seed_combination, return_value)


# MARK: - Main
def main():
    max_seed_count = get_maximum_seed_count(config.PROFESSOR_LEVEL)    # We always use the max amount of seeds.

    # MARK: Get seed combinations.
    available_seeds = []
    for seed, count in config.MY_SEEDS:
        if (count > max_seed_count):
            count = max_seed_count

        for _ in range(count):
            available_seeds.append(seed)

    seed_combinations = itertools.combinations(available_seeds, max_seed_count)

    # MARK: Get feasible combinations.
    max_cultivation_tier = get_max_cultivation_tier(config.PROFESSOR_LEVEL)

    feasible_combinations = defaultdict(list)
    """
    {yield level: [(seed combination, minimum cultivation tier)]}
    """

    def _worker_result_handler(result: typing.Tuple[typing.List[typing.Tuple[typing.Dict[str, typing.Union[str, int]], int]], typing.Dict[int, int]]):
        """
        Handles the results of `worker`.

        Adds the possible tuples

        :return:
        """
        if (result[1]):
            seed_combination = result[0]
            for level, cultivation_tier in result[1].items():
                feasible_combinations[level].append((seed_combination, cultivation_tier))

    with multiprocessing.Pool() as pool:
        for combination in seed_combinations:
            pool.apply_async(worker, (combination, config.TARGET_YIELD_LEVEL, max_cultivation_tier), callback=_worker_result_handler)

        pool.close()
        pool.join()

    # MARK: Print feasible combinations.
    if (not feasible_combinations):
        print("No feasible combinations found!")
    else:
        # Sort the feasible combinations dict.
        feasible_combinations = {yield_level: feasible_combinations[yield_level] for yield_level in sorted(feasible_combinations)}
        for yield_level in feasible_combinations:
            feasible_combinations[yield_level] = sorted(feasible_combinations[yield_level], key=lambda x: x[1])

        # Print feasible combinations.
        print(feasible_combinations)


# MARK: - Main
if __name__ == '__main__':
    main()
