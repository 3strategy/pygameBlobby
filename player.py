# classes Bat, and Net
try:
    from Shared import *

except ImportError as err:
    print("couldn't load module. %s" % err)
    sys.exit(2)


class Player(SharedSprite):
    """Movable blobby person that hits the ball"""


    def __init__(self, side):
        self.side = side

        if side == "left":
            SharedSprite.__init__(self, 'blobbyred.webp',0.4,True)

        elif "right" == side:
            SharedSprite.__init__(self, 'blobbygreen.webp',0.4)