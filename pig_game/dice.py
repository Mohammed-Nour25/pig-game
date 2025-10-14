import random
from typing import Final



class Dice:
    """
    A class representing a standard six-sided dice.

    Attributes
    ----------
    SIDES : Final[int]
        The number of sides on the dice (constant).

    Methods
    -------
    roll() -> int
        Simulates rolling the dice and returns a random integer between 1
and SIDES.
    """

    SIDES: Final[int] = 6  # constant number of sides on a standard dice

    def roll(self) -> int:
        """
        Roll the dice.

        Returns
        -------
        int
            A random integer between 1 and SIDES inclusive.
        """
        return random.randint(1, self.SIDES)
