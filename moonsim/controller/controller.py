import copy
import pyglet
import model
import view.viewer
import resources.images
import resources.indices as ind
from pyglet.window import mouse
from model.engine import Vector
from resources import const

class Controller(pyglet.window.Window):
    """Manages the simulation, window and events."""

    def __init__(self,
        disp_par=False,
        moon_locx=const.MOON_PER_LOCX, moon_locy=const.MOON_PER_LOCY,
        moon_velx=const.MOON_PER_VELX, moon_vely=const.MOON_PER_VELY,
        win_width=const.MAIN_WIN_WIDTH, win_height=const.MAIN_WIN_HEIGHT):
        """Initialization.

        Args:
            disp_par (bool): Flag for whether the simulation
                label should be drawn.
        """
        config = pyglet.gl.Config(
            double_buffer=True, sample_buffers=1, samples=4)
        super().__init__(
            width=win_width,
            height=win_height,
            caption=const.MAIN_WIN_TITLE,
            config=config)
        # Initialize the simulation master data object.
        self.simstate = ind.STOPPED
        self.simmode = ind.READY
        self.simoptions = {ind.DISP_PAR: disp_par}
        self.resets = {
            ind.INIT_LOC: Vector(moon_locx, moon_locy),
            ind.INIT_VEL: Vector(moon_velx, moon_vely),
            ind.LAST_LOC: Vector(moon_locx, moon_locy),
            ind.LAST_VEL: Vector(moon_velx, moon_vely)}

        # Initialize the simulation objects and the graphics batch.
        self.graphics_batch = pyglet.graphics.Batch()
        self.planets = list()
        self.planets.append(
            model.planet.Planet(
                resources.images.planet,
                locus=Vector(const.PLANET_INIT_LOCX, const.PLANET_INIT_LOCY),
                batch=self.graphics_batch))

        self.moon = model.moon.Moon(
            images=[resources.images.moon, resources.images.crash_animation],
            locus=Vector(moon_locx, moon_locy),
            velocity=Vector(moon_velx, moon_vely),
            batch=self.graphics_batch)

        self.player = model.player.Player(
            start_img=resources.images.start_button,
            pause_img=resources.images.pause_button,
            stop_img=resources.images.stop_button,
            reset_img=resources.images.reset_button,
            x=win_width,
            y=win_height,
            batch=self.graphics_batch)
        self.player.x -= self.player.width
        self.player.y -= self.player.height

        # Initialize the viewer.
        self.viewer = view.viewer.Viewer(self)

        # Connect signals and slots.
        self.__connect()

#######################################
# Pyglet event handlers.
# These methods respond to events dispatched by the Pyglet main loop.

    def on_draw(self):
        """Handler for window paint events."""
        if self.simstate in [ind.STOPPED, ind.PAUSED] and not self.moon.crashed:
            self.viewer.render_arrow(self.moon)
        self.viewer.render_path(self.moon)
        energy = model.engine.energy(
            self.moon, self.planets, gravity=const.GRAVITY)
        if self.simoptions[ind.DISP_PAR]:
            self.viewer.render_label(
                energy, self.moon, pyglet.clock.get_fps(),
                self.simstate, self.simmode)
        self.viewer.paint(self, self.graphics_batch)

    def on_mouse_press(self, x, y, button, modifiers):
        """Handler for mouse-down events."""
        if button != mouse.LEFT:
            return
        clicked_object, info = self.__get_clicked(x, y)
        if clicked_object == None:
            return
        clicked_object.click(x=x, y=y, info=info)

    def on_mouse_release(self, x, y, button, modifiers):
        """Handler for for mouse-up events."""
        if button != mouse.LEFT:
            return
        if self.simmode in [ind.MOVE_MOON, ind.MOVE_ARROW]:
            self.resets[ind.LAST_LOC] = copy.deepcopy(self.moon.locus)
            self.resets[ind.LAST_VEL] = copy.deepcopy(self.moon.velocity)
        self.simmode = ind.READY

    def on_mouse_drag(self, x, y, dx, dy, buttons, modifiers):
        """Handler for mouse-drag events."""
        if not mouse.LEFT & buttons:
            return
        if self.simmode == ind.MOVE_MOON:
            self.move_moon(x, y)
        elif self.simmode == ind.MOVE_ARROW:
            self.move_arrow(x, y)

