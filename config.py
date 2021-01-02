"""
Your configuration.
"""

from constants import seeds


PROFESSOR_LEVEL = "A"
"""
Your professor level determines:

- Max number of seeds
- Best cultivation method
"""

MY_SEEDS = [
    (seeds.MIXED_HERB_SEEDS, 12),
    (seeds.WESTERN_FODLAN_SEEDS, 10),
    (seeds.ROOT_VEGETABLE_SEEDS, 10),
    (seeds.NORTHERN_FODLAN_SEEDS, 5),
    (seeds.MORFIS_SEEDS, 5),
    (seeds.NORDSALAT_SEEDS, 2),
    (seeds.ALBINEAN_SEEDS, 5),
    (seeds.EASTERN_FODLAN_SEEDS, 1),
    (seeds.MIXED_FRUIT_SEEDS, 12),
    (seeds.RED_FLOWER_SEEDS, 1),
    (seeds.BLUE_FLOWER_SEEDS, 1),
    (seeds.PURPLE_FLOWER_SEEDS, 2),
    (seeds.GREEN_FLOWER_SEEDS, 2),
    (seeds.PALE_BLUE_FLOWER_SEEDS, 2),
]
"""
(seed type, amount)
"""

TARGET_YIELD_LEVEL = 4
"""
Target yield level.

Combinations with smaller yield levels are ignored.

- 0: yield level ☆
- 1: yield level ★
- 2: yield level ★☆
- 3: yield level ★★
- 4: yield level ★★☆ (recommended)
- 5: yield level ★★★
"""
