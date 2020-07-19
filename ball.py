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
        if overlap_net := self.bestoverlap(self.net):  # testoverlap(self.net, self):
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
            if bestoverlap := self.bestoverlap(player):
                self.process_impact(player,bestoverlap)

                # reset num_shots of the THE OTHER PLAYER
                self.players[not ordinal].num_shots = 0
                if not self.point_scored:
                    player.num_shots += 1
                if player.num_shots > 3:
                    self.score()
                    return

                self.point_started = True  # from here on gravity will apply.
                return  # no need to check the other player.


