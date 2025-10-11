import random
from typing import Final

class Dice:
    """
    A class representing a dice for the Pig game.

    Attributes
    ----------
    SIDES : Final[int]
        Default number of sides for a standard dice.

    Methods
    -------
    roll() -> int
        Simulates rolling the dice and returns a random integer between 1
        and SIDES.
    """

    SIDES: Final[int] = 6  # default number of sides

    def __init__(self, sides: int = 6) -> None:
        """
        Create a Dice instance.

        Parameters
        ----------
        sides : int, optional
            Number of sides for the dice (default is 6).

        Raises
        ------
        ValueError
            If sides is not an integer >= 2.
        """
        if not isinstance(sides, int) or sides < 2: 
            raise ValueError("sides must be an integer >= 2")
        self.sides = sides
           
    def roll(self) -> int:
        """
        Roll the dice.
        
        Returns
        -------
        int
            A random integer between 1 and `sides` (inclusive).
        """
        return random.randint(1, self.sides)

