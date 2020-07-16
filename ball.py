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
        self.net: Net = net  # hinting.

        self.dyfix = self.rect.height / 2
        self.dxfix = self.rect.width / 2

    def score(self, ordinal):
        if not self.point_scored:  # prevent double scoring
            if ordinal == self.lastPlayer:  # ball holder lost the point - switch ball.
                self.lastPlayer = not self.lastPlayer
            else:
                self.players[ordinal].score += 1
            self.point_scored = True

    def update(self, *args):

        # if self.point_started and self.dY < 14 * basescale:
        self.dY += self.gravity
        newpos = self.rect.move(self.dX, self.dY)

        # Test if touching the floor
        if newpos.bottom >= self.area.bottom:  # Ball touches the floor
            newpos.bottom = self.area.bottom  # repositioning to a valid position.
            self.dY = -0.6 * self.dY

            if not self.point_scored:  # give score according to court side:
                side = self.area.centerx - self.rect.centerx > 0
                self.score(side)

        # Ball off court's sides:
        if (newpos.right > self.area.right and self.dX > 0) or (newpos.left < 0 and self.dX < 0):
            newpos.left -= self.dX
            self.rect.left -= self.dX
            self.dX = -self.dX
            return

        # Net colision detection בדיקת התנגשות ברשת
        if overlap_net := testoverlap(self.net, self):
            if overlap_net[1] < 68 * basescale:  # real net impact means ball is touched on the side
                side = self.area.centerx - self.rect.centerx > 0
                self.score(side)  # give score according to court side:
                self.rect.left -= self.dX
                self.dX = -0.3 * self.dX
                return
            else:  # hit top of net
                self.dY -= 5
                self.rect = self.rect.move(self.dX, -10 * basescale)
                return

        # Player Collision testing
        for player in self.players:
            # overlap gets the result of the collision test and then an 'if' checks overlap
            # if there was no collision overlap will be None (i.e. False)
            # if there is a collision, overlap contains the information.
            if overlap := testoverlap(player, self):  # EXPRESSION ASSIGNMENT
                # handle the collision:
                # calculating the angle of collision (to bounce the ball accordingly).
                impact_gamma = angle_ofdxdy((overlap[0] - self.dxfix, (overlap[1] - self.dyfix)))[0]

                x = (self.dX, self.dY), (player.dX, player.dY)
                # the effect of the collision is calculated by Impulse Equasions.
                # dX and dY of ball and player will be sent as input,
                # and also be returned back from the impulse function.
                ((self.dX, self.dY), (player.dX, player.dY)) = calc_impulse_xy1xy2(x, 1, 3.5, impact_gamma)

                break  # no need to check the other player.

        self.rect = newpos
