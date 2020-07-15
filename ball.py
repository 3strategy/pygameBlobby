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
        self.hit = 0
        self.players = players  # type hinting is important. it helps seeing available methods in the class
        self.lastPlayer = False
        self.point_started = False
        self.point_scored = False


    def score(self, ordinal):
        if not self.point_scored:  # prevent double scoring
            if ordinal == self.lastPlayer:  # ball holder lost the point - switch ball.
                self.lastPlayer = not self.lastPlayer
            else:
                self.players[ordinal].score += 1
            self.point_scored = True

    def update(self, *args):

        #if self.point_started and self.dY < 14 * basescale:
        self.dY += self.gravity
        newpos = self.rect.move(self.dX, self.dY)

        #Test if touching the floor
        if newpos.bottom >= self.area.bottom: #player touches the floor
            newpos.bottom = self.area.bottom #repositioning to a valid position.
            self.dY = -self.dY

            if not self.point_scored:  # give score according to court side:
                side = self.area.centerx - self.rect.centerx > 0
                self.score(side)

        self.rect = newpos