#######################################
# Slots.
# These are general public methods and may be called by member
# objects via their signal methods. Slots are connected with signals
# in the __connect method.

    def update(self, dt):
        """Updates the moon during simulation runs.

        Args:
            None.
        Returns:
            Nothing.

        This method is scheduled via Pyglet when the simulation is
        running, and unscheduled when not.
        """
        subdt = dt / const.FRAME_DIVS
        for step in range(0, const.FRAME_DIVS):
            model.engine.update(
                subdt, self.moon, self.planets, gravity=const.GRAVITY)

    def toggle_sim(self):
        """Starts and pauses the simulation.

        Args:
            None.
        Returns:
            Nothing.
        """
        if self.simstate == ind.RUNNING:
            pyglet.clock.unschedule(self.update)
            self.simstate = ind.PAUSED
            self.player.pause()
        else:
            self.simstate = ind.RUNNING
            self.player.play()
            self.simmode = ind.READY
            pyglet.clock.schedule_interval(self.update, 1 / const.FRAME_RATE)

    def stop_sim(self):
        """Stops simulation and resets moon to initial state.

        Args:
            None.
        Returns:
            Nothing.
        """
        if self.simstate == ind.RUNNING:
            pyglet.clock.unschedule(self.update)
        self.simstate = ind.STOPPED
        self.player.stop()
        self.simmode = ind.READY
        self.moon.reset(self.resets[ind.INIT_LOC], self.resets[ind.INIT_VEL])

    def reset_sim(self):
        """Stops simulation and resets moon to last start state.
            
        Args:
            None.
        Returns:
            Nothing.
        """
        if self.simstate == ind.RUNNING:
            pyglet.clock.unschedule(self.update)
        self.simstate = ind.STOPPED
        self.player.reset()
        self.simmode = ind.READY
        self.moon.reset(self.resets[ind.LAST_LOC], self.resets[ind.LAST_VEL])

    def move_moon(self, x, y):
        """Repositions the moon based on bouse input.
        
        Args:
            x (float): New mouse-x coordinate for moon center.
            y (float): New mouse-y coordinate for moon center.

        Returns:
            Nothing.
        """
        if self.simstate in [ind.PAUSED, ind.STOPPED] and not self.moon.crashed:
            self.simmode = ind.MOVE_MOON
            self.moon.reset(locus=Vector(x, y))

    def move_arrow(self, x, y):
        """Changes the velocity of the moon  based on mouse input.
        
        Args:
            x (float): Mouse-x coordinate (absolute).
            y (float): Mouse-y coordinate (absolute).

        Returns:
            Nothing.

        Uses the distance from the mouse point to the center of the
        moon to determine a new moon velocity using the
        change_velocity method of the moon object.
        """
        if self.simstate in [ind.PAUSED, ind.STOPPED] and not self.moon.crashed:
            self.simmode = ind.MOVE_ARROW
            mouse_abs = Vector(x, y)
            mouse_rel = mouse_abs - self.moon.locus
            self.moon.change_velocity(mouse_rel)

#######################################
# Generic methods.

    def __connect(self):
        """Connects slot methods to member object signal methods.

        Args:
            None.
        Returns:
            Nothing.
        """
        self.player.sig_play_pause_clicked = self.toggle_sim
        self.player.sig_stop_clicked = self.stop_sim
        self.player.sig_reset_clicked = self.reset_sim
        self.moon.sig_moon_clicked = self.move_moon
        self.moon.sig_arrow_clicked = self.move_arrow

    def __get_clicked(self, x, y):
        """Routes a mouse position to the object that contains it.
            
        Args:
            x (int): Mouse x-coordinate.
            y (int): Mouse y-coordinate.

        Returns:
            tuple (two elements): First element is the object that
                contains the mouse point. The second object is
                specific to the object and may be None.

        If no responsive object contains the mouse point, then the
        renturn value is (None, None).
        """
        if model.engine.inrect(x, y, self.moon):
            return self.moon, ind.MOON
        elif self.moon.chk_in_arrow(x, y):
            return self.moon, ind.ARROW
        elif model.engine.inrect(x, y, self.player):
            return self.player, None
        else:
            return None, None
