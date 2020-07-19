# inherited class shared_sprite
try:
    import sys
    from math import *  # using the import like this means you
    # don't need to type math.sin math.cos etc....
    import os
    import pygame
    from pygame.locals import *
    from enum import Enum
    from datetime import datetime, timedelta

except ImportError as err:
    print("couldn't load module. %s" % err)
    sys.exit(2)

pygame.init()
infoObject = pygame.display.Info()
#pygame.display.set_mode((infoObject.current_w, infoObject.current_h))

screeny =  650 #infoObject.current_h  # 650 #650 is also good.
screenx =  1250 #infoObject.current_w  # 1250#1580
basescale = sqrt(screeny*screenx / (650*1250))  #
speed = 27 * basescale
gravity = 0.56 * basescale
y_compression = False
max_ball_speed = 25

# [resource handling functions here]
def load_png(name):
    """ Load image and return image object"""
    fullname = os.path.join('data', name)
    try:
        image = pygame.image.load(fullname)
        if image.get_alpha() is None:
            image = image.convert()
        else:
            image = image.convert_alpha()
    except pygame.error as message:
        print('Cannot load image:', fullname)
        raise SystemExit(message)
    return image


class SharedSprite(pygame.sprite.Sprite):

    def __init__(self, imagename, scale=1, flip=False, rotate_angle = 0):
        pygame.sprite.Sprite.__init__(self)
        self.image = load_png(imagename)
        if flip:
            self.image = pygame.transform.flip(self.image, True, False)
        if rotate_angle:
            self.image = pygame.transform.rotate(self.image, rotate_angle)
        self.rect = self.image.get_rect()

        self.image = pygame.transform.scale(self.image, (
        int(self.rect.width * basescale * scale), int(self.rect.height * basescale * scale)))
        self.rect = self.image.get_rect()
        self.oldpos = self.rect
        self.newpos = self.rect
        self.dyfix = int(self.rect.height / 2)
        self.dxfix = int(self.rect.width / 2)
        screen = pygame.display.get_surface()
        self.area = screen.get_rect()
        self.area.centery -= 50 * basescale  # move logical area up
        self.mask = pygame.mask.from_surface(self.image)  # Use `pygame.mask.from_surface` to get the masks.
        self.dX = 0.0
        self.dY = 0.0
        self.gravity = gravity
        self.initial_wall_dist = 150 * basescale
        self.boost = False
        self.dY2, self.dY1, self.dY0 = 0.0,0.0,0.0 # for debug
        self.old2, self.old1 = self.newpos, self.newpos
    def reinit(self):
        self.dX = 0.0
        self.dY = 0.0

    def update(self):
        # for debug
        self.dY3 = self.dY2
        self.dY2 = self.dY1
        self.dY1 = self.dY0
        self.dY0 = self.dY
        self.old3 = self.old2
        self.old2 = self.old1
        self.old1 = self.oldpos

        # for rolling back in case of collision
        self.oldpos = self.rect

        # move Create a copy of rect. Only the copy is moved to the new pos.
        self.newpos = self.rect.move(self.dX, self.dY)

        # Point rect to the same object as newpos:
        # Any action on newpos will move rect...(unlike before).
        self.rect = self.newpos

    def bestoverlap(self, player):
        if bestoverlap := testoverlap(player, self):
            self.orgpos, player.orgpos = self.oldpos, player.oldpos
            print (f'overlap 0:{bestoverlap}')
            # calculate best possible impact (without rolling back player:
            for i in range(7):
                self.rect = average_rect(self.newpos, self.oldpos)
                player.rect = average_rect(player.newpos, player.oldpos)
                if overlap := testoverlap(player, self):
                    self.newpos, player.newpos = self.rect, player.rect
                    if bestoverlap==overlap:
                        break
                    bestoverlap = overlap
                    if isinstance(player,Boundry):
                        print(f'overlap {i}:{bestoverlap}')
                else:
                    self.oldpos, player.oldpos = self.rect, player.rect
            return bestoverlap
        return None

    def process_impact (self,player,bestoverlap):
        # the effect of the collision is calculated by Impulse Equations.
        impact_gamma = angle_ofdxdy((bestoverlap[0] - self.dxfix, (bestoverlap[1] - self.dyfix)))[0]
        ((self.dX, self.dY), (player.dX, player.dY)) = calc_impulse_new(self,player,impact_gamma)
        # self.rollback(player)
        # assert not testoverlap(player, self)

    def rollback(self, other_object=None):
        self.rect = self.oldpos
        if other_object:
            other_object.rollback()

    def accellerate(self, initialspeed, profile):
        # apply acceleration function:
        y = initialspeed
        if profile == 1:
            a = - 0.000008 * y ** 4 - 0.000146561 * y ** 3 + 0.000800701 * y ** 2 - 0.0853439 * y - 2
        elif profile == 2:
            a = -0.00000536 * y ** 4 - 0.000177438 * y ** 3 - 0.00168125 * y ** 2 - 0.0500764 * y - 1
        elif profile == 3:
            a = 0.000001421 * y ** 5 + 0.00000749 * y ** 4 - 0.000827811 * y ** 3 - 0.00374945 * y ** 2 + 0.0185639 * y - 1
        elif profile == 4:
            a = -1
        else:
            a = 0
        # print (a)
        return a

    @property
    def weight(self):
        """calculates weight"""
        return 1

    @property
    def vector(self):
        return angle_ofdxdy((self.dX,self.dY))

