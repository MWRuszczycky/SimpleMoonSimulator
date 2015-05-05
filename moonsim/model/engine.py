import math
import pyglet

#######################################
# Core Classes.

class Vector:
    """Basic 2D vectors"""

    def __init__(self, x=0, y=0):
        """Initialization.

        Args:
            x: x position
            y: y position
        """
        self.x = x
        self.y = y

    def __add__(self, other):
        """Vector addition."""
        if isinstance(other, Vector):
            x = self.x + other.x
            y = self.y + other.y
        else:
            x = self.x + other
            y = self.y + other
        return Vector(x, y)

    def __sub__(self, other):
        """Vector substraction."""
        if isinstance(other, Vector):
            x = self.x - other.x
            y = self.y - other.y
        else:
            x = self.x - other
            y = self.y - other
        return Vector(x, y)

    def __mul__(self, other):
        """Vector dot product."""
        if isinstance(other, Vector):
            x = self.x * other.x
            y = self.y * other.y
        else:
            x = self.x * other
            y = self.y * other
        return Vector(x, y)

    def __rmul__(self, other):
        return self.__mul__(other)

    def __truediv__(self, other):
        """Division by scalar."""
        x = self.x / other
        y = self.y / other
        return Vector(x, y)
        
    def angle_deg(self):
        """Return angle in degrees."""
        return math.degrees(math.atan2(self.y, self.x))

    def angle_rad(self):
        """Return angle in radians."""
        return math.atan2(self.y, self.x)

    def mag(self):
        """Return vector magnitude."""
        return math.sqrt(self.x ** 2 + self.y ** 2)

    def norm(self):
        """Return vector magnitude."""
        mag = self.mag()
        x = self.x / mag
        y = self.y / mag
        return Vector(x, y)

class Rect:
    """Basic class for managing rectangles."""

    def __init__(self, x=0, y=0, width=0, height=0):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

#######################################
# Core functions.

def energy(moon, planets, gravity=0):
    """Determine the current energy of the moon.
        
    Args:
        moon (Moon): Moon object to determine energy for.
        planets (list of Planet): Planets objects setting up the
            gravitational field for the moon.
        gravity (float): Gravity constant.

    Returns: dict
        'total' (float): Calculated total energy of the moon.
        'kinetic' (float): Calculated kinetic energy of the moon.
        'potential' (float): Calculated potential energy of the moon.
    """
    pe = 0
    for planet in planets:
        r = planet.locus - moon.locus
        if r.mag() > (planet.width / 2 + moon.width / 2):
            pe -= gravity * planet.mass / r.mag()
    ke = moon.mass * (moon.velocity.mag() ** 2) / 2 
    te = ke + pe
    return {'total': te, 'kinetic': ke, 'potential': pe}

def update(dt, moon, planets, gravity=0):
    """Updates the current postion and velocity of the moon.
        
    Args:
        dt (float): Time step in seconds.
        moon (Moon): Moon object to be updated.
        planets (list of Planet): Planets setting up the
            gravitational field.
    
    Returns:
        Nothing.

    The moon is update over the timestep dt using the inverse square
    law of gravitation given the field set up by the planets. The
    integration uses the fourth-order Runge-Kutta algorithm.
    """
    if moon.crashed:
        return 0
    rkv1 = Vector(0, 0)
    for planet in planets:
        r = planet.locus - moon.locus
        if r.mag() > (planet.width / 2 + moon.width / 2):
            rkv1 += gravity * planet.mass * r.norm() * dt / r.mag() ** 2
        else:
            moon.crash()
            return 0
    rkx1 = moon.velocity * dt

    rkv2 = Vector(0, 0)
    for planet in planets:
        r = planet.locus - moon.locus + rkx1 / 2
        if r.mag() > (planet.width / 2 + moon.width / 2):
            rkv2 += gravity * planet.mass * r.norm() * dt / r.mag() ** 2
    rkx2 = (moon.velocity + rkv1 / 2) * dt

    rkv3 = Vector(0 ,0)
    for planet in planets:
        r = planet.locus - moon.locus + rkx2 / 2
        if r.mag() > (planet.width / 2 + moon.width / 2):
            rkv3 += gravity * planet.mass * r.norm() * dt / r.mag() ** 2
    rkx3 = (moon.velocity + rkv2 / 2) * dt

    rkv4 = Vector(0 ,0)
    for planet in planets:
        r = planet.locus - moon.locus + rkx3
        if r.mag() > (planet.width / 2 + moon.width / 2):
            rkv4 += gravity * planet.mass * r.norm() * dt / r.mag() ** 2
    rkx4 = (moon.velocity + rkv3) * dt

    moon.velocity += (rkv1 + 2 * rkv2 + 2 * rkv3 + rkv4) / 6
    moon.locus += (rkx1 + 2 * rkx2 + 2 * rkx3 + rkx4) / 6

def inrect(x, y, rect):
    """Determines whether a point lies in a rectangle.
    
    Args:
        x (int or float): X-coordinate of point.
        y (int or float): Y-coordinate of point.
        rect (Rect): Rectangle to check for point containment.
                     
    The rectangle must be perpendicular/parallel to the coordinates.
    If this is not the case, it must first be rotated."""
    in_rect_x = x > rect.x and x < rect.x + rect.width
    in_rect_y = y > rect.y and y < rect.y + rect.height
    return in_rect_x and in_rect_y
