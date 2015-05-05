import pyglet
from pyglet import gl
from resources import const

class Viewer():
    """Manages the display graphics for a window object."""
    
    def __init__(self, window):
        """Initialization.

        Args:
            window (pyglet.window.Window): Window object that the
                viewer will be managing.
        """
        pyglet.gl.glClearColor(*const.MAIN_WIN_CLEAR_CLR)
        self.arrow = {'vis': False}
        self.path = {'vis': False}
        self.label = pyglet.text.Label(
            font_name=const.MOON_PAR_LBL_FONT,
            color=const.MOON_PAR_LBL_PS_CLR,
            font_size=const.MOON_PAR_LBL_SIZE,
            multiline=True,
            width=window.width,
            anchor_x='left',
            anchor_y='bottom')
        self.show_label = False

#######################################
# Generic methods.

    def paint(self, window, graphics_batch):
        """Paints all graphics given their current rendering.
    
        Args:
            window (pyglet.window.Window): Window being painted.
            graphics_batch (pyglet.graphics.Batch): Graphics batch
                of objects with draw methods to be painted.

        Returns:
            Nothing.

        Before calling the paint method, all objects should be
        correctly rendered using the render methods. After painting,
        objects with toggled visibility have their visibilies set to
        False. These objects are made visible again by calling the
        appropriate rendering methods.
        """
        window.clear()

        # Setup openGL with alpha channel.
        gl.glEnable(gl.GL_BLEND)
        gl.glBlendFunc(gl.GL_SRC_ALPHA, gl.GL_ONE_MINUS_SRC_ALPHA)
        gl.glMatrixMode(gl.GL_MODELVIEW)
        gl.glLoadIdentity()

        # Draw all the objects.
        if self.arrow['vis'] == True:
            gl.glTranslatef(self.arrow['loc'].x, self.arrow['loc'].y, 0)
            gl.glRotatef(self.arrow['ang'], 0, 0, 1)
            pyglet.graphics.draw(self.arrow['numv'], gl.GL_TRIANGLE_FAN,
                ("v2f", self.arrow['ver']), ("c4f", self.arrow['clr']))
            gl.glLoadIdentity()
            self.arrow['vis'] = False
        if self.path['vis'] == True:
            pyglet.graphics.draw(self.path['numv'], gl.GL_LINE_STRIP,
                ("v2f", self.path['ver']), ("c4f", self.path['clr']))
            gl.glLoadIdentity()
            self.path['vis'] = False
        graphics_batch.draw()
        if self.show_label:
            self.label.draw()
            self.show_label = False

    def render_arrow(self, moon):
        """Renders the moon velocity arrow for painting.
        
        Args:
            moon (Moon): Moon object with velocity arrow to be
                rendered.

        Returns:
            Nothing.

        Sets up the self.arrow member dictionary with all the data
        required for openGL painting and sets the visibility of the
        arrow to True.
        """
        self.arrow['vis'] = True
        self.arrow['ver'], self.arrow['numv'] = moon.get_velocity_arrow()
        self.arrow['loc'] = moon.locus
        self.arrow['ang'] = moon.velocity.angle_deg()
        self.arrow['clr'] = const.MOON_ARROW_CLR * self.arrow['numv']

    def render_path(self, moon):
        """Renders path traveled by moon in current simulation.

        Args:
            moon (Moon): Moon object with path to be rendered.
        
        Returns:
            Nothing.

        Sets up the self.path member dictionary with all the data
        required for openGL painting and sets the visibility of the
        path to True. The path is draw such that line segments fade
        to 100% transparency as they get further from the moon.
        """
        colors = list()
        num_ver = len(moon.path) // 2
        for x in range(1, num_ver + 1):
            colors.extend(const.MOON_PATH_CLR[:3] + (x / num_ver,))
        self.path['vis'] = True
        self.path['ver'] = tuple(moon.path)
        self.path['numv'] = num_ver
        self.path['clr'] = tuple(colors)
        
    def render_label(self, energy, moon, fps, state, mode):
        """Renders the data label for the simulation.
            
        Args:
            energy (dict of float): Contains the energy parameters.
            moon (Moon): Moon object being simulated.
            fps (float): Current frames per second.
            state (string): Current state of the simulation.
            mode (string): Current mode of the simulation.

        Returns:
            Nothing.

        Uses the MOON_PAR_LBL_STRING to format the parameters. The
        color is set based on the simulation state, mode and whether
        the moon has crashed or not. Sets the visibility of the label
        to True.
        """
        self.label.text = const.MOON_PAR_LBL_STRING.format(
            energy['total'], energy['kinetic'], energy['potential'],
            moon.locus.x, moon.locus.y,
            moon.velocity.x, moon.velocity.y, fps)
        self.label.color = {
            'running': const.MOON_PAR_LBL_RUN_CLR,
            'paused': const.MOON_PAR_LBL_PS_CLR,
            'stopped': const.MOON_PAR_LBL_PS_CLR}[state]
        if mode in ['moving_moon', 'moving_arrow']:
            self.label.color = const.MOON_PAR_LBL_MOVE_CLR
        if moon.crashed:
            self.label.color = const.MOON_PAR_LBL_CRASH_CLR
        self.show_label = True
