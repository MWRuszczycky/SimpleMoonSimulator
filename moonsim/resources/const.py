#######################################
# Main window parameters.

# Main window default dimensions.
MAIN_WIN_WIDTH = 1200
MAIN_WIN_HEIGHT = 1000
# Main window title.
MAIN_WIN_TITLE = "Moon Simulation"
# Screen clear color.
MAIN_WIN_CLEAR_CLR = (0, 0, 0, 255)

#######################################
# Initial parameters for the planet.

# Location.
PLANET_INIT_LOCX = 600
PLANET_INIT_LOCY = 500
# Mass.
PLANET_MASS = 81.348            # Moon masses.

#######################################
# Parameters for the moon.

# Initial location (perigee).
MOON_INIT_LOCX = 357.80         # px
MOON_INIT_LOCY = 500            # px
# Mass.
MOON_MASS = 1
# Initial velocity.
MOON_INIT_VELX = 0              # px/s
MOON_INIT_VELY = 25.824         # px/s
# Moon tail path color.
MOON_PATH_CLR = (0.89, 0.80, 0.45, 1.0)
# Moon velocity arrow color.
MOON_ARROW_CLR = (0.0, 1.0, 0.0, 0.5)
# Dimensions of velocity arrow (along x-axis).
# Length and width scaling.
MOON_ARROW_LEN_SCALE = 2        # Velocity scale to get base length.
MOON_ARROW_WIDTH_SCALE = 2 / 5  # Frac moon width to get base width.
MOON_ARROW_BASE_SHIFT = 0.7     # Times moon width gives base start.
# Arrow head dimensions
MOON_ARROW_HDX = 12             # x-dimension to rectangular base.
MOON_ARROW_HDXFULL = 16         # Full x-dimension.
MOON_ARROW_HDY = 30             # Full y-dimension.

#######################################
# Physical constants and conversion factors.

# Gravity constant.
GRAVITY = 1881.6  # (px)^3 * (moon mass)^(-1) * (simulation sec)^(-2)
# Distance conversion: 1500 kilometers per pixel.
KM_PER_PX = 1500
# Time conversion: 10 hours (36000 seconds) per second of simulation.
HR_PER_SEC = 10

#######################################
# Screen label for moon parameters.

# Format string.
MOON_PAR_LBL_STRING ="\
TE: {:10.1f}\n\
KE: {:10.1f}\n\
PE: {:10.1f}\n\
x: {:11.1f}\n\
y: {:11.1f}\n\
dx/dt: {:7.1f}\n\
dy/dt: {:7.1f}\n\
FPS: {:9.1f}"
MOON_PAR_LBL_LOCX = 5
MOON_PAR_LBL_LOCY = 5
MOON_PAR_LBL_WIDTH = 200
MOON_PAR_LBL_FONT = "monospace"
MOON_PAR_LBL_SIZE = 11
MOON_PAR_LBL_RUN_CLR = (200, 200, 200, 255)     # running
MOON_PAR_LBL_PS_CLR = (58, 193, 255, 255)       # stopped/paused
MOON_PAR_LBL_CRASH_CLR = (255, 73, 91, 255)     # running and crashed
MOON_PAR_LBL_MOVE_CLR = (73, 191, 172, 255)     # user changing moon

#######################################
# Simulation defaults.

# Target frame rate
FRAME_RATE = 60     # frames per second
# Frame interval subdivision for numerical integration.
FRAME_DIVS = 100
