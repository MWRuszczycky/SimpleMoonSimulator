import sys
import getopt
import pyglet
import resources.indices as ind
from controller import controller

def get_parameters(argv):
    parameters = {
        ind.DRAW_LABEL: False}
    try:
        opts, args = getopt.getopt(argv, "l", ["label"])
    except getopt.GetoptError:
        sys.stderr.write("bad usage\n")
        sys.exit(2)
    for opt, arg in opts:
        if opt == "-l" or opt == "--label":
            parameters[ind.DRAW_LABEL] = True
    return parameters

if __name__ == "__main__":    
    parameters = get_parameters(sys.argv[1:])
    simulation = controller.Controller(draw_label=parameters[ind.DRAW_LABEL])
    pyglet.app.run()
