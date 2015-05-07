import sys
import getopt
import resources.indices as ind
from resources import const

def show_start():
    sys.stdout.write("Start Screen\n")

def show_help():
    sys.stdout.write("Help Screen\n")

def show_license():
    sys.stdout.write("License\n")

def assign_args(par, args):
    if len(args) != 2:
        raise Exception(const.BADARGMSG_STR)
    width = int(args[0])
    height = int(args[1])
    if (width >= const.MAIN_WIN_MINX) and (width <= const.MAIN_WIN_MAXX):
        par[ind.WIN_WIDTH] = width
    else:
        raise Exception(const.BADWINDIMMSG_STR)
    if (height >= const.MAIN_WIN_MINY) and (height <= const.MAIN_WIN_MAXY):
        par[ind.WIN_HEIGHT] = height
    else:
        raise Exception(const.BADWINDIMMSG_STR)

def get_parameters(argv):
    parameters = {
        ind.RUN_SIM: True,
        ind.DISP_PAR: False,
        ind.INIT_LOCX: const.MOON_PER_LOCX,
        ind.INIT_LOCY: const.MOON_PER_LOCY,
        ind.INIT_VELX: const.MOON_PER_VELX,
        ind.INIT_VELY: const.MOON_PER_VELY,
        ind.WIN_WIDTH: const.MAIN_WIN_WIDTH,
        ind.WIN_HEIGHT: const.MAIN_WIN_HEIGHT}
    try:
        opts, args = getopt.getopt(
            argv, const.STARTUP_SHORT, const.STARTUP_LONG)
        if len(args) > 0:
            assign_args(parameters, args)
        for opt, arg in opts:
            if opt in ["-h", "--help"]:
                show_help()
                parameters[ind.RUN_SIM] = False
            elif opt in ["-l", "--license"]:
                show_license()
                parameters[ind.RUN_SIM] = False
            elif opt in ["-d", "--display"]:
                parameters[ind.DISP_PAR] = True
            elif opt in ["-p", "--perigee"]:
                # This is the current default.
                pass
            elif opt in ["-a", "--apogee"]:
                parameters[ind.INIT_LOCX] = const.MOON_APO_LOCX
                parameters[ind.INIT_LOCY] = const.MOON_APO_LOCY
                parameters[ind.INIT_VELX] = const.MOON_APO_VELX
                parameters[ind.INIT_VELY] = const.MOON_APO_VELY
        return parameters
    except getopt.GetoptError:
        sys.stderr.write(const.BADCMDMSG_STR)
        sys.exit(2)
    except Exception as err:
        sys.stderr.write(str(err))
        sys.exit(2)
