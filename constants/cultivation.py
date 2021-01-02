"""
Cultivation information.
"""

import enum


# MARK: - Methods
class Method (enum.Enum):
    NONE = 0
    INFUSE_WITH_MAGIC = 1
    POUR_AIRMID_WATER = 2
    PRUNE = 3
    SCATTER_BONEMEAL = 4
    USE_CALEDONIAN_SOIL = 5
    SPREAD_PEGASUS_BLESSINGS = 6

    def get_cost(self) -> int:
        if (self == Method.NONE):
            return 0
        elif (self == Method.INFUSE_WITH_MAGIC):
            return 0
        elif (self == Method.POUR_AIRMID_WATER):
            return 300
        elif (self == Method.PRUNE):
            return 500
        elif (self == Method.SCATTER_BONEMEAL):
            return 1000
        elif (self == Method.USE_CALEDONIAN_SOIL):
            return 1500
        elif (self == Method.SPREAD_PEGASUS_BLESSINGS):
            return 2000
        else:
            raise ValueError(f"Unknown cultivation method {self} (value: {self.value}).")

    def get_name(self) -> str:
        if (self == Method.NONE):
            return "No cultivation"
        elif (self == Method.INFUSE_WITH_MAGIC):
            return "Infuse with magic (0G)"
        elif (self == Method.POUR_AIRMID_WATER):
            return "Pour Airmid water (300G)"
        elif (self == Method.PRUNE):
            return "Prune (500G)"
        elif (self == Method.SCATTER_BONEMEAL):
            return "Scatter Bonemeal (1,000G)"
        elif (self == Method.USE_CALEDONIAN_SOIL):
            return "Use Caledonian soil (1,500G)"
        elif (self == Method.SPREAD_PEGASUS_BLESSINGS):
            return "Spread pegasus blessings (2,000G)"
        else:
            raise ValueError(f"Unknown cultivation method {self} (value: {self.value}).")
