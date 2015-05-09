#######################################
# Version.

VERSION = "moonsim 0.1.0\n"

#######################################
# Main window parameters.

# Main window default dimensions.
MAIN_WIN_WIDTH = 800
MAIN_WIN_HEIGHT = 800
# Maximum and minimum window dimensions.
MAIN_WIN_MAXX = 1200
MAIN_WIN_MAXY = 1000
MAIN_WIN_MINX = 200
MAIN_WIN_MINY = 200
# Main window title.
MAIN_WIN_TITLE = "A Simple Moon Simulator"
# Screen clear color.
MAIN_WIN_CLEAR_CLR = (0, 0, 0, 255)

#######################################
# Startup argument list.

STARTUP_LONG = [
    "version",
    "display",
    "perigee",
    "apogee",
    "license",
    "help"]

STARTUP_SHORT = "dpalh"

#######################################
# Initial parameters for the planet.

# Location.
DEL_PLANET_INIT_LOCX = 0
DEL_PLANET_INIT_LOCY = 0
# Mass.
PLANET_MASS = 81.348            # Moon masses.

#######################################
# Parameters for the moon.

# Mass.
MOON_MASS = 1
# Initial location (perigee).
DEL_MOON_PER_LOCX = - 242.20    # px
DEL_MOON_PER_LOCY = 0           # px
# Initial velocity (perigee).
MOON_PER_VELX = 0               # px/s
MOON_PER_VELY = 25.824          # px/s
# Initial location (apogee).
DEL_MOON_APO_LOCX = 270.33      # px
DEL_MOON_APO_LOCY = 0           # px
# Initial velocity (apogee).
MOON_APO_VELX = 0               # px/s
MOON_APO_VELY = -23.136         # px/s

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
HR_PER_SIMSEC = 10
DAY_PER_SIMSEC = HR_PER_SIMSEC / 24
SIMSEC_PER_YEAR = 365.25 / DAY_PER_SIMSEC
# Energy.
TJ_PER_SIMENERGY = 1.2747e14

#######################################
# Screen label for moon parameters.

# Format string.
MOON_PAR_LBL_STRING ="\
t: {:14.1f} days\n\
TE: {:+13.3e} TJ\n\
KE: {:+13.3e} TJ\n\
PE: {:+13.3e} TJ\n\
r: {:+14.3e} km\n\
speed: {:+10.3e} km/h\n\
dx/dt: {:+7.3e} km/h\n\
dy/dt: {:+7.3e} km/h\n\
FPS: {:12.1f} fps"
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

#######################################
# Strings: Error messages.

# Message when unrecognized command used at startup.
BADCMDMSG_STR = "\
Unrecognized command (see 'moonsim -h').\n"
# Message when unrecognized arguments used at startup.
BADARGMSG_STR = "\
Unrecognized arguments (see 'moonsim -h').\n"
# Message when improper window dimensions requested.
BADWINDIMMSG_STR = "\
Bad window dimensions:\n\
    {minwidth:d} < width < {maxwidth:d}\
    {minheight:d} < height < {maxheight:d}\n".format(
    minwidth=MAIN_WIN_MINX - 1, maxwidth=MAIN_WIN_MAXX + 1,
    minheight=MAIN_WIN_MINY - 1, maxheight=MAIN_WIN_MAXY + 1)
# Error message when image resources cannot be found.
BADIMGRES_STR = "Cannot load image resources.\n"
