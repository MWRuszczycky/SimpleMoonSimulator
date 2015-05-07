# Startup parameters indices.
RUN_SIM =           1000 # Run simulation flag.
DISP_PAR =          1001 # Display moon simulation parameters flag.
INIT_LOCX =         1002 # Initial x-coordinate of moon.
INIT_LOCY =         1003 # Initial y-coordinate of moon.
INIT_VELX =         1004 # Initial x-velocity of moon.
INIT_VELY =         1005 # Initial y-velocity of moon.
WIN_WIDTH =         1007 # Main window width.
WIN_HEIGHT =        1006 # Main window height.

# Object identifiers.
MOON =              2000 # Body of moon.
ARROW =             2001 # Moon velocity arrow.

START_BTN =         2100 # Start button on simulation player.
PAUSE_BTN =         2101 # Pause button on simulation player.
STOP_BTN =          2102 # Stop button on simulation player.
RESET_BTN =         2103 # Reset button on simulation player.

# Simulation states.
RUNNING =           3000
STOPPED =           3001
PAUSED =            3002

# Simulation modes.
READY =             3100
MOVE_MOON =         3101
MOVE_ARROW =        3102

# Initial value indices for use in the controller.resets dict.
INIT_LOC =          4000
INIT_VEL =          4001
LAST_LOC =          4002
LAST_VEL =          4003

# Indices for energy dict.
TOTAL =             4100
KINETIC =           4101
POTENTIAL =         4102

# OpenGL vertex dict keys.
VIS =               5000 # Vertices are visible.
VER =               5001 # Vertex list.
LOC =               5002 # Translation vector for rendering vertices.
ANG =               5003 # Rotational angle for rendering vertices.
CLR =               5004 # Color list for vertex list.
NMV =               5005 # Number of vetices.

