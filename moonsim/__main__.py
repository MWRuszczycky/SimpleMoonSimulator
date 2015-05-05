import sys
import getopt
import pyglet
from controller import controller

def get_parameters(argv):
    parameters = {
        'draw_label': False}
    try:
        opts, args = getopt.getopt(argv, "l", ["label"])
    except getopt.GetoptError:
        print("bad usage")
        sys.exit(2)
    for opt, arg in opts:
        if opt == "-l" or opt == "--label":
            parameters['draw_label'] = True
    return parameters

if __name__ == "__main__":    
    parameters = get_parameters(sys.argv[1:])
    simulation = controller.Controller(draw_label=parameters['draw_label'])
    pyglet.app.run()
