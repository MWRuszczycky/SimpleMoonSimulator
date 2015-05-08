import sys
import pyglet
import resources.indices as ind
from controller import controller, startup

parameters = startup.get_parameters(sys.argv[1:])
if parameters[ind.RUN_SIM]:
    simulation = controller.Controller(
        disp_par=parameters[ind.DISP_PAR],
        planet_locx=parameters[ind.INIT_PLANET_LOCX],
        planet_locy=parameters[ind.INIT_PLANET_LOCY],
        moon_locx=parameters[ind.INIT_MOON_LOCX],
        moon_locy=parameters[ind.INIT_MOON_LOCY],
        moon_velx=parameters[ind.INIT_VELX],
        moon_vely=parameters[ind.INIT_VELY],
        win_width=parameters[ind.WIN_WIDTH],
        win_height=parameters[ind.WIN_HEIGHT])
    pyglet.app.run()
else:
    sys.exit(0)
