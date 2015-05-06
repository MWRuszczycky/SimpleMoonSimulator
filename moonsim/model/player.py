import pyglet
import model
import resources.indices as ind

class Player():
    """Manages the simulation animation player."""

    def __init__(self, start_img, pause_img, stop_img, reset_img,
                 x=0, y=0, batch=None):
        """Initialization.

        Args:
            start_img (image res): Start button image.
            pause_img (image res): Pause button image.
            stop_img (image res): Stop button image.
            reset_img (image res): Reset button image.
            x (int): X-position of control set.
            y (int): y-position of control set.
        """
        self.images = {
            ind.START_BTN : start_img,
            ind.PAUSE_BTN : pause_img,
            ind.STOP_BTN  : stop_img,
            ind.RESET_BTN : reset_img}
        self.play_btn = pyglet.sprite.Sprite(
            img=self.images[ind.START_BTN], batch=batch)
        self.stop_btn = pyglet.sprite.Sprite(
            img=self.images[ind.STOP_BTN], batch=batch)
        self.reset_btn = pyglet.sprite.Sprite(
            img=self.images[ind.RESET_BTN], batch=batch)
        self.x = x
        self.y = y

#######################################
# Signals.
# These are methods that can be connected to slot methods in another
# object to allow communication without dispatching events. If the
# signal methods are not connected, they do nothing.

    def sig_play_pause_clicked():
        """Emitted when the play/pause button is clicked."""
        pass

    def sig_stop_clicked():
        """Emitted when the stop button is clicked."""
        pass

    def sig_reset_clicked():
        """Emitted when the reset button is clicked."""
        pass

#######################################
# Generic methods.

    def click(self, x, y, info=None):
        """Manage mouse down events on the player object.
            
        Args:
            x (int or float): X-coordinate of the mouse down.
            y (int or float): Y-coordinate of the mouse down.
            info: Additional information.

        Returns:
            Nothing.
                      
        Routes the click depending on which part of the player was
        clicked and calls the corresponding signal method.
        """
        if model.engine.inrect(x, y, self.play_btn):
            self.sig_play_pause_clicked()
        elif model.engine.inrect(x, y, self.stop_btn):
            self.sig_stop_clicked()
        elif model.engine.inrect(x, y, self.reset_btn):
            self.sig_reset_clicked()

    def play(self):
        """Indicate that the simulation is running."""
        self.play_btn.image = self.images[ind.PAUSE_BTN]

    def pause(self):
        """Indicate that the simulation is paused."""
        self.play_btn.image = self.images[ind.START_BTN]

    def stop(self):
        """Indicate that the simulation is stopped."""
        self.play_btn.image = self.images[ind.START_BTN]

    def reset(self):
        """Indicate that the simulation has been reset."""
        self.play_btn.image = self.images[ind.START_BTN]

    @property
    def x(self):
        """Getter for the x position of the player object."""
        return self.__x

    @x.setter
    def x(self, value):
        """Setter for the x postion of the player object.

        Updates the x-positions of all the component sprites.
        """
        self.__x = value
        self.play_btn.x = self.__x
        self.stop_btn.x = self.play_btn.x + self.play_btn.width
        self.reset_btn.x = self.stop_btn.x + self.stop_btn.width 

    @property
    def y(self):
        """Getter for the y position of the player object."""
        return self.__y

    @y.setter
    def y(self, value):
        """Setter for the y position of the player object.

        Updates the y-positions of all the component sprites.
        """
        self.__y = value
        self.play_btn.y = self.__y
        self.stop_btn.y = self.__y
        self.reset_btn.y = self.__y

    @property
    def width(self):
        """Getter for width of the entire player object."""
        return sum([
            self.play_btn.width,
            self.stop_btn.width,
            self.reset_btn.width])

    @property
    def height(self):
        """Getter for the height of the entire player object."""
        return max([
            self.play_btn.height,
            self.stop_btn.height,
            self.reset_btn.height])
