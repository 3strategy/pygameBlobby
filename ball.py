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
        SharedSprite.__init__(self, 'VolleyGreen.png', 0.55)  # if using unusual size - use the scale to make it ok.
        self.hit = 0
        self.players = players  # type hinting is important. it helps seeing available methods in the class
        self.lastPlayer = False
        self.point_started = False
        self.point_scored = False
        self.net: Net = net  # hinting.
        self.pointer: Pointer = pointer
        self.dyfix = self.rect.height / 2
        self.dxfix = self.rect.width / 2
        self.startY = 320 * basescale

        self.reinit()

    # call this each time a new point begins, to reset parameters and position.
    def reinit(self):
        self.point_started = False
        self.point_scored = False
        if self.lastPlayer:
            self.rect.center = (self.initial_wall_dist, self.startY)
        else:
            self.rect.center = (self.area.midright[0] - self.initial_wall_dist, self.startY)

        for player in self.players:
            player.reinit()

        SharedSprite.reinit(self)

    def score(self):
        ordinal = self.area.centerx > self.rect.centerx
        if not self.point_scored:  # prevent double scoring
            if ordinal == self.lastPlayer:  # ball holder lost the point - switch ball.
                self.lastPlayer = not self.lastPlayer
            else:
                self.players[ordinal].score += 1
            self.point_scored = True

    def update(self, *args):
        SharedSprite.update(self)
        newpos, area = self.newpos, self.area
        self.pointer.rect.centerx = newpos.centerx
        # you can do the above pointing but you cannot do:
        # dY,dX = self.dY, self.dX  # WHY?
        if self.point_started and self.dY < 14 * basescale:
            self.dY += self.gravity

        # Test if touching the floor האם הכדור נוגע ברצפה
        if newpos.bottom >= area.bottom:  # Ball touches the floor
            newpos.bottom = area.bottom  # repositioning to a valid position.
            self.dY = -0.6 * self.dY
            self.score()

            # once point was scored, start a new point when ball settles down
            if -2 * basescale < self.dY < 2 * basescale:
                self.reinit()
                return  # a crucial return.

        # Test if flying too high בדיקה אם הכדור עף גבוה מדי
        elif newpos.top < -250 * basescale and self.dY < 0:
            print(f'sky high {newpos.top} dX:{self.dX:.1f} dY:{self.dY:.1f}')
            newpos.top -= self.dY
            self.dY = -self.dY

        # Ball off court's sides: בדיקה אם הכדור פוגע בקירות
        if (newpos.right > area.right and self.dX > 0) or (newpos.left < 0 and self.dX < 0):
            newpos.left -= self.dX
            self.dX = -self.dX

        # Net collision detection בדיקת התנגשות ברשת
        if overlap_net := testoverlap(self.net, self):
            self.rollback()  # Rollback position
            if overlap_net[1] < 68 * basescale:  # real net impact means ball is touched on the side
                self.score()
                self.dX = -0.3 * self.dX
            else:  # hit top of net
                self.dY -= 5

        # Player Collision testing בדיקת פגיעת שחקן בכדור
        for ordinal in range(2):
            player = self.players[ordinal]
            # overlap gets the result of the collision test and then an 'if' checks overlap
            if bestoverlap := testoverlap(player, self):  # EXPRESSION ASSIGNMENT
                print(f'\ninitial ball new:{self.newpos.center} old:{self.oldpos.center},\
                    pla new:{player.newpos.center} old:{player.oldpos.center}')
                # initial_gamma = angle_ofdxdy((bestoverlap[0] - self.dxfix, (bestoverlap[1] - self.dyfix)))[0]

                # reset num_shots of the THE OTHER PLAYER
                self.players[not ordinal].num_shots = 0
                if not self.point_scored:
                    player.num_shots += 1
                if player.num_shots > 3:
                    player.state = "3-touch"  # putting debug info here (since point is over)
                    # print(f'{datetime.now()}  3touch history ball:{self.oldpos.bottom}\
                    #     {self.old1.bottom} {self.old2.bottom} oldest{self.old3.bottom}')
                    # print(f'bl dY:{self.dY:.1f} {self.dY0:.1f} {self.dY1:.1f} {self.dY2:.1f} oldest: {self.dY3:.1f}')
                    self.score()  # give point to other side.
                    return

                # calculate best possible impact (without rolling back player:
                for i in range(4):
                    self.rect = average_rect(self.newpos, self.oldpos)
                    player.rect = average_rect(player.newpos, player.oldpos)
                    if overlap := testoverlap(player, self):
                        self.newpos, player.newpos = self.rect, player.rect
                        bestoverlap = overlap
                    else:
                        self.oldpos, player.oldpos = self.rect, player.rect

                weight = (300 if player.newpos.bottom == area.bottom else 3)
                self.point_started = True  # from here on gravity will apply.
                # the effect of the collision is calculated by Impulse Equations.
                impact_gamma = angle_ofdxdy((bestoverlap[0] - self.dxfix, (bestoverlap[1] - self.dyfix)))[0]
                x = (self.dX, self.dY), (player.dX, player.dY)
                ((self.dX, self.dY), (player.dX, player.dY)) = calc_impulse_xy1xy2(x, 1, weight, impact_gamma)

                # if abs(initial_gamma-impact_gamma) > 0.09:
                #     print(f'\nfinal ball new:{self.newpos.center} old:{self.oldpos.center}, \
                #     pla new:{player.newpos.center} old:{player.oldpos.center}\n\
                #     initial gamma:{degrees(initial_gamma):.0f}->{degrees(impact_gamma):.0f}')
                #     print('helped')

                # rollback both Ball and Player positions
                self.rollback(player)
                # check no collision and break if collision to debug
                assert not testoverlap(player, self)
                return  # no need to check the other player.
