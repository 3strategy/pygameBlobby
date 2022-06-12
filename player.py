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
        self.state = State.Still
        self.h_state = State.Still
        self.__fault: Fault = Fault.Ok
        self.canjump = True
        self.num_shots = 0
        self.score = 0

        if side == "left":
            SharedSprite.__init__(self, 'blobby6.webp', 0.3, True)
            self.sign = 1
            self.upKey = K_w
            self.downKey = K_s
            self.leftKey = K_a
            self.rightKey = K_d
        elif "right" == side:
            SharedSprite.__init__(self, 'blobbygreen.webp', 0.5)
            self.sign = -1
            self.upKey = K_UP
            self.downKey = K_DOWN
            self.leftKey = K_LEFT
            self.rightKey = K_RIGHT

        self.gravity = gravity * 3

        self.reinit()

    def reinit(self):

        if self.fault != Fault.Won:
            self.fault = Fault.Ok
        self.canjump = True
        self.num_shots = 0
        self.state = State.Still
        self.h_state = State.Still
        if self.side == "left":
            self.rect.midbottom = (self.area.midleft[0] + self.initial_wall_dist, self.area.bottom)

        elif "right" == self.side:
            self.rect.midbottom = (self.area.midright[0] - self.initial_wall_dist, self.area.bottom)
            self.sign = -1

        SharedSprite.reinit(self)

    def move(self, event: pygame.event):
        if event.type == KEYDOWN:  # we only want to trigger a move on keydown.
            if event.key == self.upKey:
                self.state = State.MoveUp

            if event.key == self.rightKey:
                self.h_state = State.MoveRight
            elif event.key == self.leftKey:
                self.h_state = State.MoveLeft

        elif event.type == KEYUP:
            # some key up should trigger "stand still", (e.g. the upKey is depressed while moving up)
            if self.state == State.MoveUp and event.key == self.upKey \
                    or (self.state == State.MoveDown and event.key == self.downKey):
                self.state = State.Still

            if self.h_state == State.MoveRight and event.key == self.rightKey \
                    or (self.h_state == State.MoveLeft and event.key == self.leftKey):
                self.h_state = State.Still

    def update(self):
        SharedSprite.update(self)

        if self.dX != 0:  # Player horisontal position checks:
            # avoid approaching the net   and avoid exiting the field
            if not Player.netApproach < abs(
                    self.area.centerx - self.newpos.centerx) < self.area.centerx + Player.sideApproach:
                self.newpos.centerx -= self.dX
                self.dX = 0

        if self.state == State.MoveUp:
            self.dY += 0.6 * self.gravity
        else:
            self.dY += self.gravity

        if self.newpos.bottom >= self.area.bottom:  # player touches the floor
            self.newpos.bottom = self.area.bottom
            if self.state == State.MoveUp:
                self.dY = -self.speed
            else:
                self.dY = 0
            self.canjump = True

        pygame.event.pump()

    @property
    def state(self):
        """holds the Vertical state"""
        return self.__vstate

    @state.setter
    def state(self, val):
        if val == State.MoveUp:
            if self.canjump:
                self.dY = -self.speed
                self.canjump = False
            self.__vstate = val
        else:
            self.__vstate = State.Still

    @property
    def h_state(self):
        return self.__h_state

    @h_state.setter
    def h_state(self, val):
        if val == State.MoveLeft:
            self.dX = -self.horisontal_speed
            self.__h_state = val
        elif val == State.MoveRight:
            self.dX = self.horisontal_speed
            self.__h_state = val
        else:
            self.dX = 0
            self.__h_state = State.Still

    @property
    def weight(self):
        """calculates weight. The idea is that player is heavier when on the ground.
        can hit harder and bounce less"""
        return 300 if self.rect.bottom == self.area.bottom else 3

    @property
    def fault(self):
        """explanation of lost point"""
        return self.__fault

    @fault.setter
    def fault(self, val):
        # prevent overwriting state Won.
        if self.__fault == Fault.Won:
            return
        else:
            self.__fault = val
