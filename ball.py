# class Ball
try:
    from Shared import *
    # from player import *
except ImportError as err:
    print("couldn't load module. %s" % err)
    sys.exit(2)


class Ball(SharedSprite):
    """A ball that will move across the screen"""


    def __init__(self, players, net, pointer):
        SharedSprite.__init__(self, 'BigBall1.png')