# game class (main)
try:
    import sys
    import re
    from player import *
    from ball import *
except ImportError as err:
    print("couldn't load module. %s" % err)
    sys.exit(2)


def main():
    # Initialise screen
    # pygame.init()
    # screen = pygame.display.set_mode((screenx, screeny),pygame.FULLSCREEN)
    screen = pygame.display.set_mode((screenx, screeny))

    pygame.display.set_caption('Blobby')

    background = pygame.image.load('data\\beachback.jpg')
    background = pygame.transform.scale(background, (screenx, screeny))
    background = background.convert()

    # Initialise players, net, and ball
    players = (Player("left"), Player("right"))
    net = Net()
    boundry = Boundry()
    pointer = Pointer()
    ball = Ball(players, net, pointer, boundry)
    Player.ball = ball  # give player a static reference to ball.

    # Initialise sprites' groups
    playersprites = pygame.sprite.RenderPlain(players)
    ballsprites = pygame.sprite.RenderPlain(ball, pointer)

    othersprites = pygame.sprite.RenderPlain(boundry, net)

    # Display some text
    font = pygame.font.Font(None, 36)
    text = font.render("Hello There", 1, (250, 250, 250))
    textpos = text.get_rect()
    textpos.centerx = background.get_rect().centerx

    # Initialise clock
    clock = pygame.time.Clock()

    # Game loop
    while 1:
        # Make sure game doesn't run at more than 60 frames per second
        clock.tick(54)

        for event in pygame.event.get():
            if event.type == QUIT or event.type == KEYDOWN and event.key == K_ESCAPE:
                return
            # OOP:Don't ask for the information you need to do the work;
            # ask for the object that has information to do the work for you. (Allen Hollub)
            for player in players:
                player.move(event)

        p0, p1 = players[0], players[1]
        info = f'{p0.score}   :   {p1.score}'
        if p0.fault != Fault.Ok:
            fl = re.search(r'((\w*)\.(\w*))', f'{p0.fault}').group(3)
            info = f'{fl} {info}'
        elif p1.fault != Fault.Ok:
            fl = re.search(r'((\w*)\.(\w*))', str(p1.fault)).group(3)
            info = f'{info}  {fl}'
        # info = f'{p0.state} {info}  {p1.state} dX:{p1.dX:.1f} dY:{p1.dY:.1f}'
        # info = f'{info} Ball dX:{ball.dX:.1f} dY:{ball.dY:.1f}'
        # note the : after which comes the formatting (here .1f for 1 decimal point)
        text = font.render(info, 1, (250, 250, 250))

        screen.blit(background, (0, 0))  # this acts as a clear screen (try without and see how everything smears)
        screen.blit(text, textpos)  # if we blit to background we are smearing.

        othersprites.update()
        playersprites.update()  # it matters if you update the player before or after the ball.
        ballsprites.update()  # calls the update method on sprite

        # othersprites.draw(screen)
        playersprites.draw(screen)
        ballsprites.draw(screen)  # blits every sprite to the screen.

        pygame.display.flip()  # refreshses the display with the content of 'screen'


if __name__ == '__main__':
    main()
