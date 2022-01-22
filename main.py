import itertools
import typing
import multiprocessing
from collections import defaultdict, Counter

from helpers.prof_level import get_maximum_seed_count, get_max_cultivation_tier
from helpers.yield_level import (
    get_base_yield_level_score,
    get_minimum_cultivation_tier,
    MAX_YIELD_LEVEL,
    YIELD_LEVEL_SCORE_THRESHOLDS,
    YIELD_LEVEL_INDICATORS,
)
from constants import seeds, cultivation
import config


# MARK: - Workers
class WorkerDropItem(Exception):
    pass


def get_base_yield_score(
    seed_combinations: typing.List[typing.Tuple[typing.Dict[str, typing.Union[str, int]], int]]
) -> int:
    ranks = [s[seeds.SEED_RANK_KEY] for s in seed_combinations]
    grades = [s[seeds.SEED_GRADE_KEY] for s in seed_combinations]

    base_yield_score = get_base_yield_level_score(ranks, grades)
    return base_yield_score


def worker(
    seed_combination: typing.List[typing.Tuple[typing.Dict[str, typing.Union[str, int]], int]],
    min_target_yield_level: int,
    max_cultivation_tier: cultivation.Method,
) -> typing.Tuple[typing.List[typing.Tuple[typing.Dict[str, typing.Union[str, int]], int]], typing.Dict[int, int]]:
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
        if min_cultivation_tier > max_cultivation_tier.value:
            # This and higher target yield levels are not achievable.
            break
        else:
            # This target yield level can be achieved with a cultivation method.
            return_value[level] = min_cultivation_tier

    if return_value:
        return (seed_combination, return_value)
    else:
        raise WorkerDropItem


# MARK: - Main
def main():
    max_seed_count = get_maximum_seed_count(config.PROFESSOR_LEVEL)  # We always use the max amount of seeds.

    # MARK: Get feasible combinations.
    max_cultivation_tier = get_max_cultivation_tier(config.PROFESSOR_LEVEL)

    feasible_combinations = defaultdict(list)
    """
    {yield level: [(seed combination, minimum cultivation tier)]}
    """

    def _worker_result_handler(
        result: typing.Tuple[
            typing.List[typing.Tuple[typing.Dict[str, typing.Union[str, int]], int]], typing.Dict[int, int]
        ]
    ):
        """
        Handles the valid results (without exception) of `worker`.

        :return:
        """
        for level, cultivation_tier in result[1].items():
            feasible_combinations[level].append((result[0], cultivation_tier))

    with multiprocessing.Pool() as pool:
        for seed_indices in itertools.combinations_with_replacement(range(len(config.MY_SEEDS)), max_seed_count):
            indices_counter = Counter(seed_indices)

            has_enough_seeds = True
            for i, expected_count in indices_counter.items():
                real_count = config.MY_SEEDS[i][1]
                if real_count < expected_count:
                    # Not enough seeds for this list of seed indices.
                    has_enough_seeds = False
                    break

            if not has_enough_seeds:
                continue

            seed_combination = [config.MY_SEEDS[i][0] for i in seed_indices]
            pool.apply_async(
                worker,
                (seed_combination, config.TARGET_YIELD_LEVEL, max_cultivation_tier),
                callback=_worker_result_handler,
            )

        pool.close()
        pool.join()

    # MARK: Print feasible combinations.
    if not feasible_combinations:
        print("No feasible combinations found!")
    else:
        # MARK: Sort the feasible combinations dict.
        # Sort by yield level: max yield level first.
        feasible_combinations = {
            yield_level: feasible_combinations[yield_level]
            for yield_level in sorted(feasible_combinations, reverse=True)
        }
        # Sort by required cultivation tier: cheaper cultivation tier first.
        for yield_level in feasible_combinations:
            feasible_combinations[yield_level] = sorted(feasible_combinations[yield_level], key=lambda x: x[1])

        # Print feasible combinations.
        # print(feasible_combinations)
        for yield_level, combo in feasible_combinations.items():
            # print(YIELD_LEVEL_INDICATORS[yield_level])
            for seed_combination, min_cultivation_tier in combo:
                seed_counts = Counter([seed[seeds.SEED_NAME_KEY] for seed in seed_combination])
                # seed_counts = {name: count for name, count in seed_counts.items()}
                seed_counts = dict(seed_counts)

                min_graded_seed = min(seed_combination, key=lambda x: x[seeds.SEED_GRADE_KEY])
                prof_exp = min_graded_seed[seeds.SEED_GRADE_KEY] * 100

                print(
                    f"{YIELD_LEVEL_INDICATORS[yield_level]} Prof exp: {prof_exp} {seed_counts} {cultivation.Method(min_cultivation_tier).get_name()}"
                )

            if combo:
                print()  # Separator between yield levels.


# MARK: - Main
if __name__ == "__main__":
    main()
