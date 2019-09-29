from enum import Enum
"""I would like the enum to be the value of each of the characters __str__ class.
I want the enumeration to handle identifying which character we are talking about,
instead of using string values nested in the game logic."""


class Type(Enum):
    INSOMNIAC = "Insomniac"
    MINION = "Minion"
    ROBBER = "Robber"
    SEER = "Seer"
    TROUBLEMAKER = "Troublemaker"
    WEREWOLF = "Werewolf"
    VILLAGER = "Villager"
