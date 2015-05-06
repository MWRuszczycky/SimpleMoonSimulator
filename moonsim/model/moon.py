import math
import pyglet
import model
import resources.indices as ind
from model.engine import Vector, Rect
from resources import const

class Moon(pyglet.sprite.Sprite):
    """Manages the moon object for the simulation."""

    def __init__(self, images, locus, velocity, mass=const.MOON_MASS,
                 batch=None, path_segment=5, path_length=200):
        """Initialization.
        Args:
            images (list of images): Sprite graphics for the moon.
            batch (pyglet.graphics.Batch): Batch for drawing.
            locus (Vector): Initial position vector.
            velocity (Vector): Initial velocity vector.
            mass (float): Mass of the moon.
            path_segment (int): Min length of path segment.
            path_length (int): Max number of segments in path.
        """
        super().__init__(img=images[0], batch=batch)
        self.path = [locus.x, locus.y]
        self.path_segment = path_segment
        self.path_length = path_length
        self.images = images
        self.mass = mass
        self.__locus = locus
        self.velocity = velocity
        self.crashed = False
        self.__adjust_position()

#######################################
# Signals.
# These are methods that can be connected to slot methods in another
# object to allow communication without dispatching events. If the
# signal methods are not connected, they do nothing.

    def sig_moon_clicked(self):
        """Emitted when the moon is clicked."""
        pass

    def sig_arrow_clicked(self):
        """Emitted when the moon velocity arrow is clicked."""
        pass

#######################################
# Methods.

    def reset(self, locus=None, velocity=None):
        """Reset the moon location and velocity.
           
        Args:
            locus (Vector): New moon locus.
            velocity (Vector): New moon velocity.

        Returns:
            Nothing.

        The locus is centered at the center of the moon sprite. If
        locus or velocity is None, then no change is made to the
        corresponding member.
        """
        self.image = self.images[0]
        self.crashed = False
        if locus != None:
            self.locus = locus
        if velocity != None:
            self.velocity = velocity
        self.path = [self.__locus.x, self.__locus.y]

    def crash(self):
        """Indicate that the moon has crashed.
        
        Args:
            None.

        Returns:
            Nothing.

        Sets the velocity to (0, 0), changes the sprite image to an
        explosion and sets the crashed flag to true.
        """
        self.velocity = Vector(0, 0)
        self.image = self.images[1]
        self.crashed = True
        self.__adjust_position()

    def change_velocity(self, mpos):
        """Set the velocity based on position of the mouse.
        
        Args:
            mpos (Vector): Vector from moon center to the mouse.

        Returns:
            Nothing.
        """
        mdir = mpos.norm()
        new_vel_mag = mpos.mag() - self.width * const.MOON_ARROW_BASE_SHIFT
        if new_vel_mag < 0:
            new_vel_mag = 0
        new_vel_mag /= const.MOON_ARROW_LEN_SCALE
        self.velocity = new_vel_mag * mdir

    def get_velocity_arrow(self):
        """Returns the unrotated, untranslated arrow vertices.
        
        Args:
            None.
        Returns:
            vertices (tuple of float): Vertices to draw the triangle
                fan for the velocity arrow.
            numv (int): Number of vertices.
                        
        The vertices are determined for the unrotated, untranslated
        velocity arrow that points from the origin right along the
        x-axis. The base is positioned correctly versus the moon
        sprite at the oring. If no arrow is to be drawn, numv = 0.
        """
        # X-pos of start of arrow base.
        basex = const.MOON_ARROW_BASE_SHIFT * self.width
        # Dimensions of rectangular part of arrow.
        xdimbase = const.MOON_ARROW_LEN_SCALE * self.velocity.mag()
        ydimbase = const.MOON_ARROW_WIDTH_SCALE * self.width
        if xdimbase < 1:
            return (), 0
        # x-pos of arrow tip.
        xtip = basex + xdimbase + const.MOON_ARROW_HDX
        vertices = (
            xtip, 0,
            xtip - const.MOON_ARROW_HDXFULL, -const.MOON_ARROW_HDY / 2,
            xtip - const.MOON_ARROW_HDX, -ydimbase / 2,
            basex, -ydimbase / 2,
            basex, ydimbase / 2,
            xtip - const.MOON_ARROW_HDX, ydimbase / 2,
            xtip - const.MOON_ARROW_HDXFULL, const.MOON_ARROW_HDY / 2)
        numv = 7
        return vertices, numv

    def chk_in_arrow(self, x, y):
        """Checks whether point is inside the velocity arrow.

        Args:
            x (float or int): X-coordinate of the point.
            y (float or int): Y-coordinate of the point.

        Returns:
            bool: True if the point is contained, False if not.

        The check is accomplished by setting up a bounding rect for
        the arrow that is aligned along the x-axis pointing to the
        right.  The point is then set relative to the moon and
        rotated to a corresponding orientation versus the bounding
        rect along the axis. The model.engine.inrect method is the
        used to determine containment.
        """
        # Bounding rect for velocity arrow.
        arrow_rect = Rect()
        arrow_rect.width = (
            const.MOON_ARROW_LEN_SCALE * self.velocity.mag() +
            const.MOON_ARROW_HDX)
        arrow_rect.height = const.MOON_ARROW_WIDTH_SCALE * self.width
        arrow_rect.x = const.MOON_ARROW_BASE_SHIFT * self.width
        arrow_rect.y = -arrow_rect.height / 2
        # Get click position relative to the moon.
        pos = Vector(x, y)
        rel_pos = pos - self.__locus 
        # Rotate the relative click position to the new arrow position.
        ang = -self.velocity.angle_rad()
        rel_rot_x = rel_pos.x * math.cos(ang) - rel_pos.y * math.sin(ang)
        rel_rot_y = rel_pos.x * math.sin(ang) + rel_pos.y * math.cos(ang)
        return model.engine.inrect(rel_rot_x, rel_rot_y, arrow_rect)

    def click(self, x, y, info):
        """Route click events on the moon and velocity arrow.

        Args:
            x (float or int): X-coordinate of click.
            y (float or int): Y-coordinate of click.
            info (string): String indicating routing.

        Returns:
            Nothing.
                           
        This method is a convenience method that does nothing more
        than take a click event on the moon and its velocity arrow
        and decompose it depending on whether the click was on the
        arrow or the moon itself."""
        if info == ind.MOON:
            self.sig_moon_clicked(x, y)
        elif info == ind.ARROW:
            self.sig_arrow_clicked(x, y)

    def __adjust_position(self):
        """Adjust the sprite position based on the locus vector.

        Args:
            None.

        Returns:
            Nothing.

        The sprite drawing reference is left/bottom, and the locus
        vector is center/center. This method corrects the sprite the
        drawing reference based on the locus vector.
        """
        self.x = self.__locus.x - self.width / 2
        self.y = self.__locus.y - self.height / 2

    @property
    def locus(self):
        """Getter for the locus vector."""
        return self.__locus

    @locus.setter
    def locus(self, value):
        """Setter for the locus vector.

        This method will also update the moon path.
        """
        if len(self.path) // 2 > 0:
            delta_x = value - Vector(self.path[-2], self.path[-1])
            disp = delta_x.mag()
        else:
            disp = 0
        self.__locus.x = value.x
        self.__locus.y = value.y
        self.__adjust_position()
        if disp >= self.path_segment:
            self.path.extend((self.__locus.x, self.__locus.y))
            if len(self.path) // 2 > self.path_length:
                self.path = self.path[2:]
