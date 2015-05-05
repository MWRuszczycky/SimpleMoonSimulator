import math
import pyglet
from model.engine import Vector

class Planet(pyglet.sprite.Sprite):
    """Manages the planet object."""

    def __init__(self, img, locus, mass=1, batch=None):
        """Initialization.
        Args:
            img (image): Sprite graphic for the planet.
            locus (Vector): Position vector for the planet.
            mass (float): Relative mass of the planet.
            batch (pyglet.graphics.Batch): Batch for drawing.
        """
        super().__init__(img=img, batch=batch)
        self.mass = mass
        self.__locus = Vector(locus.x, locus.y)
        self.locus = self.__locus

    @property
    def locus(self):
        """Getter for the planet locus vector."""
        return self.__locus

    @locus.setter
    def locus(self, value):
        """Setter for the planet locus vector.

        Args:
            value (Vector): Vector to the center of the planet.
            
        self.__locus is a vector to the center of the planet; however
        the sprite is drawn from the lower left position. This method
        makes the correction so the sprite is displayed correctly. 
        """
        self.__locus.x = value.x
        self.__locus.y = value.y
        self.x = self.__locus.x - self.width / 2
        self.y = self.__locus.y - self.height / 2
