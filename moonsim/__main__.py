import sys
import pyglet
import resources.indices as ind
from controller import controller, startup

parameters = startup.get_parameters(sys.argv[1:])
if parameters[ind.RUN_SIM]:
    simulation = controller.Controller(
        disp_par=parameters[ind.DISP_PAR],
        moon_locx=parameters[ind.INIT_LOCX],
        moon_locy=parameters[ind.INIT_LOCY],
        moon_velx=parameters[ind.INIT_VELX],
        moon_vely=parameters[ind.INIT_VELY],
        win_width=parameters[ind.WIN_WIDTH],
        win_height=parameters[ind.WIN_HEIGHT])
    pyglet.app.run()
else:
    sys.exit(0)