class Net(SharedSprite):
    def __init__(self):
        SharedSprite.__init__(self, 'Net1.png')
        self.rect.midbottom = (self.area.midbottom[0], self.area.midbottom[1] + 0)

    @property
    def weight(self):
        """returns weight"""
        return 2

    def update(self):
        self.dY,self.dX = 0, 0

class Boundry(SharedSprite):
    def __init__(self):
        SharedSprite.__init__(self, 'Boundries.png')
        self.rect.midbottom = (self.area.midbottom[0], self.area.midbottom[1] + 0)

    @property
    def weight(self):
        """returns weight"""
        return 10

    def update(self):
        self.dY,self.dX = 0, 0

class Pointer(SharedSprite):
    def __init__(self):
        SharedSprite.__init__(self, 'Pointer2.png')
        self.rect.top = self.area.top + 52 * basescale


def testoverlap(p, s):
    # Calculate the offset between the rect
    # And pass the offset to the `overlap` method of the mask.
    offset_x = p.rect.x - s.rect.x
    offset_y = p.rect.y - s.rect.y
    overlap = s.mask.overlap(p.mask, (offset_x, offset_y))
    return overlap


def average_rect(source_rect, target_rect):
    x = (target_rect.midleft[0] + source_rect.midleft[0]) / 2
    y = (target_rect.midleft[1] + source_rect.midleft[1]) / 2
    new_rect = source_rect.copy()
    new_rect.midleft = (x, y)
    return new_rect


# ===============================================================================
# Impulse Equasions for resolving ball bat and wall impacts.
def angle_ofdxdy(dxdy):  # returns angle, z
    dx, dy = dxdy[0], dxdy[1]
    if abs(dy) < 0.01:  # prevent div by zero
        dy = 0.01
    # https://math.stackexchange.com/questions/1327253/how-do-we-find-out-angle-from-x-y-coordinates
    z = (dx ** 2 + dy ** 2) ** 0.5
    angle = 2 * atan(dy / (dx + z))
    return round(angle, 4), z


def calc_impulse_new(self,wall,gama):
    g = gama  # 0 needs further explainig. ba
    vec,vec_wall = self.vector, wall.vector
    t, t2 = vec[0], vec_wall[0]
    v, v2 = vec[1], vec_wall[1]  # a scalar.
    m, m2 = self.weight, wall.weight
    mv, m2v2 = 2 * m * v, 2 * m2 * v2
    vx = (v * cos(t - g) * (m - m2) + m2v2 * cos(t2 - g)) * cos(g) / (m + m2) + v * sin(t - g) * cos(g + pi / 2)
    vy = (v * cos(t - g) * (m - m2) + m2v2 * cos(t2 - g)) * sin(g) / (m + m2) + v * sin(t - g) * sin(g + pi / 2)
    v2x = (v2 * cos(t2 - g) * (m2 - m) + mv * cos(t - g)) * cos(g) / (m + m2) + v2 * sin(t2 - g) * cos(g + pi / 2)
    v2y = (v2 * cos(t2 - g) * (m2 - m) + mv * cos(t - g)) * sin(g) / (m + m2) + v2 * sin(t2 - g) * sin(g + pi / 2)
    if y_compression:
        s = f'before: {vx:.1f} {vy:.1f} after '
        for i in range(10):
            if sqrt(vx * vx + vy * vy) > max_ball_speed:
                vy *= 0.9
                vx *= 0.98
        s += f'{vx:.1f} {vy:.1f}'
        print(f'{datetime.now()} input V:{v:.1f} theta:{degrees(t):.1f} {s}')
    xyxy = ((round(vx, 2), round(vy, 2)), (round(v2x, 2), round(v2y, 2)))
    types = type(self)
    typewall = type (wall)
    print(f'\n{datetime.now()} \n{types}: {v:.1f}({degrees(t):.1f}\u2070)\t {typewall}:{v2:.1f}({degrees(t2):.1f}\u2070),\
        impact angle:{degrees(g):.2f}\u2070 masses:{m},{m2} result:{xyxy}')
    return xyxy

class State(Enum):
    MoveUp = 0
    MoveDown = 1
    MoveRight = 2
    MoveLeft = 3
    Still = 4

class Fault(Enum):
    Ok = 0
    Floor = 1
    Net = 2
    Touch3 = 3