# classes Bat, and Net
try:
    from Shared import *

except ImportError as err:
    print("couldn't load module. %s" % err)
    sys.exit(2)


class Player(SharedSprite):
    """Movable blobby person that hits the ball"""
    netApproach = 49 * basescale
    sideApproach = 39 * basescale

    def __init__(self, side):
        self.side = side
        self.speed = speed
        self.horisontal_speed = speed * 0.3
        self.state = "still"
        self.h_state = "still"

        self.canjump = True
        self.score = 0

        if side == "left":
            SharedSprite.__init__(self, 'blobbyred.webp', 0.4, True)
            self.sign = 1
            self.upKey = K_d
            self.downKey = K_LALT
            self.leftKey = K_a
            self.rightKey = K_c
        elif "right" == side:
            SharedSprite.__init__(self, 'blobbygreen.webp', 0.4)
            self.sign = -1
            self.upKey = K_UP
            self.downKey = K_DOWN
            self.leftKey = K_LEFT
            self.rightKey = K_RIGHT

        self.gravity = gravity * 3

    def move(self, event: pygame.event):
        if event.type == KEYDOWN:  # we only want to trigger a move on keydown.
            if event.key == self.upKey:
                self.moveup()

            if event.key == self.rightKey:
                self.moveright()
            elif event.key == self.leftKey:
                self.moveleft()

        elif event.type == KEYUP:
            # some key up should trigger "stand still", (e.g. the upKey is depressed while moving up)
            if self.state == "moveup" and event.key == self.upKey \
                    or (self.state == "movedown" and event.key == self.downKey):
                self.standstill()

            if self.h_state == "moveright" and event.key == self.rightKey \
                    or (self.h_state == "moveleft" and event.key == self.leftKey):
                self.h_standstill()

    def update(self):
        newpos = self.rect.move(self.dX, self.dY)

        if self.dX != 0:  # Player horisontal position checks:
            # avoid approaching the net   and avoid exiting the field
            if abs(self.area.centerx - newpos.centerx) < Player.netApproach:
                newpos.centerx -= self.dX
                self.dX = 0
            elif abs(self.area.centerx - newpos.centerx) > self.area.centerx + Player.sideApproach:
                newpos.centerx -= self.dX
                self.dX = 0

        if self.state == "moveup":
            self.dY += 0.6 * self.gravity
        else:
            self.dY += self.gravity

        if newpos.bottom >= self.area.bottom:  # player touches the floor
            newpos.bottom = self.area.bottom
            if self.state == 'moveup':
                self.dY = -self.speed
            else:
                self.dY = 0
            self.canjump = True

        self.rect = newpos
        pygame.event.pump()

    def moveup(self):
        # these are only called once, even if key is held.
        if self.canjump:
            self.dY = -self.speed
            self.canjump = False
        self.state = "moveup"  # register the "intention" in any case: you will not get another keyboard hint...

    def standstill(self):
        self.state = "still"

    def moveright(self):
        self.dX = self.horisontal_speed
        self.h_state = "moveright"

    def moveleft(self):
        self.dX = -self.horisontal_speed
        self.h_state = "moveleft"

    def h_standstill(self):
        self.dX = 0
        self.h_state = "still"
