import sys
import pyglet
from resources import const

try:
    pyglet.resource.path.append("resources/img")
    pyglet.resource.reindex()

    moon = pyglet.resource.image("grey_moon.png")
    planet = pyglet.resource.image("blue_planet.png")

    start_button = pyglet.resource.image("start_button.png")
    stop_button = pyglet.resource.image("stop_button.png")
    pause_button = pyglet.resource.image("pause_button.png")
    reset_button = pyglet.resource.image("reset_button.png")

    crash_images = [
        pyglet.resource.image("crash/crash_animation0.png"),
        pyglet.resource.image("crash/crash_animation1.png"),
        pyglet.resource.image("crash/crash_animation2.png"),
        pyglet.resource.image("crash/crash_animation3.png"),
        pyglet.resource.image("crash/crash_animation4.png"),
        pyglet.resource.image("crash/crash_animation5.png"),
        pyglet.resource.image("crash/crash_animation6.png"),
        pyglet.resource.image("crash/crash_animation7.png"),
        pyglet.resource.image("crash/crash_animation8.png")]
    crash_frames = [pyglet.image.AnimationFrame(x, 0.05) for x in crash_images]
    crash_frames[-1].duration = None
    crash_animation = pyglet.image.Animation(crash_frames)
except Exception as err:
    sys.stderr.write(const.BADIMGRES_STR)
    sys.stderr.write("Details: {}\n".format(str(err)))
    sys.exit(1)
