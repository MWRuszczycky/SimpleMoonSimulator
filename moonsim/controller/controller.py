import copy
import pyglet
import model
import view.viewer
import resources.images
from pyglet.window import mouse
from model.engine import Vector
from resources import const

class Controller(pyglet.window.Window):
    """Manages the simulation, window and events."""

    def __init__(self, draw_label=False):
        """Initialization.

        Args:
            draw_label (bool): Flag for whether the simulation
                label should be drawn.
        """
        config = pyglet.gl.Config(
            double_buffer=True, sample_buffers=1, samples=4)
        super().__init__(
            width=const.MAIN_WIN_WIDTH,
            height=const.MAIN_WIN_HEIGHT,
            caption=const.MAIN_WIN_TITLE,
            config=config)
        # Initialize the simulation master data object.
        self.simstate = 'stopped'
        self.simmode = 'ready'
        self.simoptions = {'draw_label': draw_label}
        self.resets = {
            'init_loc': Vector(const.MOON_INIT_LOCX, const.MOON_INIT_LOCY),
            'init_vel': Vector(const.MOON_INIT_VELX, const.MOON_INIT_VELY),
            'last_loc': Vector(const.MOON_INIT_LOCX, const.MOON_INIT_LOCY),
            'last_vel': Vector(const.MOON_INIT_VELX, const.MOON_INIT_VELY)}

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
            locus=Vector(const.MOON_INIT_LOCX, const.MOON_INIT_LOCY),
            velocity=Vector(const.MOON_INIT_VELX, const.MOON_INIT_VELY),
            batch=self.graphics_batch)

        self.player = model.player.Player(
            start_img=resources.images.start_button,
            pause_img=resources.images.pause_button,
            stop_img=resources.images.stop_button,
            reset_img=resources.images.reset_button,
            x=const.MAIN_WIN_WIDTH,
            y=const.MAIN_WIN_HEIGHT,
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
        if self.simstate in ['stopped', 'paused'] and not self.moon.crashed:
            self.viewer.render_arrow(self.moon)
        self.viewer.render_path(self.moon)
        energy = model.engine.energy(
            self.moon, self.planets, gravity=const.GRAVITY)
        if self.simoptions['draw_label']:
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
        if self.simmode in ['moving_moon', 'moving_arrow']:
            self.resets['last_loc'] = copy.deepcopy(self.moon.locus)
            self.resets['last_vel'] = copy.deepcopy(self.moon.velocity)
        self.simmode = 'ready'

    def on_mouse_drag(self, x, y, dx, dy, buttons, modifiers):
        """Handler for mouse-drag events."""
        if not mouse.LEFT & buttons:
            return
        if self.simmode == 'moving_moon':
            self.move_moon(x, y)
        elif self.simmode == 'moving_arrow':
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
        if self.simstate == 'running':
            pyglet.clock.unschedule(self.update)
            self.simstate = 'paused'
            self.player.pause()
        else:
            self.simstate = 'running'
            self.player.play()
            self.simmode = 'ready'
            pyglet.clock.schedule_interval(self.update, 1 / const.FRAME_RATE)

    def stop_sim(self):
        """Stops simulation and resets moon to initial state.

        Args:
            None.
        Returns:
            Nothing.
        """
        if self.simstate == 'running':
            pyglet.clock.unschedule(self.update)
        self.simstate = 'stopped'
        self.player.stop()
        self.simmode = 'ready'
        self.moon.reset(self.resets['init_loc'], self.resets['init_vel'])

    def reset_sim(self):
        """Stops simulation and resets moon to last start state.
            
        Args:
            None.
        Returns:
            Nothing.
        """
        if self.simstate == 'running':
            pyglet.clock.unschedule(self.update)
        self.simstate = 'stopped'
        self.player.reset()
        self.simmode = 'ready'
        self.moon.reset(self.resets['last_loc'], self.resets['last_vel'])

    def move_moon(self, x, y):
        """Repositions the moon based on bouse input.
        
        Args:
            x (float): New mouse-x coordinate for moon center.
            y (float): New mouse-y coordinate for moon center.

        Returns:
            Nothing.
        """
        if self.simstate in ['paused', 'stopped'] and not self.moon.crashed:
            self.simmode = 'moving_moon'
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
        if self.simstate in ['paused', 'stopped'] and not self.moon.crashed:
            self.simmode = 'moving_arrow'
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
            return self.moon, 'moon'
        elif self.moon.chk_in_arrow(x, y):
            return self.moon, 'arrow'
        elif model.engine.inrect(x, y, self.player):
            return self.player, None
        else:
            return None, None
