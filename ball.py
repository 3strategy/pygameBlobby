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
        SharedSprite.__init__(self, 'VolleyGreen.png', 0.45)  # if using unusual size - use the scale to make it ok.
        self.hit = 0
        self.players = players  # type hinting is important. it helps seeing available methods in the class
        self.lastPlayer = False
        self.point_started = False
        self.point_scored = False
        self.net: Net = net  # hinting.

        self.dyfix = self.rect.height / 2
        self.dxfix = self.rect.width / 2
        self.startY = 320 * basescale

        self.reinit()

    # call this each time a new point begins, to reset parameters and position.
    def reinit(self):
        self.point_started = False
        self.point_scored = False
        self.dX, self.dY = 0.0, 0 * basescale
        if self.lastPlayer:
            self.rect.center = (self.initial_wall_dist, self.startY)
        else:
            self.rect.center = (self.area.midright[0] - self.initial_wall_dist, self.startY)

        for player in self.players:
            player.reinit()

    def score(self):
        ordinal = self.area.centerx > self.rect.centerx
        if not self.point_scored:  # prevent double scoring
            if ordinal == self.lastPlayer:  # ball holder lost the point - switch ball.
                self.lastPlayer = not self.lastPlayer
            else:
                self.players[ordinal].score += 1
            self.point_scored = True

    def update(self, *args):
        oldpos = self.rect
        if self.point_started and self.dY < 14 * basescale:
            self.dY += self.gravity
        newpos = self.rect.move(self.dX, self.dY)

        # Test if touching the floor
        if newpos.bottom >= self.area.bottom:  # Ball touches the floor
            newpos.bottom = self.area.bottom  # repositioning to a valid position.
            self.dY = -0.6 * self.dY

            # give score according to court side:
            self.score()

            # once point was scored, start a new point when ball settles down
            if -2 < self.dY < 2:
                self.reinit()
                return  # a crucial return.

        # Test if flying too high
        elif self.rect.top < -200 * basescale and self.dY < 0:
            print(f'sky high {self.rect.top} dX:{self.dX:.1f} dY:{self.dY:.1f}')
            self.rect.top -= self.dY
            self.dY = -self.dY

        # Ball off court's sides:
        if (newpos.right > self.area.right and self.dX > 0) or (newpos.left < 0 and self.dX < 0):
            newpos.left -= self.dX
            self.rect.left -= self.dX
            self.dX = -self.dX
            return

        # Net colision detection בדיקת התנגשות ברשת
        if overlap_net := testoverlap(self.net, self):
            if overlap_net[1] < 68 * basescale:  # real net impact means ball is touched on the side
                self.score()
                self.rect.left -= self.dX
                self.dX = -0.3 * self.dX
                return
            else:  # hit top of net
                self.dY -= 5
                self.rect = self.rect.move(self.dX, -10 * basescale)
                return

        self.rect = newpos
        # Player Collision testing
        for ordinal in range(2):
            player = self.players[ordinal]
            # overlap gets the result of the collision test and then an 'if' checks overlap
            # if there was no collision overlap will be None (i.e. False)
            # if there is a collision, overlap contains the information.
            if overlap := testoverlap(player, self):  # EXPRESSION ASSIGNMENT

                # reset num_shots of the THE OTHER PLAYER
                self.players[not ordinal].num_shots = 0
                player.num_shots += 1
                if player.num_shots > 3:
                    player.state = "3-touch"  # putting debug info here (since point is over)
                    self.score()  # give point to other side.
                    return  # here it's just like writing else:

                self.point_started = True  # from here on gravity will apply.
                # handle the collision:
                # calculating the angle of collision (to bounce the ball accordingly).
                impact_gamma = angle_ofdxdy((overlap[0] - self.dxfix, (overlap[1] - self.dyfix)))[0]

                x = (self.dX, self.dY), (player.dX, player.dY)
                # the effect of the collision is calculated by Impulse Equations.
                # dX and dY of ball and player will be sent as input,
                # and also be returned back from the impulse function.
                ((self.dX, self.dY), (player.dX, player.dY)) = calc_impulse_xy1xy2(x, 1, 3.5, impact_gamma)
                self.rect = oldpos
                return  # no need to check the other player.
