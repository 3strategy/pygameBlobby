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
        self.speed = speed
        self.horisontal_speed = speed * 0.3

        if side == "left":
            SharedSprite.__init__(self, 'blobbyred.webp',0.4,True)
            self.sign = 1
            self.upKey = K_d
            self.downKey = K_LALT
            self.leftKey = K_a
            self.rightKey = K_c
        elif "right" == side:
            SharedSprite.__init__(self, 'blobbygreen.webp',0.4)
            self.sign = -1
            self.upKey = K_UP
            self.downKey = K_DOWN
            self.leftKey = K_LEFT
            self.rightKey = K_RIGHT

    def move(self, event: pygame.event):
        if event.type == KEYDOWN:  # we only want to trigger a move on keydown.

            if event.key == self.rightKey:  # and (self.h_state == "still" or self.h_state == "moveleft"):
                self.moveright()
            elif event.key == self.leftKey:  # and (self.h_state == "still" or self.h_state == "moveright"):
                self.moveleft()


    def update(self):
        self.rect = self.rect.move(self.dX, self.dY)
        pygame.event.pump()

    def moveright(self):
        self.dX = self.horisontal_speed
        self.h_state = "moveright"

    def moveleft(self):
        self.dX = -self.horisontal_speed
        self.h_state = "moveleft"
